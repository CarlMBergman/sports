from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional

from events import Event
from sources.base import EventSource


class SvffFixturesSource(EventSource):
    """Parse sample SvFF fixtures JSON used by Allsvenskan/Damallsvenskan/Superettan."""

    def __init__(self, fixture_path: Path, competition: Optional[str] = None) -> None:
        self.fixture_path = fixture_path
        self.competition = competition

    def load(self) -> Iterable[Event]:
        payload = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        fixtures: List[dict] = payload.get("data", [])

        for fixture in fixtures:
            competition = self.competition or fixture.get("competition", "Unknown Competition")
            start = fixture.get("startDate")
            if not start:
                continue
            start_dt = datetime.fromisoformat(start)
            start_utc = start_dt.astimezone(timezone.utc)

            home = fixture.get("homeTeam", {}).get("name", "Home")
            away = fixture.get("awayTeam", {}).get("name", "Away")
            event_name = f"{home} vs {away}"

            yield Event(
                sport="football",
                competition=competition,
                event_name=event_name,
                participants=[home, away],
                start_time_utc=start_utc,
                local_timezone=start_dt.tzinfo.tzname(start_dt) if start_dt.tzinfo else "UTC",
                location=fixture.get("venue", ""),
                source="SvFF sample",
                url=fixture.get("url"),
                broadcast=fixture.get("tvChannel"),
                raw=fixture,
            )
