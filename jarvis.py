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

def main():
    print("\033[96m" + BANNER + "\033[0m")
    
    # Initialize Agent Manager for live fleet commands
    manager = AgentManager()
    manager.discover_plugins("agents")
    
    status = jarvis_service.get_system_context(agent_manager=manager)
    print(f"\033[90m[TELEMETRY] Arc Reactor: {status.get('power_level')} | Time: {status.get('current_time')}\033[0m")
    print(f"\033[90m[TELEMETRY] Fleet: {status.get('fleet_scale')} | Defense: {status.get('defense_shields')}\033[0m")
    print("\033[33mType your directive or inquiry below. Type 'exit' or 'quit' to conclude.\033[0m\n")
    
    # Initial greeting
    initial_greeting = "Good day, Sir. J.A.R.V.I.S. is online and at your service. All fleet telemetry is nominal. What are your orders?"
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
