from typing import Dict, Any, List
from datetime import datetime
from core.base_agent import BaseAgent
from agents.meeting_assistant.subagents import (
    CalendarEventAuditorSubAgent,
    ScheduleConflictDetectorSubAgent,
    DailyAgendaCompilerSubAgent
)

class MeetingAssistantAgent(BaseAgent):
    """
    Employee #2: Calendar & Meeting Scheduler Coordinator
    Audits incoming calendar invites, detects scheduling conflicts, and prepares daily agenda briefings.
    """
    def __init__(self):
        super().__init__(
            agent_id="meeting_assistant",
            name="Meeting & Calendar Coordinator",
            description="Analyzes incoming calendar invites, detects scheduling conflicts, and prepares daily agenda briefings.",
            icon="calendar",
            schedule_minutes=120
        )
        self.stats = {
            "invites_reviewed": 14,
            "conflicts_resolved": 3,
            "briefings_prepared": 5
        }
        self.config = {
            "CALENDAR_PROVIDER": "Google Calendar",
            "AUTO_DECLINE_CONFLICTS": False,
            "BUFFER_MINUTES_BETWEEN_MEETINGS": 15,
            "BRIEFING_TIME": "08:30"
        }

        # Register specialized single-task subagents
        self.register_subagent(CalendarEventAuditorSubAgent())
        self.register_subagent(ScheduleConflictDetectorSubAgent())
        self.register_subagent(DailyAgendaCompilerSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "CALENDAR_PROVIDER",
                "label": "Calendar Service Provider",
                "type": "text",
                "default": "Google Calendar",
                "description": "Provider service (e.g. Google Calendar, Outlook, Apple)"
            },
            {
                "key": "BUFFER_MINUTES_BETWEEN_MEETINGS",
                "label": "Buffer Minutes Between Meetings",
                "type": "number",
                "default": 15,
                "description": "Minimum focus buffer time between back-to-back calls"
            },
            {
                "key": "AUTO_DECLINE_CONFLICTS",
                "label": "Auto-Decline Double Bookings",
                "type": "boolean",
                "default": False,
                "description": "Automatically decline conflicting invites with a polite note"
            },
            {
                "key": "BRIEFING_TIME",
                "label": "Daily Morning Briefing Time",
                "type": "text",
                "default": "08:30",
                "description": "Time to compile and send daily schedule agenda"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="meeting_assistant/agent.py", message="Calendar coordinator preferences updated", level="SUCCESS")
        return True

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Initialize", file_used="meeting_assistant/agent.py", message="Beginning calendar audit for next 48 hours via subagents...", level="INFO")
        
        # Subagent 1: Audit Calendar Events
        audit_res = self.run_subagent(
            "meeting_calendar_auditor",
            {
                "provider": self.config.get("CALENDAR_PROVIDER", "Google Calendar"),
                "window_hours": 48
            }
        )
        events = audit_res.get("events", [])
        self.stats["invites_reviewed"] += len(events)

        # Subagent 2: Detect Conflicts
        conflict_res = self.run_subagent(
            "meeting_conflict_detector",
            {
                "events": events,
                "buffer_minutes": int(self.config.get("BUFFER_MINUTES_BETWEEN_MEETINGS", 15))
            }
        )
        if conflict_res.get("conflicts_found", 0) > 0:
            self.stats["conflicts_resolved"] += conflict_res.get("conflicts_found", 0)

        # Subagent 3: Compile Daily Agenda Briefing
        agenda_res = self.run_subagent(
            "meeting_agenda_compiler",
            {"events": events}
        )
        self.stats["briefings_prepared"] += 1

        self.log(step="Audit Result", file_used="meeting_assistant/agent.py", message=f"Audited {len(events)} events: {conflict_res.get('conflicts_found')} conflicts found. Briefing ready.", level="SUCCESS")

        return {
            "status": "Completed Calendar Audit",
            "calendar_audit": audit_res,
            "conflict_audit": conflict_res,
            "agenda": agenda_res
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Invites Audited", "value": self.stats["invites_reviewed"], "color": "blue"},
            {"title": "Conflicts Fixed", "value": self.stats["conflicts_resolved"], "color": "yellow"},
            {"title": "Briefings Sent", "value": self.stats["briefings_prepared"], "color": "green"}
        ]
