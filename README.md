# GPT-Test

Automation project for **web** and **desktop** apps using Playwright, Pytest, and Pywinauto.

---

## Repository layout

| Path                 | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| `pages/`             | Page Objects (Web + Desktop)                                |
| `tests/`             | Pytest test suites                                          |
| `.github/workflows/` | CI pipelines (web on GitHub‑hosted, desktop on self‑hosted) |
| `requirements.txt`   | Runtime dependencies                                        |
| `README.md`          | This guide                                                  |

---

## Prerequisites

### Local development

* **Python 3.11** (64‑bit) – [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Install deps & Playwright browsers:

  ```bash
  pip install -r requirements.txt
  playwright install
  ```
* **Windows 10/11 GUI** for desktop tests (`mspaint.exe` shipped by default).

### Self‑hosted runner (Windows)

1. Create folder `C:\actions-runner`.
2. Download & unzip `actions-runner-win-x64-2.325.0.zip`.
3. Configure the runner:

   ```powershell
   .\config.cmd --url https://github.com/<org>/<repo> --token <TOKEN>
   .\run.cmd               # run interactively (not as service)
   ```
4. Runner labels used by the workflow: `self-hosted`, `windows`, `x64`.

> **Important:** GUI automation requires an **interactive session**. Do *not* run the runner as a Windows service unless you enable desktop interaction (not recommended).

---

## Running tests

### Web (Playwright)

```bash
pytest tests/web -v --base-url=https://example.com
```

### Desktop (Pywinauto)

```bash
pytest tests/desktop -v
```

The current desktop test `test_open_paint.py` simply opens **Paint**, asserts the window is visible, then closes it.

---

## CI pipelines

| Job       | Runner label set            | Purpose             |
| --------- | --------------------------- | ------------------- |
| `web`     | `windows-latest` (hosted)   | Playwright tests    |
| `desktop` | `self-hosted, windows, x64` | Pywinauto GUI tests |

Each job publishes an HTML report as artifact `*test-report*`.

---

## Troubleshooting

| Issue                                      | Fix / hint                                                           |
| ------------------------------------------ | -------------------------------------------------------------------- |
| `ElementNotFoundError` in desktop tests    | Ensure runner is in **interactive** session (`run.cmd`).             |
| PowerShell script blocked                  | Run as admin: `Set-ExecutionPolicy RemoteSigned -Scope LocalMachine` |
| Runner “session already exists / conflict” | Stop duplicate services; keep only **one** runner active             |

---

## Contributing

1. Create a feature branch (`feat/<topic>`).
2. Use **Codex Workspace** to generate or edit code.
3. Run linters & tests locally → open a Pull Request.

---

## License

MIT © 2025 – csalcantaraBR

