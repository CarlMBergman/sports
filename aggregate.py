from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from aggregator import collect_events, export_events_to_json
from sources.fis import FisCalendarSource
from sources.ibu import IbuEventsSource
from sources.svff import SvffFixturesSource


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate sample Swedish sports events")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_ROOT / "data",
        help="Directory containing sample JSON files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("events.json"),
        help="Where to write aggregated events JSON",
    )
    args = parser.parse_args()

    data_dir: Path = args.data_dir
    sources = [
        SvffFixturesSource(data_dir / "svff_fixture_sample.json"),
        IbuEventsSource(data_dir / "ibu_events_sample.json"),
        FisCalendarSource(data_dir / "fis_events_sample.json"),
    ]

    events = collect_events(sources)
    export_events_to_json(events, args.output)
    print(f"Wrote {len(events)} events to {args.output}")


if __name__ == "__main__":
    main()
