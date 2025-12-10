from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Event:
    sport: str
    competition: str
    event_name: str
    participants: List[str]
    start_time_utc: datetime
    local_timezone: str
    location: str
    source: str
    url: Optional[str] = None
    broadcast: Optional[str] = None
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "sport": self.sport,
            "competition": self.competition,
            "event_name": self.event_name,
            "participants": self.participants,
            "start_time_utc": self.start_time_utc.isoformat(),
            "local_timezone": self.local_timezone,
            "location": self.location,
            "source": self.source,
            "url": self.url,
            "broadcast": self.broadcast,
        }
