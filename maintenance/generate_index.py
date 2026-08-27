#!/usr/bin/env python3
"""Emit the deterministic NNAGA repository catalog index."""
from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

RELEASE = "2026-08-27"


def q(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def generate(root: Path) -> str:
    rows = []
    seen: set[tuple[str, str]] = set()
    required = ("id", "name", "version", "format", "description", "manufacturer")
    for path in sorted((root / "packages").glob("*/manifest.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        missing = [field for field in required if not str(data.get(field, "")).strip()]
        if missing:
            raise SystemExit(f"{path}: missing required fields: {', '.join(missing)}")
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
