"""
NEXUS™ — J.A.R.V.I.S. (Iron Man Voice & Terminal Command Console)
Standalone Terminal & Voice-Controlled Assistant for Mr. Deven Pawaray (Sir).
"""

import sys
import os
import json
import time
from datetime import datetime

# UTF-8 fix for Windows Console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv()

from core.jarvis_service import jarvis_service
from core.agent_manager import AgentManager

BANNER = r"""
   ╦ ╔═╗ ╦═╗ ╦  ╦ ╦ ╔═╗   ┌──────────────────────────────────────────────┐
   ║ ╠═╣ ╠╦╝ ╚╗╔╝ ║ ╚═╗   │  J.A.R.V.I.S. • STARK PROTOCOL ONLINE       │
  ╚╝ ╩ ╩ ╩╚═  ╚╝  ╩ ╚═╝   │  Principal: Deven Pawaray (Sir)              │
                          │  Nexus AI Fleet: 16 Autonomous Agents Active │
                          └──────────────────────────────────────────────┘
"""

def print_typewriter(text: str, delay: float = 0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def speak_local(text: str):
    """Optional local text-to-speech fallback using pyttsx3 or SAPI if installed."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # Strictly prioritize male voices (David, George, Daniel, Oliver, Mark) and reject female voices
        voices = engine.getProperty('voices')
        female_names = ["female", "zira", "hazel", "susan", "catherine", "linda", "eva"]
        for v in voices:
            name = v.name.lower()
            if any(f in name for f in female_names):
                continue
            if any(m in name for m in ["george", "daniel", "arthur", "david", "mark", "male", "oliver"]):
                engine.setProperty('voice', v.id)
                break
        engine.setProperty('rate', 185)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

from core.jarvis_file_engine import jarvis_file_engine

def main():
    print("\033[96m" + BANNER + "\033[0m")
    
    # Initialize Agent Manager for live fleet commands
    manager = AgentManager()
    manager.discover_plugins("agents")
    
    status = jarvis_service.get_system_context(agent_manager=manager)
    print(f"\033[90m[TELEMETRY] Arc Reactor: {status.get('power_level')} | Time: {status.get('current_time')}\033[0m")
    print(f"\033[90m[TELEMETRY] Fleet: {status.get('fleet_scale')} | Defense: {status.get('defense_shields')}\033[0m")
    print(f"\033[90m[FILE ENGINE] Full Root Access: Active | Syntax Validator: Online\033[0m")
    print("\033[33mType your directive or inquiry below. Examples:\033[0m")
    print("  \033[90m• improve <file>      (e.g., 'improve core/storage.py')\033[0m")
    print("  \033[90m• audit <file>        (e.g., 'audit server.py')\033[0m")
    print("  \033[90m• read <file>         (e.g., 'read core/paths.py')\033[0m")
    print("  \033[90m• list [folder]       (e.g., 'list core')\033[0m")
    print("  \033[90m• Natural language: 'J.A.R.V.I.S., rewrite and improve all files'\033[0m\n")
    
    # Initial greeting
    initial_greeting = "Good day, Sir. J.A.R.V.I.S. is online with full file access and fleet command authority. What are your orders?"
    print(f"\033[96m[J.A.R.V.I.S.]\033[0m ", end="")
    print_typewriter(initial_greeting)
    
    while True:
        try:
            user_input = input("\n\033[92mSir > \033[0m").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit", "bye", "goodbye"):
                farewell = "Standing by, Sir. Have a splendid day."
                print(f"\033[96m[J.A.R.V.I.S.]\033[0m {farewell}")
                speak_local(farewell)
                break
            
            if user_input.lower() in ("clear", "cls"):
                os.system("cls" if os.name == "nt" else "clear")
                print("\033[96m" + BANNER + "\033[0m")
                continue

            # Direct File Engine Shortcuts
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1].strip() if len(parts) > 1 else ""

            if cmd == "read" and arg:
                res = jarvis_file_engine.read_file(arg, max_lines=80)
                if res.get("success"):
                    print(f"\033[94m--- {arg} ({res['total_lines']} lines) ---\033[0m")
                    print(res.get("content", ""))
                    if res.get("truncated"):
                        print("\033[90m[Output truncated at 80 lines]\033[0m")
                else:
                    print(f"\033[91m[-] {res.get('error')}\033[0m")
                continue

            if cmd == "improve" and arg:
                print(f"\033[90m[J.A.R.V.I.S. is refactoring and improving {arg}...]\033[0m")
                res = jarvis_file_engine.improve_file(arg)
                if res.get("success"):
                    print(f"\033[92m✓ Refactored & formatted: {arg} ({res.get('lines_written')} lines written, syntax valid: {res.get('syntax_valid')})\033[0m")
                else:
                    print(f"\033[91m[-] {res.get('error')}\033[0m")
                continue

            if cmd == "audit" and arg:
                res = jarvis_file_engine.audit_file(arg)
                if res.get("success"):
                    issues = res.get("issues", [])
                    print(f"\033[94mAudit for {arg}: {len(issues)} issues found.\033[0m")
                    for iss in issues:
                        print(f"  \033[93m⚠ {iss}\033[0m")
                    if not issues:
                        print("  \033[92m✓ File is 100% clean with valid syntax.\033[0m")
                else:
                    print(f"\033[91m[-] {res.get('error')}\033[0m")
                continue

            if cmd == "list":
                res = jarvis_file_engine.list_files(subpath=arg)
                if res.get("success"):
                    files = res.get("files", [])
                    print(f"\033[94mFound {res.get('total_files')} files in '{arg or 'root'}':\033[0m")
                    for f in files[:25]:
                        print(f"  • {f['path']} ({f['size_bytes']} bytes)")
                    if len(files) > 25:
                        print(f"\033[90m  ...and {len(files) - 25} more files.\033[0m")
                else:
                    print(f"\033[91m[-] {res.get('error')}\033[0m")
                continue

            if cmd == "reports":
                print("\033[90m[J.A.R.V.I.S. is reading workspace reports...]\033[0m")
                rep_res = jarvis_service.read_reports(target=arg if arg else None)
                print(f"\033[94m--- J.A.R.V.I.S. REPORT BRIEFING ---\033[0m")
                print(f"\033[92m{rep_res.get('summary')}\033[0m")
                for rname, rdata in rep_res.get("reports", {}).items():
                    print(f"  \033[93m• {rname}\033[0m: {str(rdata)[:160]}...")
                continue

            if cmd == "stats":
                print("\033[90m[J.A.R.V.I.S. is gathering fleet telemetry...]\033[0m")
                st_res = jarvis_service.get_fleet_stats(agent_manager=manager)
                print(f"\033[94m--- J.A.R.V.I.S. FLEET TELEMETRY ---\033[0m")
                print(f"\033[92mArchitecture: {st_res.get('architecture')}\033[0m")
                print(f"Database: {st_res.get('database', {}).get('engine')} ({st_res.get('database', {}).get('status')}) - {st_res.get('database', {}).get('size_kb')} KB")
                for dname, dinfo in st_res.get("domains", {}).items():
                    print(f"  \033[96m[{dname}]\033[0m {dinfo.get('name')}: {dinfo.get('status')} (Run count: {dinfo.get('run_count')})")
                continue

            if cmd == "revenue":
                print("\033[90m[J.A.R.V.I.S. is auditing financial ledgers and treasury...]\033[0m")
                rev_res = jarvis_service.analyze_revenue()
                print(f"\033[94m--- J.A.R.V.I.S. FINANCIAL & REVENUE INTELLIGENCE ---\033[0m")
                print(f"\033[92m{rev_res.get('summary')}\033[0m\n")
                inv = rev_res.get("invoices", {})
                print(f"  \033[93m• Invoices Ledger\033[0m: {inv.get('total_invoices')} total ({inv.get('paid_count')} paid, {inv.get('pending_count')} pending)")
                print(f"    - MUR Billed: Rs {inv.get('mur_invoiced', 0):,.2f} | Collected: Rs {inv.get('mur_collected', 0):,.2f} | Outstanding: Rs {inv.get('mur_pending', 0):,.2f}")
                print(f"    - USD Billed: ${inv.get('usd_invoiced', 0):,.2f} | Collected: ${inv.get('usd_collected', 0):,.2f}")
                tr = rev_res.get("treasury", {})
                print(f"  \033[93m• Sovereign Treasury\033[0m: ${tr.get('balance_usdc', 0):.2f} USDC ({tr.get('network')}) | Vault: {tr.get('vault_status')}")
                bp = rev_res.get("blueprints", {})
                print(f"  \033[93m• Revenue Blueprints\033[0m: {bp.get('ready_count')}/{bp.get('total_blueprints')} ready to execute in Mauritius")
                continue
            
            print("\033[90m[J.A.R.V.I.S. is processing telemetry...]\033[0m")
            res = jarvis_service.chat(user_message=user_input, voice_mode=True, agent_manager=manager)
            
            reply = res.get("reply", "")
            action = res.get("action_taken")
            
            if action:
                print(f"\033[93m⚡ [FLEET PROTOCOL EXECUTED]: {action}\033[0m")
            
            print(f"\033[96m[J.A.R.V.I.S.]\033[0m ", end="")
            print_typewriter(reply)
            
            # Speak if speech is supported
            speak_local(reply)
            
        except (KeyboardInterrupt, EOFError):
            print("\n\033[96m[J.A.R.V.I.S.]\033[0m Systems standing down. Power levels nominal.")
            break

if __name__ == "__main__":
    main()
