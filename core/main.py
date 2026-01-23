import os
import sys
import time
import subprocess
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
# Using the only model available to your account
MODEL_NAME = "gemini-2.0-flash-lite-preview-02-05"
MAX_RETRIES = 5

console = Console()

if not API_KEY:
    sys.exit("CRITICAL ERROR: GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

# --- THE TOOLS ---
def read_file(filepath: str):
    """Reads a file. Usage: read_file('memory/project_status.md')"""
    if not os.path.exists(filepath): return f"Error: {filepath} not found."
    with open(filepath, "r") as f: return f.read()

def write_file(filepath: str, content: str):
    """Writes/Overwrites a file. Usage: write_file('notes.md', 'content')"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f: f.write(content)
        return f"Success: Wrote to {filepath}"
    except Exception as e: return str(e)

def run_git(command: str):
    """Runs a git command. Usage: run_git('add .')"""
    if any(bad in command for bad in [";", "&&", "|"]): return "Error: Chaining commands not allowed."
    full_cmd = f"git {command}"
    try:
        print(f"🤖 [System] Executing: {full_cmd}") 
        result = subprocess.run(full_cmd.split(), capture_output=True, text=True)
        return f"Git Output: {result.stdout} {result.stderr}"
    except Exception as e: return str(e)

# --- THE ARCHITECTURE (ROBUSTNESS) ---
def send_message_with_retry(chat, message):
    """
    Sends a message to the Gemini API with automatic retries for rate limits.
    
    This function handles the 'ResourceExhausted' (429) error by implementing
    an exponential backoff strategy.
    
    Args:
        chat: The active chat session object.
        message (str): The user's input string.
        
    Returns:
        response: The API response object or an error string.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            if not message.strip(): return None # Ignore empty inputs
            return chat.send_message(message)
        except exceptions.ResourceExhausted:
            # If we hit error 429 (Rate Limit), we wait.
            # Strategy: 2^0=1s, 2^1=2s, 2^2=4s... (+1s buffer)
            wait_time = (2 ** retries) + 1 
            console.print(f"[bold red]⚠️  Rate Limit Hit. Cooling down for {wait_time}s...[/bold red]")
            time.sleep(wait_time)
            retries += 1
        except Exception as e:
            return f"Error: {e}"
    return "[Error] Max retries exceeded. API is too busy."

def start_chat():
    tools = [read_file, write_file, run_git]
    
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        tools=tools,
        system_instruction="""
        You are Continuity, a Production-Grade AI Project Manager.
        
        PROTOCOL:
        1. Manage Files: read_file, write_file
        2. Version Control: run_git
        3. BEHAVIOR: 
           - Always read 'memory/project_status.md' first.
           - When asked to document, read the source code first.
           - When asked to backup, run 'git add .' then 'git commit'.
        """
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)
    console.print(f"[bold green]🟢 Continuity v5 (Refactored) Online[/bold green]")
    console.print(f"[dim]Engine: {MODEL_NAME} | Auto-Retry: Enabled[/dim]\n")

    while True:
        user_input = console.input("[bold yellow]You > [/bold yellow]")
        if user_input.lower() in ["exit", "quit"]: break
        if not user_input.strip(): continue
        
        response = send_message_with_retry(chat, user_input)
        
        if response:
            if isinstance(response, str):
                console.print(f"[red]{response}[/red]")
            elif response.parts:
                try:
                    console.print(Markdown(response.text))
                except ValueError:
                    console.print("[dim]Action completed (Silent Success).[/dim]")
            else:
                console.print("[dim]Action completed.[/dim]")

if __name__ == "__main__":
    start_chat()
