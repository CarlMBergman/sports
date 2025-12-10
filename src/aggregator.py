from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from events import Event
from sources.base import EventSource


def collect_events(sources: Iterable[EventSource]) -> List[Event]:
    events: List[Event] = []
    for source in sources:
        events.extend(source.list())
    return events


def export_events_to_json(events: List[Event], output_path: Path) -> None:
    payload = [event.to_dict() for event in events]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
