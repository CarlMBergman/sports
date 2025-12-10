from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from events import Event
from sources.base import EventSource


class IbuEventsSource(EventSource):
    """Parse sample IBU biathlon events JSON."""

    def __init__(self, events_path: Path) -> None:
        self.events_path = events_path

    def load(self) -> Iterable[Event]:
        payload = json.loads(self.events_path.read_text(encoding="utf-8"))
        for event in payload.get("events", []):
            start_raw = event.get("startTime")
            if not start_raw:
                continue
            local_dt = datetime.fromisoformat(start_raw)
            start_utc = local_dt.astimezone(timezone.utc)

            yield Event(
                sport="biathlon",
                competition=event.get("category", "IBU Event"),
                event_name=event.get("description", "Biathlon event"),
                participants=[],
                start_time_utc=start_utc,
                local_timezone=local_dt.tzinfo.tzname(local_dt) if local_dt.tzinfo else "UTC",
                location=event.get("location", ""),
                source="IBU sample",
                url=event.get("url"),
                broadcast=event.get("broadcast"),
                raw=event,
            )
