import glob
import os
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_logs():
    # 1. Find the most recent log file
    files = glob.glob('logs/*.log')
    if not files:
        console.print("[bold red]❌ No log files found.[/bold red]")
        return

    latest_file = max(files, key=os.path.getctime)
    console.print(f"\n[bold blue]🔎 Analyzing Target:[/bold blue] [dim]{latest_file}[/dim]")

    # 2. Setup the dashboard
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Signal", style="dim", width=10)
    table.add_column("Event Details")

    error_count = 0
    action_count = 0

    # 3. Scan the file
    with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            clean_line = line.strip()
            
            # Detect Errors
            if "Error" in clean_line or "Exception" in clean_line or "Traceback" in clean_line:
                error_count += 1
                table.add_row("[bold red]ERROR[/bold red]", f"[red]{clean_line[:90]}[/red]")
            
            # Detect System Actions (Git, File I/O)
            elif "[System]" in clean_line:
                action_count += 1
                # Clean up the log tag for display
                msg = clean_line.split("System]")[-1].strip()
                table.add_row("[green]ACTION[/green]", msg)

    # 4. Display Results
    if error_count > 0 or action_count > 0:
        console.print(table)
    else:
        console.print("[italic]Log is clean (No major events detected).[/italic]")

    # Summary Footer
    console.print(f"\n[bold]📊 Summary:[/bold] {error_count} Errors | {action_count} Actions Executed\n")

if __name__ == "__main__":
    analyze_logs()
