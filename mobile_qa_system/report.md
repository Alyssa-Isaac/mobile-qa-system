# Mobile QA System – Project Report

This repository contains a minimal Android UI automation agent built using Python and ADB.

## Design Rationale

A full design rationale, architecture explanation, and early demo are documented in:

📄 `Framework Analysis and Video.pdf`

This document explains:
- Why Python and ADB were chosen
- The supervisor–executor architecture
- Tradeoffs between visual vs UI-hierarchy verification

## Implemented Tasks

- Task 01: UI Hierarchy Capture  
  Captures and persists the Android UI hierarchy using UIAutomator for downstream verification.  
  See `results/task_01_ui_hierarchy/`

- Task 02: Open Gmail  
  Demonstrates end-to-end task execution using the supervisor–executor–verifier pipeline, including app launch, UI capture, and verification.  
  See `results/open_gmail/`

- Task 03: Open Settings  
  Demonstrates task reuse and extensibility by launching a different Android application using the same executor and supervisor logic.  
  See `results/open_settings/`
