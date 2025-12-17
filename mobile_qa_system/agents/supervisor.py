from __future__ import annotations

from pathlib import Path
from datetime import datetime

from agents.executor import DeviceExecutor
from agents.verifier import UIVerifier


class Supervisor:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.runs_dir = self.base_dir / "runs"
        self.runs_dir.mkdir(exist_ok=True)

    def start_run(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = self.runs_dir / f"run_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Starting test run: {run_dir}")

        # 1) Executing capture step (should create screen.png and ui.xml in run_dir)
        executor = DeviceExecutor(run_dir)
        executor.execute_step()

        # 2) Verifying results exist
        ui_xml_path = run_dir / "ui.xml"
        screenshot_path = run_dir / "screen.png"

        if not ui_xml_path.exists():
            raise FileNotFoundError(f"Expected ui.xml not found at: {ui_xml_path}")
        if not screenshot_path.exists():
            raise FileNotFoundError(f"Expected screen.png not found at: {screenshot_path}")

        print("Verifying UI...")

        # 3) Verification
        verifier = UIVerifier(ui_xml_path)

    
        targets = [
    "Hey bestie! This is my first app!",
]

        result = verifier.verify_any(targets)

        
        result_file = run_dir / "result.txt"

        if result.matched:
            print(f"Verifier check: OK (matched '{result.target}', count={result.count})")
            result_file.write_text(
                f"PASS\nMatched: {result.target}\nCount: {result.count}\nExamples: {result.examples}\n",
                encoding="utf-8"
            )
        else:
            
            print("Verifier check: NOT FOUND in ui.xml.")
            print("Debug examples (from ui.xml text fields):")
            for ex in result.examples[:10]:
                print(f"  - {ex}")

            result_file.write_text(
                "FAIL\n"
                f"Could not find any of: {result.target}\n"
                "This can happen if the app content is a WebView and does not appear in ui.xml.\n"
                f"Debug text examples: {result.examples}\n",
                encoding="utf-8"
            )

            

        print("Run complete.")
