# Continuity: The AI Project Manager

**Continuity** is an autonomous terminal-based AI agent that manages your project, edits files, and handles Git version control automatically. Built with Google Gemini 2.0 Flash Lite.

## 🚀 Features
* **Context Awareness:** Automatically reads `memory/project_status.md` to understand the project state.
* **Autonomous File Editing:** Can read, write, and update code files without copy-pasting.
* **Git Integration:** Auto-backups with intelligent commit messages (`git add .` -> `git commit`).
* **Self-Healing:** Includes auto-retry logic for API rate limits.

## 📦 Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/continuity.git](https://github.com/YOUR_USERNAME/continuity.git)
    cd continuity
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-generativeai typer rich python-dotenv
    ```

3.  **Setup API Key:**
    Create a `.env` file:
    ```text
    GEMINI_API_KEY=your_google_api_key_here
    ```

## 🛠️ Usage

Start the agent:
```bash
python3 core/main.py
