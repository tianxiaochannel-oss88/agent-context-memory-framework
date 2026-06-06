#!/usr/bin/env python3
"""Read-only health scanner for self-improving memory records."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RECORD_FILES = ("corrections.md", "reflections.md")
REQUIRED_FIELDS = (
    "id",
    "type",
    "scope",
    "summary",
    "keywords",
    "source_refs",
    "confidence",
    "review_state",
    "verify_before_use",
    "valid_until",
    "last_seen_at",
    "evidence_count",
    "superseded_by",
    "created_at",
    "last_used_at",
    "use_count",
)
REQUIRED_SECTIONS = ("Trigger", "Lesson", "Use When", "Do Not Use When")
VALID_REVIEW_STATES = {"candidate", "active", "stale", "archived", "superseded"}


@dataclass(frozen=True)
class Record:
    path: Path
    line: int
    metadata: dict[str, object]
    body: str

    @property
    def label(self) -> str:
        record_id = self.metadata.get("id")
        if isinstance(record_id, str) and record_id:
            return record_id
        return f"{self.path.name}:{self.line}"


@dataclass
class Findings:
    missing_fields: list[str]
    missing_sections: list[str]
    invalid_values: list[str]
    expired: list[str]
    broken_refs: list[str]
    duplicate_groups: list[str]
    stale_in_active_files: list[str]

    def has_items(self) -> bool:
        return any(
            (
                self.missing_fields,
                self.missing_sections,
                self.invalid_values,
                self.expired,
                self.broken_refs,
                self.duplicate_groups,
                self.stale_in_active_files,
            )
        )


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_metadata(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    current_key: str | None = None

    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", raw)
        if match:
            key, value = match.group(1), match.group(2)
            data[key] = strip_quotes(value)
            current_key = key
            continue

        item = re.match(r"^\s*-\s+(.*)$", raw)
        if item and current_key:
            existing = data.get(current_key)
            if not isinstance(existing, list):
                existing = [] if existing == "" else [existing]
            existing.append(strip_quotes(item.group(1)))
            data[current_key] = existing

    return data


def iter_records(path: Path) -> Iterable[Record]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            i += 1
            continue

        if not in_fence and stripped == "---":
            start = i
            end = None
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == "---":
                    end = j
                    break
                j += 1

            if end is None:
                i += 1
                continue

            body_start = end + 1
            k = body_start
            body_fence = False
            while k < len(lines):
                marker = lines[k].strip()
                if marker.startswith("```"):
                    body_fence = not body_fence
                if not body_fence and marker == "---":
                    break
                k += 1

            metadata = parse_metadata(lines[start + 1 : end])
            body = "\n".join(lines[body_start:k])
            yield Record(path=path, line=start + 1, metadata=metadata, body=body)
            i = k
            continue

        i += 1


def as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def parse_date(value: object) -> dt.date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return dt.date.fromisoformat(value.strip())
    except ValueError:
        return None


def source_ref_path(source_ref: str) -> str | None:
    ref = source_ref.strip()
    if not ref or ref.startswith(("http://", "https://", "session:")):
        return None

    markdown_match = re.match(r"^(.+?\.md)(?::|#|$)", ref)
    if markdown_match:
        return markdown_match.group(1)

    return ref.split("#", 1)[0].split(":", 1)[0]


def normalize_summary(record: Record) -> tuple[str, str, str] | None:
    record_type = record.metadata.get("type")
    scope = record.metadata.get("scope")
    summary = record.metadata.get("summary")
    if not all(isinstance(item, str) and item.strip() for item in (record_type, scope, summary)):
        return None
    normalized = re.sub(r"\s+", " ", str(summary).strip().casefold())
    return (str(record_type).strip(), str(scope).strip(), normalized)


def analyze_records(workspace: Path, records: list[Record], today: dt.date) -> Findings:
    findings = Findings([], [], [], [], [], [], [])
    seen: dict[tuple[str, str, str], list[Record]] = {}

    for record in records:
        missing = [field for field in REQUIRED_FIELDS if field not in record.metadata]
        if missing:
            findings.missing_fields.append(f"{record.label}: missing {', '.join(missing)}")

        for section in REQUIRED_SECTIONS:
            if not re.search(rf"^#+\s+{re.escape(section)}\s*$", record.body, re.MULTILINE):
                findings.missing_sections.append(f"{record.label}: missing section {section}")

        review_state = record.metadata.get("review_state")
        if isinstance(review_state, str) and review_state and review_state not in VALID_REVIEW_STATES:
            findings.invalid_values.append(f"{record.label}: invalid review_state={review_state}")

        verify_before_use = record.metadata.get("verify_before_use")
        if isinstance(verify_before_use, str) and verify_before_use and verify_before_use not in {"true", "false"}:
            findings.invalid_values.append(f"{record.label}: invalid verify_before_use={verify_before_use}")

        for int_field in ("evidence_count", "use_count"):
            value = record.metadata.get(int_field)
            if isinstance(value, str) and value:
                try:
                    if int(value) < 0:
                        findings.invalid_values.append(f"{record.label}: {int_field} must be non-negative")
                except ValueError:
                    findings.invalid_values.append(f"{record.label}: invalid {int_field}={value}")

        valid_until = record.metadata.get("valid_until")
        parsed_valid_until = parse_date(valid_until)
        if isinstance(valid_until, str) and valid_until.strip() and parsed_valid_until is None:
            findings.invalid_values.append(f"{record.label}: invalid valid_until={valid_until}")
        elif parsed_valid_until and parsed_valid_until < today:
            findings.expired.append(f"{record.label}: valid_until {parsed_valid_until.isoformat()} is before {today.isoformat()}")

        for source_ref in as_list(record.metadata.get("source_refs")):
            ref_path = source_ref_path(source_ref)
            if not ref_path:
                continue
            candidate = Path(ref_path)
            if not candidate.is_absolute():
                candidate = workspace / candidate
            if not candidate.exists():
                findings.broken_refs.append(f"{record.label}: missing source_ref {source_ref}")

        if review_state in {"stale", "superseded"} and "archive" not in record.path.parts:
            findings.stale_in_active_files.append(f"{record.label}: review_state={review_state} remains in {record.path.name}")

        key = normalize_summary(record)
        if key:
            seen.setdefault(key, []).append(record)

    for duplicate_records in seen.values():
        if len(duplicate_records) > 1:
            labels = ", ".join(record.label for record in duplicate_records)
            findings.duplicate_groups.append(labels)

    return findings


def bullet_section(title: str, items: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        lines.append("- None")
    else:
        lines.extend(f"- {item}" for item in items)
    lines.append("")
    return lines


def build_report(workspace: Path, records: list[Record], findings: Findings, today: dt.date) -> str:
    lines = [
        "# Self-Improving Health",
        "",
        f"Generated: {dt.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"Workspace: {workspace}",
        "Mode: read-only; no memory records were modified.",
        "",
        "## Summary",
        "",
        f"- Records scanned: {len(records)}",
        f"- Expired records: {len(findings.expired)}",
        f"- Duplicate groups: {len(findings.duplicate_groups)}",
        f"- Broken source refs: {len(findings.broken_refs)}",
        f"- Missing field findings: {len(findings.missing_fields)}",
        f"- Missing section findings: {len(findings.missing_sections)}",
        f"- Invalid value findings: {len(findings.invalid_values)}",
        f"- Stale/superseded records in active files: {len(findings.stale_in_active_files)}",
        "",
    ]
    lines += bullet_section("Expired Records", findings.expired)
    lines += bullet_section("Duplicate Groups", findings.duplicate_groups)
    lines += bullet_section("Broken Source Refs", findings.broken_refs)
    lines += bullet_section("Missing Fields", findings.missing_fields)
    lines += bullet_section("Missing Sections", findings.missing_sections)
    lines += bullet_section("Invalid Values", findings.invalid_values)
    lines += bullet_section("Stale Or Superseded In Active Files", findings.stale_in_active_files)
    lines += [
        "## Boundary",
        "",
        "- This scan is advisory only.",
        "- It does not mark records stale.",
        "- It does not merge, delete, promote, or edit memory.",
        "- Proposed maintenance must be reviewed before applying.",
        "",
    ]
    return "\n".join(lines)


def build_proposal(workspace: Path, findings: Findings, today: dt.date) -> str:
    lines = [
        "# Self-Improving Maintenance Proposal",
        "",
        f"Generated: {dt.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"Workspace: {workspace}",
        "Review state: candidate",
        "",
        "This proposal was generated by a read-only scan. It did not change existing memory.",
        "",
        "## Proposed Review Actions",
        "",
    ]

    if not findings.has_items():
        lines.append("- No maintenance action is currently recommended.")
    else:
        for item in findings.expired:
            lines.append(f"- Review expired candidate: {item}. Decide whether to mark stale, extend `valid_until`, or keep with `verify_before_use`.")
        for item in findings.duplicate_groups:
            lines.append(f"- Review duplicate group: {item}. If they are the same lesson, update `source_refs`, `last_seen_at`, and `evidence_count`; do not merge semantics automatically.")
        for item in findings.broken_refs:
            lines.append(f"- Review broken source reference: {item}. Fix the reference or lower confidence after review.")
        for item in findings.missing_fields:
            lines.append(f"- Repair missing fields: {item}.")
        for item in findings.missing_sections:
            lines.append(f"- Repair missing sections: {item}.")
        for item in findings.invalid_values:
            lines.append(f"- Repair invalid value: {item}.")
        for item in findings.stale_in_active_files:
            lines.append(f"- Review stale/superseded active record: {item}. Consider archive after review.")

    lines += [
        "",
        "## Non-Actions",
        "",
        "- Do not automatically delete records.",
        "- Do not automatically promote records to hot memory or topic memory.",
        "- Do not automatically change persona, tool routing, permissions, or framework policy.",
        "- Do not automatically mark records stale without explicit approval or a future explicit apply flag.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Read-only self-improving memory health scanner.")
    parser.add_argument("--workspace", default=None, help="Agent workspace root. Defaults to OPENCLAW_WORKSPACE or current directory.")
    parser.add_argument("--report", default=None, help="Report output path. Defaults to reports/self-improving-health.md.")
    parser.add_argument("--proposal", default=None, help="Pending proposal output path. Defaults to pending/memory-updates/YYYY-MM-DD-self-improving-maintenance.md.")
    parser.add_argument("--date", default=None, help="Override today's date as YYYY-MM-DD for deterministic checks.")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace or Path.cwd()).expanduser().resolve()
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    lane_dir = workspace / "memory" / "self-improving"

    if not lane_dir.is_dir():
        print(f"Missing self-improving lane: {lane_dir}", file=sys.stderr)
        return 1

    records: list[Record] = []
    for filename in RECORD_FILES:
        path = lane_dir / filename
        if path.exists():
            records.extend(iter_records(path))

    findings = analyze_records(workspace, records, today)

    report_path = Path(args.report) if args.report else workspace / "reports" / "self-improving-health.md"
    proposal_path = Path(args.proposal) if args.proposal else workspace / "pending" / "memory-updates" / f"{today.isoformat()}-self-improving-maintenance.md"
    if not report_path.is_absolute():
        report_path = workspace / report_path
    if not proposal_path.is_absolute():
        proposal_path = workspace / proposal_path

    report_path.parent.mkdir(parents=True, exist_ok=True)
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(workspace, records, findings, today), encoding="utf-8")
    proposal_path.write_text(build_proposal(workspace, findings, today), encoding="utf-8")

    print(f"Report: {report_path}")
    print(f"Proposal: {proposal_path}")
    print(f"Records scanned: {len(records)}")
    print(f"Findings: {'yes' if findings.has_items() else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
