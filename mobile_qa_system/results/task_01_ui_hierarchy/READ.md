## Task 1: Capture UI Hierarchy

### Goal
Capture the Android UI hierarchy using UIAutomator and save outputs for inspection.

### What it does
- Connects to emulator via ADB
- Dumps UI hierarchy to XML
- Saves artifacts per run folder (`runs/run_YYYYMMDD_HHMMSS/`)

### Artifacts
- `ui.xml` (UIAutomator dump)
- `screen.png` or screenshot output (if captured)
- `terminal_success.png` (execution proof)

### How to run
From project root:
```bash
python main.py
