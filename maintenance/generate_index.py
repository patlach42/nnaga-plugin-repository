#!/usr/bin/env python3
"""Emit the deterministic NNAGA repository catalog index."""
from __future__ import annotations

import argparse
import json
import posixpath
import tomllib
from pathlib import Path
from urllib.parse import urlsplit

RELEASE = "2026-08-28"


def q(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def generate(root: Path) -> str:
    rows = []
    seen: set[tuple[str, str]] = set()
    required = ("id", "name", "version", "format", "description", "manufacturer", "source")
    for path in sorted((root / "packages").glob("*/manifest.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        missing = [field for field in required if not str(data.get(field, "")).strip()]
        if missing:
            raise SystemExit(f"{path}: missing required fields: {', '.join(missing)}")
        description = str(data["description"]).strip()
        if not 30 <= len(description) <= 180 or description.casefold() == str(data["name"]).strip().casefold():
            raise SystemExit(f"{path}: description must be a 30-180 character purpose sentence")
        source = urlsplit(str(data["source"]))
        unsafe_source = (
            source.scheme != "https"
            or not source.hostname
            or source.username
            or source.password
            or source.query
            or source.fragment
            or not source.path
            or source.path.lower().endswith(".git")
            or "%2e" in source.path.lower()
            or posixpath.normpath(source.path) != source.path
        )
        if unsafe_source:
            raise SystemExit(f"{path}: source must be a canonical absolute HTTPS URL")
        tags = data.get("tags")
        if not isinstance(tags, list):
            raise SystemExit(f"{path}: tags must be a list")
        key = (str(data["format"]), str(data["id"]))
        if key in seen:
            raise SystemExit(f"{path}: duplicate format:id {key[0]}:{key[1]}")
        seen.add(key)
        rows.append(
            "[[packages]]\n"
            f"manifest = {q(path.relative_to(root).as_posix() + '?v=' + RELEASE)}\n"
            f"id = {q(data['id'])}\n"
            f"name = {q(data['name'])}\n"
            f"version = {q(data['version'])}\n"
            f"format = {q(data['format'])}\n"
            f"description = {q(data['description'])}\n"
            f"manufacturer = {q(data['manufacturer'])}\n"
            f"source = {q(data['source'])}\n"
            f"tags = {json.dumps(tags, ensure_ascii=False, separators=(',', ':'))}\n"
        )
    return f"schema = 2\nrepository = \"nnaga-plugin-repository\"\nrelease = \"{RELEASE}\"\n\n" + "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    (args.root / "index.toml").write_text(generate(args.root), encoding="utf-8")
    print(f"Generated {len(list((args.root / 'packages').glob('*/manifest.toml')))} packages")


if __name__ == "__main__":
    main()
