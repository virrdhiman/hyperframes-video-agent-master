#!/usr/bin/env python3
"""
Download usable Remotion resources from a DOCX link directory.

What this script does:
1. Extracts hyperlink text + URL pairs from a DOCX file.
2. Clones GitHub repositories referenced in the doc.
3. Downloads key npm package tarballs for Remotion workflows.
4. Downloads curated Google Fonts (woff2) for local/offline usage.
5. Saves HTML snapshots for reference pages.
6. Tries to discover direct file download links from free pages.
7. Writes machine-readable manifests and a human-readable summary.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

FILE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z",
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
    ".mp3",
    ".wav",
    ".ogg",
    ".flac",
    ".aiff",
    ".json",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".tar",
    ".gz",
    ".tgz",
}

MANUAL_DOMAINS = {
    "storyblocks.com": "paid subscription",
    "pond5.com": "paid marketplace",
    "premiumbeat.com": "manual claim/login",
    "cinepacks.store": "manual checkout",
    "videezy.com": "manual download flow",
    "vecteezy.com": "manual download flow",
    "motionbolt.com": "manual signup/download",
    "ignitemotion.com": "manual download flow",
    "zapsplat.com": "account required",
    "iconscout.com": "manual download flow",
    "lordicon.com": "manual download flow",
    "lottiefiles.com": "manual download flow",
    "finsweet.com": "manual selection/download",
    "gumroad.com": "manual checkout",
    "kenney.itch.io": "manual checkout/download",
    "clippkit.com": "manual signup/download",
    "remotiontemplates.dev": "manual selection/download",
    "elevenlabs.io": "account/API key required",
}

REFERENCE_DOMAINS = {
    "remotion.dev",
    "shadcn.io",
    "ui.aceternity.com",
    "magicui.design",
    "reactbits.dev",
    "vantajs.com",
    "airbnb.io",
    "rive.app",
    "react-svgr.com",
    "unsplash.com",
    "pexels.com",
    "pixabay.com",
    "mixkit.co",
    "freesound.org",
    "kenney.nl",
    "game-icons.net",
    "videvo.net",
}

NPM_PACKAGES = [
    "@remotion/lottie",
    "@remotion/rive",
    "@remotion/google-fonts",
    "remotion-transition-series",
    "remotion-animate-text",
    "three",
    "@react-three/fiber",
    "@react-three/drei",
]

GOOGLE_FONT_FAMILIES = [
    "Inter",
    "Roboto",
    "Montserrat",
    "Poppins",
    "Merriweather",
    "Bebas Neue",
]


@dataclass
class Resource:
    name: str
    url: str


def log(message: str) -> None:
    print(message, flush=True)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "resource"


def domain_of(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().split("@")[-1]
    if host.startswith("www."):
        host = host[4:]
    return host


def extension_from_url(url: str) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    return suffix


def parse_docx_links(docx_path: Path) -> list[Resource]:
    with zipfile.ZipFile(docx_path) as zf:
        rels_xml = ET.fromstring(zf.read("word/_rels/document.xml.rels"))
        doc_xml = ET.fromstring(zf.read("word/document.xml"))

    rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    r_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

    rel_map: dict[str, str] = {}
    for rel in rels_xml.findall(f"{rel_ns}Relationship"):
        rel_type = rel.attrib.get("Type", "")
        if "hyperlink" in rel_type:
            rel_id = rel.attrib.get("Id", "")
            target = rel.attrib.get("Target", "")
            if rel_id and target:
                rel_map[rel_id] = target

    resources: list[Resource] = []
    seen: set[tuple[str, str]] = set()

    for hyperlink in doc_xml.findall(f".//{w_ns}hyperlink"):
        rel_id = hyperlink.attrib.get(r_ns)
        if not rel_id:
            continue

        parts: list[str] = []
        for text_node in hyperlink.findall(f".//{w_ns}t"):
            parts.append(text_node.text or "")
        text = "".join(parts).strip()
        target = rel_map.get(rel_id, "").strip()
        if not text or not target:
            continue

        key = (text, target)
        if key in seen:
            continue
        seen.add(key)
        resources.append(Resource(name=text, url=target))

    return resources


def fetch_bytes(
    url: str,
    timeout: int = 30,
    max_bytes: int = 3_000_000,
) -> tuple[bytes | None, str | None, str | None]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = resp.read(64 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > max_bytes:
                    return None, content_type, "exceeds max snapshot size"
            return b"".join(chunks), content_type, None
    except HTTPError as exc:
        return None, None, f"HTTP {exc.code}"
    except URLError as exc:
        return None, None, f"URL error: {exc.reason}"
    except Exception as exc:  # noqa: BLE001
        return None, None, str(exc)


def download_file(
    url: str,
    dest: Path,
    timeout: int = 45,
    max_bytes: int = 250 * 1024 * 1024,
) -> tuple[bool, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=timeout) as resp:
            content_type = (resp.headers.get("Content-Type", "") or "").lower()
            if content_type.startswith("text/html"):
                return False, "not a direct file (html)"

            content_length = resp.headers.get("Content-Length")
            if content_length:
                try:
                    size = int(content_length)
                    if size > max_bytes:
                        return False, f"too large ({size} bytes)"
                except ValueError:
                    pass

            dest.parent.mkdir(parents=True, exist_ok=True)
            total = 0
            with dest.open("wb") as fh:
                while True:
                    chunk = resp.read(256 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        fh.close()
                        dest.unlink(missing_ok=True)
                        return False, f"aborted (exceeds {max_bytes} bytes)"
                    fh.write(chunk)
            return True, f"downloaded ({total} bytes)"
    except HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except URLError as exc:
        return False, f"URL error: {exc.reason}"
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def save_html_snapshot(url: str, out_path: Path) -> tuple[bool, str]:
    data, content_type, err = fetch_bytes(url=url, max_bytes=5_000_000)
    if err:
        return False, err
    if data is None:
        return False, "no data"
    if "html" not in (content_type or "").lower():
        return False, f"not html ({content_type})"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return True, "snapshot saved"


def extract_download_candidates(html: str, base_url: str) -> list[str]:
    candidates: set[str] = set()
    pattern = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
    for match in pattern.findall(html):
        raw = match.strip()
        if not raw:
            continue
        if raw.startswith(("javascript:", "mailto:", "#")):
            continue
        full = urljoin(base_url, raw)
        parsed = urlparse(full)
        if parsed.scheme not in {"http", "https"}:
            continue

        lower = full.lower()
        ext = extension_from_url(full)
        if ext in FILE_EXTENSIONS or "download" in lower:
            candidates.add(full)

    return sorted(candidates)


def run_command(
    args: list[str],
    cwd: Path | None = None,
    timeout_seconds: int = 180,
) -> tuple[bool, str]:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
    if completed.returncode == 0:
        out = (completed.stdout or "").strip()
        return True, out or "ok"
    err = (completed.stderr or completed.stdout or "").strip()
    return False, err or f"exit code {completed.returncode}"


def github_owner_repo(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if domain_of(url) != "github.com":
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None
    owner = parts[0]
    repo = parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def clone_github(url: str, dest_root: Path) -> tuple[bool, str, Path]:
    owner_repo = github_owner_repo(url)
    if owner_repo is None:
        return False, "not a github repo url", dest_root
    owner, repo = owner_repo
    target = dest_root / f"{owner}__{repo}"
    if target.exists():
        return True, "already exists", target
    ok, msg = run_command(["git", "clone", "--depth", "1", url, str(target)])
    return ok, msg, target


def pack_npm_packages(dest_root: Path) -> list[dict]:
    results: list[dict] = []
    npm = shutil.which("npm")
    if not npm:
        for pkg in NPM_PACKAGES:
            results.append(
                {
                    "package": pkg,
                    "status": "skipped",
                    "detail": "npm not found",
                }
            )
        return results

    dest_root.mkdir(parents=True, exist_ok=True)
    for pkg in NPM_PACKAGES:
        ok, msg = run_command(
            [npm, "pack", pkg, "--pack-destination", str(dest_root)]
        )
        results.append(
            {
                "package": pkg,
                "status": "downloaded" if ok else "failed",
                "detail": msg,
            }
        )
    return results


def download_google_fonts(dest_root: Path) -> list[dict]:
    results: list[dict] = []
    dest_root.mkdir(parents=True, exist_ok=True)
    css_pattern = re.compile(r"url\((https://[^)]+)\)")

    for family in GOOGLE_FONT_FAMILIES:
        family_slug = slugify(family)
        css_url = (
            "https://fonts.googleapis.com/css2?family="
            + quote_plus(family)
            + ":wght@400;500;700&display=swap"
        )
        data, content_type, err = fetch_bytes(css_url, max_bytes=1_000_000)
        if err or not data:
            results.append(
                {
                    "family": family,
                    "status": "failed",
                    "detail": err or "no css response",
                }
            )
            continue

        css_text = data.decode("utf-8", errors="ignore")
        family_dir = dest_root / family_slug
        family_dir.mkdir(parents=True, exist_ok=True)
        (family_dir / "stylesheet.css").write_text(css_text, encoding="utf-8")

        urls = sorted(set(css_pattern.findall(css_text)))
        downloaded = 0
        for idx, font_url in enumerate(urls, start=1):
            ext = extension_from_url(font_url) or ".woff2"
            file_name = f"{family_slug}-{idx:02d}{ext}"
            ok, detail = download_file(font_url, family_dir / file_name, max_bytes=10_000_000)
            if ok:
                downloaded += 1
            else:
                results.append(
                    {
                        "family": family,
                        "status": "partial",
                        "detail": f"{font_url} -> {detail}",
                    }
                )
        results.append(
            {
                "family": family,
                "status": "downloaded" if downloaded > 0 else "failed",
                "detail": f"{downloaded} files",
            }
        )
    return results


def classify_resource(resource: Resource) -> tuple[str, str]:
    url = resource.url
    host = domain_of(url)
    ext = extension_from_url(url)
    lower_url = url.lower()

    if github_owner_repo(url):
        return "github_repo", "direct clone"
    if ext in FILE_EXTENSIONS:
        return "direct_file", "direct file link"
    if any(host == d or host.endswith(f".{d}") for d in MANUAL_DOMAINS):
        reason = next(
            MANUAL_DOMAINS[d]
            for d in MANUAL_DOMAINS
            if host == d or host.endswith(f".{d}")
        )
        return "manual", reason
    if "/api" in lower_url or "developers" in lower_url:
        return "api_docs", "API docs"
    if any(host == d or host.endswith(f".{d}") for d in REFERENCE_DOMAINS):
        return "reference", "reference page"
    return "web", "general web resource"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")


def write_markdown_summary(
    path: Path,
    run_data: dict,
) -> None:
    lines: list[str] = []
    lines.append("# Remotion Resource Download Report")
    lines.append("")
    lines.append(f"- Source DOCX: `{run_data['source_docx']}`")
    lines.append(f"- Total links parsed: `{run_data['total_links']}`")
    lines.append(f"- GitHub repos downloaded: `{run_data['counts']['github_downloaded']}`")
    lines.append(f"- Direct files downloaded: `{run_data['counts']['direct_files_downloaded']}`")
    lines.append(f"- HTML snapshots saved: `{run_data['counts']['snapshots_saved']}`")
    lines.append(f"- Manual follow-up items: `{run_data['counts']['manual_items']}`")
    lines.append("")

    lines.append("## Key Paths")
    lines.append("")
    lines.append("- Code repos: `assets/remotion_resources/code/github/`")
    lines.append("- npm tarballs: `assets/remotion_resources/packages/npm/`")
    lines.append("- Fonts: `assets/remotion_resources/fonts/google/`")
    lines.append("- Direct files: `assets/remotion_resources/downloads/direct/`")
    lines.append("- Discovered files: `assets/remotion_resources/downloads/discovered/`")
    lines.append("- Page snapshots: `assets/remotion_resources/docs/html/`")
    lines.append("- Manifest: `assets/remotion_resources/manifests/download_report.json`")
    lines.append("")

    lines.append("## Manual Follow-Up")
    lines.append("")
    if run_data["manual"]:
        for item in run_data["manual"]:
            lines.append(
                f"- {item['name']}: {item['url']} ({item['reason']})"
            )
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## npm Package Results")
    lines.append("")
    for pkg in run_data["npm_packages"]:
        lines.append(
            f"- {pkg['package']}: {pkg['status']} ({pkg['detail']})"
        )
    lines.append("")

    lines.append("## Font Results")
    lines.append("")
    for font in run_data["fonts"]:
        lines.append(f"- {font['family']}: {font['status']} ({font['detail']})")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download usable resources from a Remotion DOCX link directory."
    )
    parser.add_argument(
        "--docx",
        default="/Users/face/Downloads/remotion-resources.docx",
        help="Path to source DOCX file",
    )
    parser.add_argument(
        "--out",
        default="assets/remotion_resources",
        help="Output root directory",
    )
    parser.add_argument(
        "--max-discovered-per-resource",
        type=int,
        default=3,
        help="How many discovered direct file links to try per web page",
    )
    parser.add_argument(
        "--skip-html-snapshots",
        action="store_true",
        help="Do not save HTML snapshots",
    )
    parser.add_argument(
        "--skip-npm",
        action="store_true",
        help="Skip npm package tarball downloads",
    )
    parser.add_argument(
        "--skip-fonts",
        action="store_true",
        help="Skip Google Fonts download",
    )
    args = parser.parse_args()

    source_docx = Path(args.docx).expanduser().resolve()
    out_root = Path(args.out).resolve()
    if not source_docx.exists():
        log(f"[ERROR] DOCX not found: {source_docx}")
        return 1

    code_dir = out_root / "code" / "github"
    docs_dir = out_root / "docs" / "html"
    direct_dir = out_root / "downloads" / "direct"
    discovered_dir = out_root / "downloads" / "discovered"
    manifests_dir = out_root / "manifests"
    npm_dir = out_root / "packages" / "npm"
    fonts_dir = out_root / "fonts" / "google"

    for d in [code_dir, docs_dir, direct_dir, discovered_dir, manifests_dir]:
        d.mkdir(parents=True, exist_ok=True)

    resources = parse_docx_links(source_docx)
    log(f"[INFO] Parsed {len(resources)} unique links from DOCX")

    extracted_json = [
        {"name": r.name, "url": r.url}
        for r in resources
    ]
    write_json(manifests_dir / "resources_extracted.json", extracted_json)

    results: list[dict] = []
    manual_items: list[dict] = []
    counts = {
        "github_downloaded": 0,
        "direct_files_downloaded": 0,
        "snapshots_saved": 0,
        "manual_items": 0,
    }

    for resource in resources:
        method, reason = classify_resource(resource)
        entry = {
            "name": resource.name,
            "url": resource.url,
            "method": method,
            "classification_reason": reason,
            "status": "pending",
            "detail": "",
        }

        if method == "github_repo":
            ok, detail, target = clone_github(resource.url, code_dir)
            entry["status"] = "downloaded" if ok else "failed"
            entry["detail"] = f"{detail} -> {target}"
            if ok:
                counts["github_downloaded"] += 1
            results.append(entry)
            continue

        if method == "direct_file":
            ext = extension_from_url(resource.url) or ".bin"
            filename = f"{slugify(resource.name)}{ext}"
            ok, detail = download_file(resource.url, direct_dir / filename)
            entry["status"] = "downloaded" if ok else "failed"
            entry["detail"] = detail
            if ok:
                counts["direct_files_downloaded"] += 1
            results.append(entry)
            continue

        snapshot_saved = False
        snapshot_path = docs_dir / f"{slugify(resource.name)}.html"
        html_text = ""
        if not args.skip_html_snapshots:
            ok, detail = save_html_snapshot(resource.url, snapshot_path)
            if ok:
                counts["snapshots_saved"] += 1
                snapshot_saved = True
                html_text = snapshot_path.read_text(encoding="utf-8", errors="ignore")
            entry["detail"] = detail

        if method == "manual":
            entry["status"] = "manual"
            manual_items.append(
                {
                    "name": resource.name,
                    "url": resource.url,
                    "reason": reason,
                }
            )
            counts["manual_items"] += 1
            if snapshot_saved:
                entry["detail"] = f"{entry['detail']}; snapshot: {snapshot_path.name}"
            results.append(entry)
            continue

        discovered_count = 0
        if html_text:
            candidates = extract_download_candidates(html_text, resource.url)
            for candidate in candidates[: args.max_discovered_per_resource]:
                ext = extension_from_url(candidate) or ".bin"
                fname = (
                    f"{slugify(resource.name)}--{discovered_count + 1:02d}{ext}"
                )
                ok, detail = download_file(candidate, discovered_dir / fname)
                if ok:
                    discovered_count += 1
                    counts["direct_files_downloaded"] += 1
                else:
                    entry["detail"] = (
                        f"{entry['detail']}; discovered {candidate} -> {detail}"
                    ).strip("; ")

        entry["status"] = "snapshot" if snapshot_saved else "not_downloaded"
        if discovered_count > 0:
            entry["status"] = "partial_download"
            entry["detail"] = (
                f"{entry['detail']}; downloaded {discovered_count} discovered files"
            ).strip("; ")
        results.append(entry)

    npm_results: list[dict] = []
    if args.skip_npm:
        log("[INFO] Skipping npm package downloads")
    else:
        log("[INFO] Packing npm packages")
        npm_results = pack_npm_packages(npm_dir)

    font_results: list[dict] = []
    if args.skip_fonts:
        log("[INFO] Skipping Google Fonts downloads")
    else:
        log("[INFO] Downloading curated Google Fonts")
        font_results = download_google_fonts(fonts_dir)

    report = {
        "source_docx": str(source_docx),
        "output_root": str(out_root),
        "total_links": len(resources),
        "counts": counts,
        "resources": results,
        "manual": manual_items,
        "npm_packages": npm_results,
        "fonts": font_results,
    }
    write_json(manifests_dir / "download_report.json", report)
    write_markdown_summary(out_root / "README.md", report)

    log(f"[INFO] Finished. Output root: {out_root}")
    log("[INFO] Manifest: assets/remotion_resources/manifests/download_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
