from datetime import datetime, timedelta
from typing import Dict, Any, List
from core.subagent import BaseSubAgent

class CalendarEventAuditorSubAgent(BaseSubAgent):
    """
    Subagent 1: Syncs and audits upcoming calendar events across a rolling time window.
    """
    def __init__(self):
        super().__init__(
            subagent_id="meeting_calendar_auditor",
            name="Calendar Event Auditor SubAgent",
            parent_agent_id="meeting_assistant",
            description="Audits upcoming schedule across Google Calendar/Outlook and standardizes meeting metadata."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        provider = payload.get("provider", "Google Calendar")
        window_hours = payload.get("window_hours", 48)

        now = datetime.now()
        # Simulated events schedule
        events = [
            {
                "id": "evt_101",
                "title": "Eco-Travellounge Architecture Review",
                "start": (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "end": (now + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                "attendees": ["devenpawaray@gmail.com", "tech-lead@eco-travellounge.mu"]
            },
            {
                "id": "evt_102",
                "title": "Med360 Deployment Pre-Flight Sync",
                "start": (now + timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M"),
                "end": (now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
                "attendees": ["devenpawaray@gmail.com", "hospital-ops@med360.mu"]
            }
        ]

        return {
            "provider": provider,
            "window_hours": window_hours,
            "events_count": len(events),
            "events": events
        }


class ScheduleConflictDetectorSubAgent(BaseSubAgent):
    """
    Subagent 2: Scans for overlapping events and enforces inter-meeting focus buffer minutes.
    """
    def __init__(self):
        super().__init__(
            subagent_id="meeting_conflict_detector",
            name="Schedule Conflict Detector SubAgent",
            parent_agent_id="meeting_assistant",
            description="Detects double bookings, overlapping meetings, and buffer time violations between calls."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        events = payload.get("events", [])
        buffer_minutes = payload.get("buffer_minutes", 15)

        conflicts = []
        # Simple interval check
        for i in range(len(events) - 1):
            e1 = events[i]
            e2 = events[i+1]
            try:
                end1 = datetime.strptime(e1["end"], "%Y-%m-%d %H:%M")
                start2 = datetime.strptime(e2["start"], "%Y-%m-%d %H:%M")
                gap_minutes = (start2 - end1).total_seconds() / 60
                if gap_minutes < buffer_minutes:
                    conflicts.append({
                        "event_a": e1["title"],
                        "event_b": e2["title"],
                        "gap_minutes": gap_minutes,
                        "required_buffer": buffer_minutes,
                        "type": "BUFFER_VIOLATION" if gap_minutes >= 0 else "OVERLAP"
                    })
            except Exception:
                pass

        return {
            "conflicts_found": len(conflicts),
            "conflicts": conflicts,
            "schedule_is_clean": len(conflicts) == 0
        }


class DailyAgendaCompilerSubAgent(BaseSubAgent):
    """
    Subagent 3: Generates executive morning schedule briefings.
    """
    def __init__(self):
        super().__init__(
            subagent_id="meeting_agenda_compiler",
            name="Daily Agenda Compiler SubAgent",
            parent_agent_id="meeting_assistant",
            description="Formats and compiles executive daily calendar agenda briefings."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        events = payload.get("events", [])
        date_str = datetime.now().strftime("%A, %d %B %Y")

        agenda_lines = [
            f"📅 *DAILY AGENDA & CALENDAR BRIEF* ({date_str})",
            f"Total Committed Calls: {len(events)}\n"
        ]

        if not events:
            agenda_lines.append("🎉 *Zero calendar commitments today.* Pure deep work & code sprint time!")
        else:
            for ev in events:
                agenda_lines.append(f"• {ev.get('start', '').split(' ')[-1]} - {ev.get('end', '').split(' ')[-1]}: *{ev.get('title')}*")

        agenda_text = "\n".join(agenda_lines)

        return {
            "date": date_str,
            "agenda_text": agenda_text,
            "events_count": len(events)
        }
