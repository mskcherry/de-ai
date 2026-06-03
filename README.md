# De-AI

**Remove AI fingerprints from your academic LaTeX papers — right in the browser.**

De-AI scans `.tex` files for 80+ AI-flagged words, filler phrases, generic closers, and significance inflation patterns. It presents an interactive review interface where you accept or reject each change, then writes the cleaned files back to disk.

---

## Quick Start

```bash
python serve.py
```

This starts a local server at **http://localhost:8384** and opens it in your browser automatically.

### Usage

1. **Upload** — Drag & drop `.tex` files or select an entire folder
2. **Scan** — Click **"De-AI'ze"** to detect AI writing patterns
3. **Review** — Accept ✓ or reject ✕ each suggested change (with tooltips explaining why)
4. **Save** — Click **"Apply & Download .tex"** to write changes back to your files

> Backups are created automatically in `.deai-backups/` before any file is overwritten.

---

## What It Detects

| Category | Examples | Priority |
|---|---|---|
| **Tier 1 — Most flagged** | `novel`, `comprehensive`, `cutting-edge`, `groundbreaking`, `pioneering` | P1 |
| **Tier 2 — Frequently flagged** | `leverages→uses`, `enhances→improves`, `utilize→use`, `facilitate→enable`, `robust`, `scalable`, `innovative`, `delve` | P2 |
| **Filler phrases** | "highlights the importance of", "it is worth noting that", "in the realm of", "plays a crucial role in" | P1 |
| **Generic closers** | "paving the way for", "opens new avenues", "positioning it as a", "serves as a critical foundation" | P1 |
| **Significance inflation** | "fundamental", "significant", "novel", "innovative" — removed when used as empty emphasis | P1–P2 |

### LaTeX-Aware

The scanner **never touches** content inside:
- `\cite{}`, `\ref{}`, `\label{}`, `\url{}`, `\texttt{}`
- Math environments (`$...$`, `$$...$$`)
- Comments (`% ...`)
- Any `\command{...}` structure

---

## Project Structure

```
De-AI/
├── index.html                  # Upload & interactive review UI
├── serve.py                    # Local Python server (writes files to disk)
├── README.md                   # This file
└── academic-writing-skills/    # De-AI toolkit (skills, scripts, references)
```

---

## Requirements

- **Python 3.10+** (standard library only — no `pip install` needed)
- A modern browser (Chrome, Edge, Firefox)

---

## How It Works

### Without the server (`file://` mode)

Open `index.html` directly in a browser. Everything works except saving — accepted changes are **downloaded** as modified `.tex` files that you manually replace.

### With the server (`http://localhost:8384`)

Run `python serve.py`. The server adds a `/api/save` endpoint that writes modified files **directly back to disk**, with automatic timestamped backups in `.deai-backups/`.

---

## Powered By

Built on top of [academic-writing-skills](https://github.com/bahayonghang/academic-writing-skills) — a toolkit for De-AI editing, grammar analysis, format checks, bibliography verification, and experiment narrative generation for academic papers.

---

## License

Academic Use Only — Not for commercial use.
