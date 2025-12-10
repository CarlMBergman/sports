from __future__ import annotations

import json
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from events import Event
from sources.base import EventSource


class FisCalendarSource(EventSource):
    """Parse sample FIS calendar JSON for cross-country/alpine events."""

    def __init__(self, calendar_path: Path, default_timezone: str = "Europe/Zurich") -> None:
        self.calendar_path = calendar_path
        self.default_timezone = default_timezone

    def load(self) -> Iterable[Event]:
        payload = json.loads(self.calendar_path.read_text(encoding="utf-8"))
        races = payload.get("races", [])

        for race in races:
            date_str = race.get("date")
            time_str = race.get("time")
            if not date_str or not time_str:
                continue
            tz_name = race.get("timezone", self.default_timezone)
            local_zone = ZoneInfo(tz_name)

            local_dt = datetime.combine(
                datetime.fromisoformat(date_str).date(),
                time.fromisoformat(time_str),
                tzinfo=local_zone,
            )
            start_utc = local_dt.astimezone(timezone.utc)

            yield Event(
                sport=race.get("discipline", "winter sport").lower(),
                competition=race.get("competition", "FIS Event"),
                event_name=race.get("name", "FIS race"),
                participants=race.get("athletes", []),
                start_time_utc=start_utc,
                local_timezone=tz_name,
                location=race.get("location", ""),
                source="FIS sample",
                url=race.get("url"),
                broadcast=race.get("broadcast"),
                raw=race,
            )
