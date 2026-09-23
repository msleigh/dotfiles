# Jellyfin naming reference

Official documentation:

- Movies: <https://jellyfin.org/docs/general/server/media/movies/>
- Shows: <https://jellyfin.org/docs/general/server/media/shows/>
- Provider identifiers: <https://jellyfin.org/docs/general/server/metadata/identifiers/>

## Movies

Use one directory per film. Keep the directory and primary video basename identical:

```text
Movies/
└── Movie Name (2024) [imdbid-tt1234567]/
    └── Movie Name (2024) [imdbid-tt1234567].mp4
```

Jellyfin permits optional year and provider IDs, but this library's preferred house style
includes both whenever they can be identified reliably. Multiple versions must begin with
the exact folder name and then use a Jellyfin-supported separator and label.

## Shows

```text
TV/
└── Series Name (2024) [imdbid-tt1234567]/
    └── Season 01/
        └── Series Name S01E02 - Episode Title.mp4
```

- Use `Season NN`, zero-padded.
- Do not place normal episode files in the series root.
- Match season and episode numbers to the selected metadata provider.
- Put confirmed specials in `Season 00`. Do not invent special numbers.
- For a file containing multiple consecutive episodes, Jellyfin accepts `S01E01-E02`, but
  splitting it into individual episodes is preferred.
- For one logical item split across files, supported stacking labels include `-cd1`,
  `-disc1`, and `-part-1`. Do not use stacking labels for separately catalogued episodes.

## Provider IDs

Preferred local spelling:

- `[imdbid-tt9362722]`
- `[tmdbid-569094]` when no IMDb ID is available

Jellyfin also supports TVDB and alternate delimiters/aliases. The BBC PID in a get_iplayer
filename is useful provenance, but it is not a Jellyfin metadata-provider ID.

## Artwork and invalid characters

Use recognised artwork names such as `poster.jpg` and `backdrop.jpg`. Avoid filesystem
reserved characters: `< > : " / \ | ? *`. Do not copy download fragments or incidental
text files into the library.
