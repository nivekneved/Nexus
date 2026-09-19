import os
import sys
import time
import schedule
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from core.agent_manager import AgentManager
from core.overnight_chronicle import overnight_chronicle

console = Console(force_terminal=True, legacy_windows=False)

def night_shift_job(manager: AgentManager):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[bold cyan]🌙 [NIGHT SHIFT TRIGGER] {now_str}: Initiating autonomous multi-agent sweep...[/bold cyan]")
    
    try:
        res = overnight_chronicle.run_full_night_shift_cycle()
        
        table = Table(title=f"Night Shift Cycle #{res.get('cycle_number')} Summary ({res.get('duration_seconds')}s)", style="blue")
        table.add_column("Agent / Employee", style="bold white")
        table.add_column("Status", justify="center")
        
        for agent_id, status in res.get("results", {}).items():
            status_badge = "[green]SUCCESS[/green]" if status is True else f"[yellow]{status}[/yellow]"
            table.add_row(agent_id, status_badge)
            
        console.print(table)
        console.print(f"[dim]Next scheduled run: {res.get('next_run')}[/dim]")
    except Exception as e:
        console.print(f"[bold red]❌ Night Shift run encountered an error: {e}[/bold red]")

def main():
    console.print(Panel.fit(
        "[bold green]🌙 NEXUS 24/7 AUTONOMOUS OVERNIGHT WORKFORCE DAEMON[/bold green]\n"
        "[white]Running silent multi-agent cycles while you sleep.[/white]\n"
        "[cyan]Schedule: Every 30 minutes | Audit: overnight_activity.json[/cyan]\n"
        "[dim]Press Ctrl+C to terminate the daemon.[/dim]",
        border_style="green"
    ))

    # Initialize manager and discover plugins
    manager = AgentManager()
    manager.discover_plugins("agents")
    overnight_chronicle.agent_manager = manager

    # 1. Run immediate kick-off cycle
    night_shift_job(manager)

    # 2. Schedule recurring every 30 minutes
    schedule.every(30).minutes.do(night_shift_job, manager)

    # Heartbeat loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Daemon shutting down gracefully. Good morning![/yellow]")

if __name__ == "__main__":
    main()
