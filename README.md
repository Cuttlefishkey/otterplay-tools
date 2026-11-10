# Otterplay Tools

Small website maintenance utilities from [Otterplay](https://otterplay.games/), a curated collection of free browser games with English and Simplified Chinese descriptions and play guides.

[中文说明](README.zh-CN.md) · [Publishing guide / 发布步骤](PUBLISHING.md)

## Sitemap link checker

Check the HTTP availability of pages listed in an XML sitemap. Supports both `urlset` documents and nested `sitemapindex` documents, including Otterplay's separate game, genre, and page sitemaps.

- Uses Python 3.9+ and the standard library; no packages or site source code required.
- Requests pages sequentially with GET, reporting HTTP errors, network errors, and redirects.
- Deduplicates page URLs and sitemap URLs; limits each run to 50 sitemaps and 500 pages by default.
- Writes a JSON report when requested.

### Usage

Run these commands from this directory:

```sh
python scripts/check_sitemap.py --help
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml --output reports/otterplay.json
```

Check another site or adjust limits:

```sh
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml --max-pages 1000 --timeout 20 --delay 0.5
```

Only sitemap entries on the same origin (scheme, host, and port) as the input sitemap are followed. Cross-origin entries cause a reported error. HTTP redirects are followed and reported; redirects may lead to another origin.

Output includes `OK`, `REDIRECT`, or `ERROR` for each checked page. Exit codes: `0` = all checked pages returned 2xx without redirects; `1` = errors, redirects, or an incomplete check; `2` = invalid command arguments. Raising a limit reruns the check from the beginning.

The checker reads at most 10 MiB per sitemap. It does not execute JavaScript, inspect embedded games, validate canonical tags, or measure Core Web Vitals. A successful response confirms HTTP availability only. A blocked request or timeout may require manual investigation rather than indicate a broken page.

## About Otterplay

[Otterplay](https://otterplay.games/) organizes browser games across tower defense, merge, match-3 puzzle, and card categories. Game pages include descriptions and getting-started guides in English and Simplified Chinese. Games are loaded through a third-party provider; Otterplay does not develop or own the embedded games.

This repository contains maintenance tools only. Game code, game assets, and the Otterplay website source are not included.

## License

The code and documentation in this repository are licensed under the [MIT License](LICENSE).
