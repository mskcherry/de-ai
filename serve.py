"""
De-AI Local Server
==================
A tiny HTTP server that serves index.html AND writes modified .tex files
back to disk when the user clicks "Apply Changes".

Usage:
    python serve.py
    → Opens http://localhost:8384 automatically
"""

import http.server
import json
import shutil
import webbrowser
from datetime import datetime
from pathlib import Path

PORT = 8384
SERVE_DIR = Path(__file__).parent.resolve()


class DeAIHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static files + handles API endpoints for saving."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SERVE_DIR), **kwargs)

    def do_POST(self):
        if self.path == "/api/save":
            self._handle_save()
        elif self.path == "/api/list-tex":
            self._handle_list_tex()
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _handle_save(self):
        """Save modified .tex files back to disk."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            files = data.get("files", [])
            if not files:
                self._json_response(400, {"error": "No files to save"})
                return

            saved = []
            for f in files:
                filepath = f.get("path", "")
                content = f.get("content", "")
                original_name = f.get("name", "unknown.tex")

                if filepath:
                    # Resolve the path relative to the serve directory
                    target = Path(filepath).resolve()
                else:
                    # Fall back to name in the serve directory
                    target = SERVE_DIR / original_name

                # Security: ensure we're writing a .tex file
                if not str(target).lower().endswith(".tex"):
                    continue

                # Create backup before overwriting
                if target.exists():
                    backup_dir = target.parent / ".deai-backups"
                    backup_dir.mkdir(exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{target.stem}_{timestamp}{target.suffix}"
                    shutil.copy2(target, backup_dir / backup_name)

                # Write the modified content
                target.write_text(content, encoding="utf-8")
                saved.append(str(target))

            self._json_response(200, {
                "saved": saved,
                "count": len(saved),
                "message": f"Successfully saved {len(saved)} file(s)",
            })
            print(f"  [OK] Saved {len(saved)} file(s): {', '.join(saved)}")

        except Exception as e:
            self._json_response(500, {"error": str(e)})
            print(f"  [ERR] Error saving: {e}")

    def _handle_list_tex(self):
        """List .tex files in a directory."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            directory = data.get("directory", str(SERVE_DIR))

            target_dir = Path(directory).resolve()
            if not target_dir.is_dir():
                self._json_response(400, {"error": f"Not a directory: {directory}"})
                return

            tex_files = []
            for tex in sorted(target_dir.rglob("*.tex")):
                tex_files.append({
                    "path": str(tex),
                    "name": tex.name,
                    "relative": str(tex.relative_to(target_dir)),
                    "size": tex.stat().st_size,
                })

            self._json_response(200, {"files": tex_files, "directory": str(target_dir)})

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format, *args):
        """Quieter logging."""
        try:
            msg = format % args
        except Exception:
            msg = str(args)
        if "/api/" in msg:
            print(f"  [API] {msg}")
        elif ".html" in msg:
            print(f"  [WEB] {msg}")


def main():
    print()
    print("  +--------------------------------------------+")
    print("  |        De-AI Local Server                   |")
    print("  +--------------------------------------------+")
    print(f"  |  URL:  http://localhost:{PORT}              |")
    print(f"  |  Dir:  {str(SERVE_DIR)[:36]:36s}  |")
    print("  |  Press Ctrl+C to stop                      |")
    print("  +--------------------------------------------+")
    print()

    server = http.server.HTTPServer(("", PORT), DeAIHandler)

    # Auto-open browser
    url = f"http://localhost:{PORT}/index.html"
    print(f"  >> Opening {url} ...")
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
