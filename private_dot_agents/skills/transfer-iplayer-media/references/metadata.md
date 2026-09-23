# Metadata identification

## Evidence order

1. Inspect the source filename, BBC PID, embedded media tags, duration, and any get_iplayer
   sidecars or history entry.
2. Check BBC programme metadata for the PID when available.
3. Search TMDB for both movie and TV candidates when classification is uncertain.
4. Compare canonical title, original title, year, synopsis, runtime, and episode title.
5. If evidence conflicts or more than one candidate remains plausible, ask Michael.

Never infer a provider match from title alone when remakes or similarly named programmes
exist. Never label a one-off programme as a movie merely because it is a single file.

## TMDB helper

Run relative to this skill directory:

```bash
python3 scripts/search_tmdb.py --kind all --query "Title"
python3 scripts/search_tmdb.py --kind movie --query "Title" --year 2024
python3 scripts/search_tmdb.py --kind tv --query "Series" --year 2024
```

The helper reads one of:

- `TMDB_API_READ_ACCESS_TOKEN` (preferred bearer token)
- `TMDB_BEARER_TOKEN` (alias)
- `TMDB_API_KEY` (v3 API key fallback)

Do not print, paste into commands, commit, or store credentials in the skill. If none of
these variables is configured, ask Michael to expose one in his machine-local secret
configuration. The helper emits candidate metadata and retrieves IMDb IDs through TMDB's
external-ID endpoint.

## Selecting a result

A high-confidence result agrees on media type, canonical title, year, synopsis/subject,
and approximate runtime or episode context. State the chosen result and alternatives.
Prefer `[imdbid-...]` in the destination name when TMDB returns a valid IMDb ID. Otherwise
use `[tmdbid-...]`. If no reliable provider entry exists, omit the tag rather than adding a
wrong identifier.
