## Task: Open Gmail on Android

### Description
This task demonstrates a minimal Android UI agent that autonomously interacts with an emulator to locate and open the Gmail application.

### Environment
- Android Emulator (Pixel device)
- Android Debug Bridge (ADB)
- Python-based agent framework

### Agent Actions
- Verifies device availability via ADB
- Performs a swipe gesture to scroll the home screen
- Launches the Gmail application
- Captures the UI hierarchy
- Verifies that Gmail is present in the UI

### Result
The agent successfully opened the Gmail application and confirmed the task completion via UI verification.

### Demo
See `demo.mp4.mov` for a short screen recording of the agent execution.
