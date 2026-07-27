#!/usr/bin/env python3
"""Atomically manage Cline's durable PR review worklist."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = 1
STATES = ("todo", "in_progress", "waiting", "done")
COMMON_FIELDS = {"repo", "number", "url", "title", "opened", "state"}
STATE_FIELDS = {
    "todo": set(),
    "in_progress": {"lastUpdate", "purpose", "targetBranch", "baseSha", "headSha", "nextStep", "evidence", "resources"},
    "waiting": {
        "lastUpdate",
        "purpose",
        "targetBranch",
        "baseSha",
        "headSha",
        "waitingFor",
        "recheckWhen",
        "nextStep",
        "evidence",
        "resources",
    },
    "done": {"lastUpdate", "outcome", "evidence", "action", "verifiedRemoteState", "resources"},
}


class WorklistError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean(value: str, name: str) -> str:
    result = " ".join(value.split())
    if not result:
        raise WorklistError(f"{name} must not be empty")
    return result


def identity(item: dict[str, Any]) -> str:
    return f"{item['repo']}#{item['number']}"


def expected_url(repo: str, number: int) -> str:
    return f"https://github.com/{repo}/pull/{number}"


def validate_item(item: Any) -> None:
    if not isinstance(item, dict):
        raise WorklistError("Every item must be an object")
    state = item.get("state")
    if state not in STATES:
        raise WorklistError(f"Invalid state: {state!r}")
    required = (COMMON_FIELDS - {"opened"}) | STATE_FIELDS[state]
    allowed = COMMON_FIELDS | STATE_FIELDS[state]
    missing = required - set(item)
    unknown = set(item) - allowed
    label = f"{item.get('repo', '?')}#{item.get('number', '?')}"
    if missing:
        raise WorklistError(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise WorklistError(f"{label} has fields invalid for {state}: {', '.join(sorted(unknown))}")
    repo = item["repo"]
    number = item["number"]
    if not isinstance(repo, str) or repo.count("/") != 1 or not all(part for part in repo.split("/")):
        raise WorklistError(f"Invalid repository: {repo!r}")
    if not isinstance(number, int) or isinstance(number, bool) or number < 1:
        raise WorklistError(f"Invalid PR number: {number!r}")
    if not isinstance(item["url"], str) or item["url"].lower() != expected_url(repo, number).lower():
        raise WorklistError(f"URL does not match {label}")
    if "opened" in item and (not isinstance(item["opened"], str) or not item["opened"].strip()):
        raise WorklistError(f"{label}.opened must be a non-empty string when present")
    for field in required - {"number", "resources"}:
        if not isinstance(item[field], str) or not item[field].strip():
            raise WorklistError(f"{label}.{field} must be a non-empty string")
    if "resources" in item:
        resources = item["resources"]
        if not isinstance(resources, list) or any(not isinstance(value, str) or not value.strip() for value in resources):
            raise WorklistError(f"{label}.resources must be an array of non-empty strings")
        if len(resources) != len(set(resources)):
            raise WorklistError(f"{label}.resources contains duplicates")
        if state == "done" and resources:
            raise WorklistError(f"{label} is done but still owns resources")


def validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or set(data) != {"version", "items"}:
        raise WorklistError("Root must contain exactly version and items")
    if data["version"] != VERSION:
        raise WorklistError(f"Unsupported worklist version: {data['version']!r}")
    if not isinstance(data["items"], list):
        raise WorklistError("items must be an array")
    seen: set[str] = set()
    active = 0
    for item in data["items"]:
        validate_item(item)
        key = identity(item).lower()
        if key in seen:
            raise WorklistError(f"Duplicate PR: {identity(item)}")
        seen.add(key)
        active += item["state"] == "in_progress"
    if active > 1:
        raise WorklistError("At most one item may be in_progress")
    return data


def default_path() -> Path:
    override = os.environ.get("PR_REVIEW_WORKLIST")
    return Path(override).expanduser() if override else Path.home() / ".cline" / "pr-review-worklist.json"


def read_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def load(path: Path, create: bool = False) -> tuple[dict[str, Any], bytes | None]:
    original = read_bytes(path)
    if original is None:
        if create:
            return {"version": VERSION, "items": []}, None
        raise WorklistError(f"Worklist not found: {path}; run init first")
    try:
        return validate(json.loads(original)), original
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise WorklistError(f"Worklist is not valid UTF-8 JSON: {path}") from error


def atomic_write(path: Path, data: dict[str, Any], original: bytes | None) -> None:
    validate(data)
    rendered = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    current = read_bytes(path)
    if current != original:
        expected = "missing" if original is None else hashlib.sha256(original).hexdigest()
        actual = "missing" if current is None else hashlib.sha256(current).hexdigest()
        raise WorklistError(f"Worklist changed during command (expected {expected}, found {actual}); retry")
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(rendered)
            output.flush()
            os.fsync(output.fileno())
        if path.exists():
            os.chmod(temporary, path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def find_item(data: dict[str, Any], pr: str) -> dict[str, Any]:
    matches = [item for item in data["items"] if identity(item).lower() == pr.lower()]
    if len(matches) != 1:
        raise WorklistError(f"Expected one item for {pr}, found {len(matches)}")
    return matches[0]


def active_item(data: dict[str, Any], pr: str | None = None) -> dict[str, Any]:
    matches = [item for item in data["items"] if item["state"] == "in_progress"]
    if len(matches) != 1:
        raise WorklistError(f"Expected one in_progress item, found {len(matches)}")
    item = matches[0]
    if pr and identity(item).lower() != pr.lower():
        raise WorklistError(f"Expected active PR {pr}, found {identity(item)}")
    return item


def command_init(args: argparse.Namespace) -> None:
    data, original = load(args.path, create=True)
    atomic_write(args.path, data, original)
    print(args.path)


def command_validate(args: argparse.Namespace) -> None:
    load(args.path)
    print("valid")


def command_summary(args: argparse.Namespace) -> None:
    data, _ = load(args.path)
    counts = {state: sum(item["state"] == state for item in data["items"]) for state in STATES}
    counts["active"] = next((identity(item) for item in data["items"] if item["state"] == "in_progress"), None)
    print(json.dumps(counts, separators=(",", ":")) if args.json else " ".join(f"{key}={value}" for key, value in counts.items()))


def command_add(args: argparse.Namespace) -> None:
    data, original = load(args.path)
    item = {
        "repo": clean(args.repo, "repo"),
        "number": args.number,
        "url": expected_url(args.repo, args.number),
        "title": clean(args.title, "title"),
        "state": "todo",
    }
    if args.opened:
        item["opened"] = clean(args.opened, "opened")
    if any(identity(existing).lower() == identity(item).lower() for existing in data["items"]):
        raise WorklistError(f"{identity(item)} already exists")
    data["items"].append(item)
    atomic_write(args.path, data, original)
    print(identity(item))


def command_start(args: argparse.Namespace) -> None:
    data, original = load(args.path)
    if any(item["state"] == "in_progress" for item in data["items"]):
        raise WorklistError("An item is already in_progress")
    if args.pr:
        item = find_item(data, args.pr)
        if item["state"] not in {"todo", "waiting"}:
            raise WorklistError(f"{args.pr} cannot start from {item['state']}")
    else:
        item = next((candidate for candidate in data["items"] if candidate["state"] == "todo"), None)
        if item is None:
            raise WorklistError("No todo item is available")
    previous_state = item["state"]
    previous_evidence = item.get("evidence")
    purpose = item.get("purpose", item["title"])
    target_branch = item.get("targetBranch", "pending live verification")
    base_sha = item.get("baseSha", "pending")
    head_sha = item.get("headSha", "pending")
    resources = item.get("resources", [])
    for field in STATE_FIELDS[previous_state]:
        item.pop(field, None)
    item.update(
        state="in_progress",
        lastUpdate=f"{now()} — {clean(args.note, 'note')}",
        purpose=purpose,
        targetBranch=target_branch,
        baseSha=base_sha,
        headSha=head_sha,
        nextStep=clean(args.next_step, "next step"),
        evidence=(f"Resumed from waiting. {previous_evidence}" if previous_state == "waiting" else "none yet"),
        resources=resources,
    )
    atomic_write(args.path, data, original)
    print(identity(item))


def command_update(args: argparse.Namespace) -> None:
    data, original = load(args.path)
    item = active_item(data, args.pr)
    item["lastUpdate"] = f"{now()} — {clean(args.note, 'note')}"
    for argument, field in (
        (args.target_branch, "targetBranch"),
        (args.base, "baseSha"),
        (args.head, "headSha"),
        (args.next_step, "nextStep"),
        (args.evidence, "evidence"),
    ):
        if argument is not None:
            item[field] = clean(argument, field)
    if args.clear_resources:
        item["resources"] = []
    elif args.resource is not None:
        additions = [clean(value, "resource") for value in args.resource]
        item["resources"] = list(dict.fromkeys([*item["resources"], *additions]))
    atomic_write(args.path, data, original)
    print(identity(item))


def command_wait(args: argparse.Namespace) -> None:
    data, original = load(args.path)
    item = active_item(data, args.pr)
    item.update(
        state="waiting",
        lastUpdate=f"{now()} — {clean(args.note, 'note')}",
        waitingFor=clean(args.waiting_for, "waiting for"),
        recheckWhen=clean(args.recheck_when, "recheck when"),
        nextStep=clean(args.next_step, "next step"),
        evidence=clean(args.evidence, "evidence"),
    )
    atomic_write(args.path, data, original)
    print(identity(item))


def command_done(args: argparse.Namespace) -> None:
    data, original = load(args.path)
    item = active_item(data, args.pr)
    if item["resources"]:
        raise WorklistError("Clear resources with update --clear-resources before marking done")
    for field in STATE_FIELDS["in_progress"]:
        item.pop(field, None)
    item.update(
        state="done",
        lastUpdate=f"{now()} — {clean(args.note, 'note')}",
        outcome=clean(args.outcome, "outcome"),
        evidence=clean(args.evidence, "evidence"),
        action=clean(args.action, "action"),
        verifiedRemoteState=clean(args.remote_state, "remote state"),
        resources=[],
    )
    atomic_write(args.path, data, original)
    print(identity(item))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=default_path())
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text, function in (
        ("init", "create or normalize the worklist", command_init),
        ("validate", "validate the worklist", command_validate),
        ("summary", "print worklist counts", command_summary),
    ):
        command = commands.add_parser(name, help=help_text)
        if name == "summary":
            command.add_argument("--json", action="store_true")
        command.set_defaults(func=function)
    command = commands.add_parser("add", help="append one PR as todo")
    command.add_argument("--repo", required=True)
    command.add_argument("--number", type=int, required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--opened")
    command.set_defaults(func=command_add)
    command = commands.add_parser("start", help="move the first todo or a named todo/waiting PR to in_progress")
    command.add_argument("--pr")
    command.add_argument("--note", default="selected for review")
    command.add_argument("--next-step", required=True)
    command.set_defaults(func=command_start)
    command = commands.add_parser("update", help="update the active PR")
    command.add_argument("--pr", required=True)
    command.add_argument("--note", required=True)
    command.add_argument("--target-branch")
    command.add_argument("--base")
    command.add_argument("--head")
    command.add_argument("--next-step")
    command.add_argument("--evidence")
    resources = command.add_mutually_exclusive_group()
    resources.add_argument("--resource", action="append")
    resources.add_argument("--clear-resources", action="store_true")
    command.set_defaults(func=command_update)
    command = commands.add_parser("wait", help="move the active PR to waiting")
    command.add_argument("--pr", required=True)
    command.add_argument("--note", required=True)
    command.add_argument("--waiting-for", required=True)
    command.add_argument("--recheck-when", required=True)
    command.add_argument("--next-step", required=True)
    command.add_argument("--evidence", required=True)
    command.set_defaults(func=command_wait)
    command = commands.add_parser("done", help="move the resource-free active PR to done")
    command.add_argument("--pr", required=True)
    command.add_argument("--note", required=True)
    command.add_argument("--outcome", required=True)
    command.add_argument("--evidence", required=True)
    command.add_argument("--action", required=True)
    command.add_argument("--remote-state", required=True)
    command.set_defaults(func=command_done)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.func(args)
    except (WorklistError, OSError) as error:
        print(f"worklist: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
