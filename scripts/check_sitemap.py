#!/usr/bin/env python3
"""Check sitemap page availability using only Python's standard library."""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path

MAX_XML_BYTES = 10 * 1024 * 1024
NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def origin(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Expected an absolute HTTP(S) URL: " + url)
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs containing credentials are not supported")
    return (parsed.scheme, parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sitemap", help="Absolute URL of a sitemap or sitemap index")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between requests")
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--max-sitemaps", type=int, default=50)
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    import math
    if (not math.isfinite(args.timeout) or not math.isfinite(args.delay)
            or args.timeout <= 0 or args.delay < 0 or args.max_pages < 1 or args.max_sitemaps < 1):
        parser.error("Timeout and limits must be positive; delay must be nonnegative and finite")
    try:
        scope = origin(args.sitemap)
    except ValueError as exc:
        parser.error(str(exc))

    errors, results = [], []
    pending = deque([args.sitemap])
    seen_maps, seen_pages = set(), set()

    def request(url):
        time.sleep(args.delay)
        return urllib.request.urlopen(urllib.request.Request(
            url, headers={"User-Agent": "OtterplayTools/1.0 (sitemap availability checker)"}
        ), timeout=args.timeout)

    def record_error(message):
        errors.append(message)
        print("ERROR " + message)

    while pending:
        url = pending.popleft()
        if url in seen_maps:
            continue
        if len(seen_maps) >= args.max_sitemaps:
            record_error("Sitemap limit reached; check is incomplete")
            break
        seen_maps.add(url)
        try:
            with request(url) as response:
                data = response.read(MAX_XML_BYTES + 1)
                if response.geturl() != url:
                    record_error("Sitemap redirected: {} -> {}".format(url, response.geturl()))
            if len(data) > MAX_XML_BYTES:
                raise ValueError("Sitemap exceeds 10 MiB")
            root = ET.fromstring(data)
            if root.tag not in (NAMESPACE + "sitemapindex", NAMESPACE + "urlset"):
                raise ValueError("Expected sitemap namespace and sitemapindex or urlset root")
            is_index = root.tag == NAMESPACE + "sitemapindex"
            entries = root.findall(NAMESPACE + ("sitemap" if is_index else "url"))
            if not entries:
                raise ValueError("Sitemap contains no entries")
            for entry in entries:
                loc = entry.find(NAMESPACE + "loc")
                target = (loc.text or "").strip() if loc is not None else ""
                try:
                    if origin(target) != scope:
                        raise ValueError("Cross-origin entry: " + target)
                except ValueError as exc:
                    record_error("{}: {}".format(url, exc))
                    continue
                if is_index:
                    if target not in seen_maps:
                        pending.append(target)
                elif target not in seen_pages:
                    seen_pages.add(target)
        except (OSError, ValueError, ET.ParseError) as exc:
            record_error("{}: {}".format(url, exc))

    if len(seen_pages) > args.max_pages:
        record_error("Page limit reached; checking {} of {} discovered pages".format(
            args.max_pages, len(seen_pages)))
    for url in sorted(seen_pages)[:args.max_pages]:
        result = {"url": url}
        try:
            with request(url) as response:
                result.update(status=response.status, final_url=response.geturl())
            result["result"] = ("REDIRECT" if result["final_url"] != url else
                                "OK" if 200 <= result["status"] < 300 else "ERROR")
        except (OSError, ValueError) as exc:
            result.update(result="ERROR", error=str(exc))
            if isinstance(exc, urllib.error.HTTPError):
                result["status"] = exc.code
                exc.close()
        results.append(result)
        print("{} {} {}".format(result["result"], result.get("status", "-"), url))

    failed = bool(errors) or any(item["result"] != "OK" for item in results)
    report = {"sitemap": args.sitemap, "sitemaps_read": len(seen_maps),
              "pages_discovered": len(seen_pages), "pages_checked": len(results),
              "passed": not failed, "errors": errors, "pages": results}
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            record_error("Could not write report: " + str(exc))
            failed = True
    print("Checked {} pages across {} sitemaps: {}".format(
        len(results), len(seen_maps), "issues found" if failed else "passed"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
