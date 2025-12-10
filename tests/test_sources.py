import sys
from datetime import timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from aggregator import collect_events
from sources.fis import FisCalendarSource
from sources.ibu import IbuEventsSource
from sources.svff import SvffFixturesSource


def load_all_events():
    data_dir = PROJECT_ROOT / "data"
    sources = [
        SvffFixturesSource(data_dir / "svff_fixture_sample.json"),
        IbuEventsSource(data_dir / "ibu_events_sample.json"),
        FisCalendarSource(data_dir / "fis_events_sample.json"),
    ]
    events = collect_events(sources)
    return events


def test_svff_events_have_two_fixtures():
    events = load_all_events()
    football_events = [e for e in events if e.sport == "football"]
    assert len(football_events) == 2
    assert football_events[0].event_name == "AIK vs Djurgården"


def test_biathlon_events_are_utc_sorted():
    events = load_all_events()
    biathlon_events = [e for e in events if e.sport == "biathlon"]
    utc_times = [e.start_time_utc for e in biathlon_events]
    assert utc_times == sorted(utc_times)
    for e in biathlon_events:
        assert e.start_time_utc.tzinfo == timezone.utc


def test_fis_events_have_locations_and_timezone():
    events = load_all_events()
    fis_events = [e for e in events if e.source == "FIS sample"]
    assert len(fis_events) == 2
    assert all(e.location for e in fis_events)
    assert any(e.local_timezone == "Europe/Stockholm" for e in fis_events)
