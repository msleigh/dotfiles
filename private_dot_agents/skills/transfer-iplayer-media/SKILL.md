---
name: transfer-iplayer-media
description: Identify, rename, and safely transfer movies and TV programmes downloaded by get_iplayer from ~/iPlayer/TV to the Jellyfin libraries at /Volumes/Media/Movies and /Volumes/Media/TV. Use when Michael asks to import, move, file, organise, or transfer iPlayer downloads to the media server, or to fix Jellyfin naming for those downloads.
compatibility: macOS; requires the Media NAS mounted at /Volumes/Media and standard shell tools. Optional TMDB credentials improve metadata matching.
---

# Transfer iPlayer Media

## Purpose

Move completed get_iplayer video downloads from `~/iPlayer/TV` into the Jellyfin
library on `/Volumes/Media`. Identify each title first, then use Jellyfin-compatible
names and the conventions already established in this library.

Read [references/jellyfin-layout.md](references/jellyfin-layout.md) for detailed naming
rules. Read [references/metadata.md](references/metadata.md) when identifying a title or
using TMDB.

## Fixed locations

- Staging: `~/iPlayer/TV`
- Movies: `/Volumes/Media/Movies`
- TV: `/Volumes/Media/TV`
- Rsync transfer ledger: `~/iPlayer/.rsync-transferred.exclude`
- Jellyfin: `JELLYFIN_URL` from `~/.extra` (currently `http://pi01.local:8096`)

Do not use this skill for `~/iPlayer/Radio` unless Michael explicitly extends the task.
Never print, log, or pass `JELLYFIN_API_KEY` as a command-line argument.

## Safety contract

- Treat staging and NAS media as user data. Never overwrite, merge, rename, or delete an
  existing NAS item without explicit approval.
- Start read-only. Confirm that `/Volumes/Media` is currently an active NAS mount, inventory
  staging, inspect any matching destination, and check `pgrep -af get_iplayer`.
- The NAS share is not always mounted. If the mount check fails, stop and ask Michael to
  mount it. Never create `/Volumes/Media`, mount the share, or fall back to local storage.
- Do not transfer an active or incomplete download. `.dash.m4a`, `.video.m4v`, `.txt`,
  `.partial`, and similar fragments indicate work in progress. If uncertain, stop and ask.
- Present the proposed source, identification, destination, and final name before writing.
  Resolve ambiguous metadata with Michael. Do not choose merely because it is the first
  search result.
- A request to transfer media permits the agreed file operation, but not unrelated library
  cleanup. Point out nearby inconsistencies and leave them unchanged unless asked.
- Copy to a temporary name on the NAS, verify the copy, atomically rename it to the final
  name, and only then remove the staging source. Never use a blind cross-volume `mv`.
- Preserve the original extension. Do not transcode, remux, or alter media streams unless
  explicitly asked.

## Workflow

1. **Preflight**
   - Verify with the system mount table that `/Volumes/Media` is an active NAS filesystem,
     then verify `/Volumes/Media/Movies` and `/Volumes/Media/TV` are writable directories.
     Directory existence alone is not proof that the share is mounted.
   - If absent, stop without creating directories or moving data and tell Michael to mount
     the share manually.
   - Check free space with `df -h /Volumes/Media`.
   - List staging files with sizes and inspect running get_iplayer processes.
   - Group get_iplayer fragments by basename/PID. Process only completed final media files.

2. **Inspect and identify**
   - Extract the BBC PID from the source name when present, but never use it as a Jellyfin
     provider ID.
   - Inspect embedded tags and duration with `ffprobe`; use get_iplayer/BBC metadata when
     available.
   - Decide whether the provider catalogues the item as a movie or a TV series/episode.
     A one-off BBC programme is not automatically a movie.
   - Search TMDB when needed with `scripts/search_tmdb.py`. Prefer an unambiguous IMDb ID
     for the library tag; fall back to a TMDB ID when IMDb is unavailable.
   - Confirm the exact title, year, media type, and, for TV, provider season/episode number.

3. **Follow the existing house style**
   - Movie directory and video basename:
     `Title (Year) [imdbid-tt1234567]`
   - Series directory:
     `Series Title (Year) [imdbid-tt1234567]`
   - Season directory: `Season 01` (specials use `Season 00` only when provider metadata
     confirms the special number).
   - Episode basename:
     `Series Title S01E02 - Episode Title`
   - If IMDb has no ID, use `[tmdbid-12345]`. Omit a provider tag only after a real search
     found no reliable match, and say so.
   - Use the provider's canonical display title and release/first-air year. Remove filesystem
     forbidden characters while keeping natural spaces and punctuation.

4. **Plan and confirm**
   - Show a concise table: source, detected type, metadata match and IDs, destination, and
     any sidecars.
   - Flag collisions, an existing series folder with a different ID/year, non-standard
     layout, multiple candidate matches, or uncertain episode numbering.
   - Ask for confirmation before the first copy. One confirmation can cover a clearly
     listed batch.

5. **Transfer safely**
   - Create only the agreed title/season directories.
   - Copy each video with `rsync --archive --protect-args --progress` to a unique temporary
     filename in the final destination directory (for example `.incoming-<filename>`).
   - Compare source and temporary copy sizes, then compare SHA-256 digests with
     `shasum -a 256`. A checksum is required before source deletion.
   - Rename the verified temporary file to the final basename without overwriting anything.
   - Transfer recognised artwork only when useful, naming it with Jellyfin conventions such
     as `poster.jpg`. Ignore temporary get_iplayer `.txt` fragment files. Do not create NFO
     files unless requested.
   - Remove only the verified staging source and its clearly associated temporary remnants.
     Never remove an unrelated source file.
   - After the NAS checksum passes and the staging source is removed, record its source-root
     relative pattern in `~/iPlayer/.rsync-transferred.exclude`. Anchor it with `/`, preserve
     the exact directory and basename, and use a final `.*` only to cover that programme's
     media/artwork extensions. Do not add broad shared-directory exclusions, duplicates,
     unverified files, or incomplete downloads. This prevents later pulls from `vns` from
     restoring transferred staging files while retaining the remote copy as a fallback.

6. **Refresh Jellyfin**
   - After a successful, checksum-verified transfer, run
     `bash scripts/refresh_jellyfin.sh refresh`. The helper must check the `Scan Media
     Library` task first and skip the request when a scan is already running.
   - Use `bash scripts/refresh_jellyfin.sh status` to inspect scan progress and
     `bash scripts/refresh_jellyfin.sh search "Title"` to confirm the new item and provider
     IDs after the scan.
   - The helper loads `JELLYFIN_URL` and `JELLYFIN_API_KEY` from `~/.extra` and passes the
     key to `curl` on standard input, keeping it out of process arguments and output. Never
     store the key in this skill.
   - A refresh failure does not invalidate a verified media copy. Report it and leave the
     transferred file in place.

7. **Validate and report**
   - List the final destination and run `ffprobe` on the destination file.
   - Confirm source removal, final path, byte size, checksum, provider match, Jellyfin scan
     result, and any files intentionally left in staging.
   - Report library inconsistencies observed during the task, but do not repair them unless
     requested.

## Existing-library observations

The newer and preferred entries already follow the year/provider-ID style above. Older
content is mixed: some movie folders omit year and provider ID, some movie video basenames
do not match their folder, and some TV episodes sit directly in the series root rather than
`Season NN`. Treat those as legacy inconsistencies, not as patterns to copy.
