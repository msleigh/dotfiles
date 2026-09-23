#!/usr/bin/env python3
"""Search TMDB and print Jellyfin-relevant provider IDs as JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.themoviedb.org/3"


def request_json(path: str, params: dict[str, str] | None = None) -> dict:
    token = os.environ.get("TMDB_API_READ_ACCESS_TOKEN") or os.environ.get("TMDB_BEARER_TOKEN")
    api_key = os.environ.get("TMDB_API_KEY")
    if not token and not api_key:
        raise RuntimeError(
            "Set TMDB_API_READ_ACCESS_TOKEN (preferred), TMDB_BEARER_TOKEN, "
            "or TMDB_API_KEY."
        )

    query = dict(params or {})
    headers = {"Accept": "application/json", "User-Agent": "transfer-iplayer-media/1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        query["api_key"] = api_key or ""

    url = f"{BASE}{path}?{urllib.parse.urlencode(query)}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        # Do not include the URL: it may contain a v3 API key.
        detail = error.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"TMDB returned HTTP {error.code}: {detail}") from None
    except urllib.error.URLError as error:
        raise RuntimeError(f"Could not contact TMDB: {error.reason}") from None


def search(kind: str, query: str, year: int | None, limit: int) -> list[dict]:
    params = {"query": query, "include_adult": "false", "language": "en-GB"}
    if year:
        params["primary_release_year" if kind == "movie" else "first_air_date_year"] = str(year)
    results = request_json(f"/search/{kind}", params).get("results", [])[:limit]
    output = []
    for item in results:
        tmdb_id = item.get("id")
        external = request_json(f"/{kind}/{tmdb_id}/external_ids") if tmdb_id else {}
        imdb_id = external.get("imdb_id")
        date = item.get("release_date") if kind == "movie" else item.get("first_air_date")
        title = item.get("title") if kind == "movie" else item.get("name")
        original_title = item.get("original_title") if kind == "movie" else item.get("original_name")
        output.append(
            {
                "media_type": kind,
                "title": title,
                "original_title": original_title,
                "year": date[:4] if date else None,
                "tmdb_id": tmdb_id,
                "imdb_id": imdb_id,
                "jellyfin_provider_tag": (
                    f"[imdbid-{imdb_id}]" if imdb_id else f"[tmdbid-{tmdb_id}]"
                ),
                "popularity": item.get("popularity"),
                "overview": item.get("overview"),
            }
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--kind", choices=("movie", "tv", "all"), default="all")
    parser.add_argument("--year", type=int)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 20:
        parser.error("--limit must be between 1 and 20")

    kinds = ("movie", "tv") if args.kind == "all" else (args.kind,)
    try:
        results = [item for kind in kinds for item in search(kind, args.query, args.year, args.limit)]
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
