#!/usr/bin/env python3
"""Validate catalog JSON and local references used by the READMEs."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DATASETS = (
    ("data/papers.json", "schema/papers.schema.json", "papers", "title"),
    ("data/resources.json", "schema/resources.schema.json", "resources", "name"),
)
READMES = ("README.md", "README.zh-CN.md")
URL_FIELDS = ("paper_url", "code_url", "project_url", "url")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"\b(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)


def load_json(relative_path: str, errors: list[str]) -> Any | None:
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{relative_path}: 无法读取有效 JSON：{exc}")
        return None


def is_valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not any(
        char.isspace() for char in value
    )


def validate_collection(
    data_path: str,
    schema_path: str,
    collection_key: str,
    title_key: str,
    errors: list[str],
) -> tuple[list[dict[str, Any]], int]:
    payload = load_json(data_path, errors)
    schema = load_json(schema_path, errors)
    if payload is None or schema is None:
        return [], 0

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(payload), key=lambda item: list(item.path))
    for error in schema_errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{data_path}:{location}: schema 校验失败：{error.message}")

    records = payload.get(collection_key, [])
    if not isinstance(records, list):
        return [], len(schema_errors)

    ids = [record.get("id") for record in records if isinstance(record, dict)]
    duplicates = sorted(item for item, count in Counter(ids).items() if item and count > 1)
    for item in duplicates:
        errors.append(f"{data_path}: 重复 ID：{item}")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        label = record.get("id", f"index {index}")
        title = record.get(title_key)
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{data_path}:{label}: {title_key} 必须是非空文本")
        elif any(ord(char) < 32 for char in title):
            errors.append(f"{data_path}:{label}: {title_key} 含控制字符")

        for field in URL_FIELDS:
            value = record.get(field)
            if value is not None and (not isinstance(value, str) or not is_valid_https_url(value)):
                errors.append(f"{data_path}:{label}: {field} 不是有效 HTTPS URL：{value!r}")

        briefs = record.get("source_brief", [])
        if isinstance(briefs, list):
            for brief in briefs:
                if not isinstance(brief, str) or not (ROOT / brief).is_file():
                    errors.append(f"{data_path}:{label}: source_brief 不存在：{brief!r}")

    return records, len(schema_errors)


def local_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target).split("#", 1)[0].split("?", 1)[0]
    parsed = urlparse(target)
    if not target or target.startswith("#") or parsed.scheme or target.startswith("//"):
        return None
    return target


def validate_readme_references(errors: list[str]) -> int:
    checked: set[tuple[str, str]] = set()
    for readme in READMES:
        path = ROOT / readme
        text = path.read_text(encoding="utf-8")
        targets = MARKDOWN_LINK_RE.findall(text) + HTML_LINK_RE.findall(text)
        for raw_target in targets:
            target = local_target(raw_target)
            if target is None:
                continue
            key = (readme, target)
            if key in checked:
                continue
            checked.add(key)
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{readme}: 本地引用越出仓库：{target}")
                continue
            if not resolved.exists():
                errors.append(f"{readme}: 本地引用不存在：{target}")
    return len(checked)


def main() -> int:
    errors: list[str] = []
    totals: dict[str, int] = {}
    schema_error_count = 0

    print("开始校验数据与本地引用…")
    for data_path, schema_path, collection_key, title_key in DATASETS:
        records, schema_errors = validate_collection(
            data_path, schema_path, collection_key, title_key, errors
        )
        totals[collection_key] = len(records)
        schema_error_count += schema_errors
        print(f"  - {data_path}: {len(records)} 条记录")

    reference_count = validate_readme_references(errors)
    print(f"  - README 本地引用: {reference_count} 个")
    print(
        "摘要："
        f"{totals.get('papers', 0)} 篇论文，"
        f"{totals.get('resources', 0)} 项资源，"
        f"{schema_error_count} 个 schema 错误，"
        f"{len(errors)} 个总错误。"
    )

    if errors:
        print("\n校验失败：", file=sys.stderr)
        for error in errors:
            print(f"  ERROR: {error}", file=sys.stderr)
        return 1

    print("校验通过：schema、ID、标题/URL、source_brief 与 README 本地引用均有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
