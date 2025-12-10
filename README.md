# sports

Prototype aggregator for Swedish football and winter sports events using sample JSON payloads.

## Structure
- `aggregate.py` – CLI to aggregate sample events into `events.json`.
- `src/` – core library: event schema, aggregation helpers, and source parsers.
- `data/` – sample payloads approximating SvFF fixtures, IBU biathlon events, and FIS calendars.
- `tests/` – basic parsing and timezone tests.

## Usage
Run the CLI to produce a merged events file:

```bash
python aggregate.py --output events.json
```

## Testing
```bash
python -m pytest
```
