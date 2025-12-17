import subprocess
from pathlib import Path
from datetime import datetime


class DeviceExecutor:
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir

    def run_command(self, command: list[str]) -> str:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def capture_ui(self):
        print("Capturing UI hierarchy...")
        self.run_command(["adb", "shell", "uiautomator", "dump"])
        self.run_command(["adb", "pull", "/sdcard/ui.xml", str(self.run_dir / "ui.xml")])

    def capture_screenshot(self):
        print("Capturing screenshot...")
        screenshot_path = self.run_dir / "screen.png"
        subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout=open(screenshot_path, "wb"),
            check=True
        )

    def execute_step(self):
        self.capture_ui()
        self.capture_screenshot()
