import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any

class TelemetryBus:
    """
    Central Real-Time Event Bus:
    Broadcasts step-by-step agent telemetry, file accesses,
    and decisions to connected web dashboard clients via SSE.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelemetryBus, cls).__new__(cls)
            cls._instance.subscribers: List[asyncio.Queue] = []
            cls._instance.history: List[Dict[str, Any]] = []
        return cls._instance

    def emit(self, agent_id: str, agent_name: str, step: str, file_used: str, message: str, level: str = "INFO"):
        """
        Emits an event into the history and pushes to all active web subscribers.
        """
        event = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "agent_id": agent_id,
            "agent_name": agent_name,
            "step": step,
            "file_used": file_used,
            "message": message,
            "level": level.upper()  # INFO, ACTION, LLM, SUCCESS, WARN, ERROR
        }

        # Keep last 200 events in memory
        self.history.append(event)
        if len(self.history) > 200:
            self.history.pop(0)

        # Broadcast to all async SSE subscriber queues
        dead_queues = []
        for q in self.subscribers:
            try:
                q.put_nowait(event)
            except Exception:
                dead_queues.append(q)

        for dq in dead_queues:
            if dq in self.subscribers:
                self.subscribers.remove(dq)

    def subscribe(self) -> asyncio.Queue:
        """Subscribes an SSE connection to live events."""
        q = asyncio.Queue()
        self.subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        """Removes a disconnected SSE client queue."""
        if q in self.subscribers:
            self.subscribers.remove(q)

    def get_recent_history(self) -> List[Dict[str, Any]]:
        return self.history[-40:]

telemetry = TelemetryBus()
