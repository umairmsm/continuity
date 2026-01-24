import os
import sys
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
# The NEW SDK can access the stable model
MODEL_NAME = "gemini-2.5-flash"

console = Console()

if not API_KEY:
    sys.exit("CRITICAL ERROR: GEMINI_API_KEY not found in .env")

# Initialize the Modern Client
client = genai.Client(api_key=API_KEY)

# --- THE TOOLS ---
def read_file(filepath: str):
    """Reads a file from the project."""
    if not os.path.exists(filepath): return f"Error: {filepath} not found."
    with open(filepath, "r") as f: return f.read()

def write_file(filepath: str, content: str):
    """Writes a file to the project."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f: f.write(content)
        return f"Success: Wrote to {filepath}"
    except Exception as e: return str(e)

def run_git(command: str):
    """Runs a git command."""
    if any(bad in command for bad in [";", "&&", "|"]): return "Error: Chaining commands not allowed."
    full_cmd = f"git {command}"
    try:
        print(f"🤖 [System] Executing: {full_cmd}") 
        result = subprocess.run(full_cmd.split(), capture_output=True, text=True)
        return f"Git Output: {result.stdout} {result.stderr}"
    except Exception as e: return str(e)

# Map tools for the new SDK
tools_map = [read_file, write_file, run_git]

# --- THE CHAT LOOP ---
def start_chat():
    # Create the chat session with the new syntax
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            tools=tools_map,
            system_instruction="""
            You are Continuity, a Production-Grade AI Project Manager.
            PROTOCOL:
            1. Always read 'memory/project_status.md' first.
            2. When asked to backup, run 'git add .' then 'git commit'.
            3. Be concise.
            """
        )
    )
    
    console.print(f"[bold green]🟢 Continuity V6 (Modern Engine) Online[/bold green]")
    console.print(f"[dim]Engine: {MODEL_NAME} | SDK: google-genai (v1.0)[/dim]\n")

    while True:
        user_input = console.input("[bold yellow]You > [/bold yellow]")
        if user_input.lower() in ["exit", "quit"]: break
        if not user_input.strip(): continue

        try:
            # The new SDK handles tool calling automatically and robustly
            response = chat.send_message(user_input)
            
            if response.text:
                console.print(Markdown(response.text))
            else:
                # If text is empty, it means tools ran silently. Check parts.
                console.print("[dim]Action completed successfully.[/dim]")
                
        except Exception as e:
            console.print(f"[bold red]System Error: {e}[/bold red]")

if __name__ == "__main__":
    start_chat()
