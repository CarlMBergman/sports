# Data source plan: Swedish athletes schedules (priority: winter sports + football)

## Goals
- Identify reliable API or scrapeable feeds for upcoming events featuring Swedish athletes.
- Normalize data into a common event schema for aggregation.
- Start with football (men/women domestic leagues, national teams) and winter sports (cross-country, biathlon, alpine, ski jumping, snowboard/freestyle, bandy, ice hockey for domestic leagues) before expanding to other sports.

## Football sources (highest priority)
1. **Svenska Fotbollförbundet (SvFF) public JSON endpoints**
   - Used by allsvenskan.se, superettan.se, damallsvenskan.se sites; inspect network calls for fixtures and tables.
   - Expected fields: match id, competition, home/away teams, kickoff (UTC/local), venue, TV/stream info, status.
   - Actions: capture example fixture endpoint for Allsvenskan/Damallsvenskan/Superettan; confirm rate limits and if CORS allows server-side fetch.
2. **UEFA APIs for Swedish national teams and clubs**
   - Nations League/Euro qualifiers/Champions League data available via public JSON used on UEFA.com.
   - Actions: capture fixtures endpoints for Sweden men/women, plus major club competitions where Swedish teams participate.
3. **Fallback commercial APIs**
   - Options: API-Football (RapidAPI), TheSportsDB, LiveScore API, Sportradar (licensed).
   - Actions: evaluate free tier coverage for Swedish leagues; note licensing constraints for redistribution.

## Winter sports sources (priority focus)
1. **FIS (cross-country, alpine, ski jumping, snowboard/freestyle)**
   - FIS event calendar endpoints often exposed as JSON under `data.fis-ski.com` with competition codes.
   - Actions: identify endpoints for World Cup/Continental Cup events; extract athlete start lists and start times; normalize to UTC.
2. **IBU Biathlon**
   - Public JSON APIs used on biathlonworld.com (e.g., `api.biathlonresults.com` for events, start lists, results).
   - Actions: locate upcoming event list endpoint; capture start times, disciplines, athlete entries; check rate limits/ToS.
3. **SHL/HockeyAllsvenskan (ice hockey)**
   - League sites expose JSON fixtures via their web frontends.
   - Actions: inspect network calls for schedule endpoints; map fields (gameId, teams, arena, startTime, TV/stream info).
4. **Bandy (Elitserien)**
   - Svenska Bandyförbundet site publishes fixtures; likely HTML requiring scraping.
   - Actions: prototype scraper for fixtures page, extracting date/time, teams, venue.
5. **World Cup calendars for sliding sports (luge/bobsleigh/skeleton), speed skating, and curling**
   - Most federation sites expose calendar pages with structured JSON or predictable HTML tables.
   - Actions: select one discipline (e.g., speed skating ISU calendar) to validate scraper approach after FIS/IBU.

## Common schema (applies to all sources)
- `sport`, `competition`, `event_name`, `athletes/teams`, `start_time_utc`, `local_timezone`, `location`, `source`, `url`, `broadcast/stream` (optional).
- Deduplicate by `(sport, competition, start_time_utc, teams/athletes)` and prefer official API data over scraped HTML.

## Next steps (execution order)
1. Capture and document concrete JSON endpoints for SvFF leagues and IBU/FIS calendars; store sample responses.
2. Build minimal fetchers for **Allsvenskan/Damallsvenskan/Superettan** fixtures and **IBU events**; normalize to schema.
3. Add one scraper for **FIS World Cup calendar** if JSON is unavailable; include parsing tests for date/time selectors.
4. Evaluate one commercial fallback (e.g., API-Football free tier) for resilience; record licensing limits.
5. Add monitoring checklist: response codes, last updated timestamps, and source attribution requirements per feed.
