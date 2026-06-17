# Project: Continuity CLI
**Status:** Phase 3
**Date:** 2024-05-21

## Core Mission
Build a terminal-based AI agent that manages its own development and documentation.

## Current Objectives
- [ ] Revoke/rotate the Gemini API key that was hardcoded in `scripts/check_models.py` (now removed) since it may have been exposed in git history.
- [ ] Add a `requirements.txt` (README references `pip install -r requirements.txt` but the file doesn't exist).
- [ ] Wire `core/log_insight.py` into the main chat loop so sessions auto-log to `logs/*.log` and get analyzed (it currently reads `logs/*.log` but `core/main.py` doesn't write any).
- [ ] Decide the fate of `core/mock.py` (demo/offline mode) — keep as an explicit `--mock` flag on `main.py`, or remove it.
- [ ] Add basic tests around the tool functions in `core/main.py` (`read_file`, `write_file`, `run_git`).
- [ ] Harden `run_git`: current blocklist (`;`, `&&`, `|`) is a weak guard against arbitrary git subcommands; consider an allowlist of safe subcommands instead.

## Technical Constraints
- Language: Python 3.10+
- AI: Gemini 1.5 Flash (for speed) or Pro (for complex reasoning).
- Backup: Git (Automated).
