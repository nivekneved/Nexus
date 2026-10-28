import os
import time
import subprocess
import schedule
from datetime import datetime

# Define the absolute paths to the scripts
ROOT_DIR = r"C:\Users\deven\OneDrive\Desktop\Agents"
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

OSINT_SCRIPTS = [
    os.path.join(SCRIPTS_DIR, "real_lead_scraper_overpass.py"),
    os.path.join(SCRIPTS_DIR, "real_lead_scraper_github.py"),
    os.path.join(SCRIPTS_DIR, "real_lead_scraper_xray.py"),
    os.path.join(SCRIPTS_DIR, "osint_hiring_hijacker.py"),
    os.path.join(SCRIPTS_DIR, "osint_cert_sniper.py"),
    os.path.join(SCRIPTS_DIR, "osint_real_estate.py")
]

DISPATCHER_SCRIPT = os.path.join(SCRIPTS_DIR, "dispatch_cold_emails.py")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_script(script_path):
    log(f"Executing: {os.path.basename(script_path)}...")
    try:
        # Run the script and wait for it to finish
        result = subprocess.run(["python", script_path], cwd=ROOT_DIR, capture_output=True, text=True)
        if result.returncode == 0:
            log(f"SUCCESS: {os.path.basename(script_path)}")
            # Print the last few lines of output for context
            lines = result.stdout.strip().split('\n')
            for line in lines[-3:]:
                if line.strip(): print(f"    > {line}")
        else:
            log(f"ERROR: {os.path.basename(script_path)} failed with code {result.returncode}")
            print(result.stderr)
    except Exception as e:
        log(f"FATAL ERROR running {script_path}: {e}")

def execute_revenue_cycle():
    """
    The main autonomous cycle:
    1. Hunt for fresh leads across all OSINT channels.
    2. Dispatch the pitch to newly found, unique leads.
    """
    print("\n" + "="*70)
    log("🦅 NEXUS REVENUE AUTOPILOT CYCLE INITIATED")
    print("="*70)

    # Phase 1: Hunt
    log("--- PHASE 1: HUNTING (OSINT GATHERING) ---")
    for script in OSINT_SCRIPTS:
        run_script(script)
        time.sleep(5) # Brief pause between scraping engines

    # Phase 2: Dispatch
    log("--- PHASE 2: DISPATCH (FIRING PITCHES) ---")
    run_script(DISPATCHER_SCRIPT)

    log("✅ CYCLE COMPLETE. Awaiting next scheduled run.")
    print("="*70 + "\n")

def start_autopilot():
    log("Nexus Revenue Autopilot is ALIVE.")
    log("Target: Generate real revenue via autonomous OSINT hunting & pitching.")

    # Run once immediately on startup
    execute_revenue_cycle()

    # Schedule the cycle to run every 6 hours
    # This prevents exhausting sources and keeps under Gmail/API rate limits
    schedule.every(6).hours.do(execute_revenue_cycle)

    log("Scheduler active. Entering background loop (6-hour intervals).")
    log("Press Ctrl+C to terminate the autopilot.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)

    except KeyboardInterrupt:
        log("Autopilot terminated by user.")

if __name__ == "__main__":
    start_autopilot()
