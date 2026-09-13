#!/usr/bin/env python3
"""Report stable-ID content changes without modifying source or runtime files."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        if path.suffix.lower() == ".csv":
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)):
                raise ValueError("duplicate CSV columns")
            rows = list(reader)
            if any(None in row or None in row.values() for row in rows):
                raise ValueError("CSV row width does not match header")
        elif path.suffix.lower() == ".json":
            rows = json.load(handle)
        else:
            raise ValueError("use normalized CSV or a JSON array; XLSX requires a project adapter")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("expected a list of objects")
    return rows


def compare(before, after, id_field, fields):
    if not fields or id_field in fields:
        raise ValueError("provide editable fields excluding the stable ID")
    def index(rows):
        result = {}
        for row in rows:
            identifier = row.get(id_field)
            if not isinstance(identifier, str) or not identifier.strip():
                raise ValueError("each row needs a nonempty string stable ID")
            if identifier in result:
                raise ValueError(f"duplicate ID: {identifier}")
            if not set(fields) <= row.keys():
                raise ValueError(f"missing editable fields: {identifier}")
            result[identifier] = row
        return result
    old, new = index(before), index(after)
    report = {"changed": [], "ignored_fields": [], "added": [], "removed": []}
    for identifier in sorted(old.keys() & new.keys()):
        for field in sorted(old[identifier].keys() | new[identifier].keys()):
            left, right = old[identifier], new[identifier]
            if (field in left) == (field in right) and left.get(field) == right.get(field):
                continue
            entry = {"id": identifier, "field": field,
                     "before": left.get(field), "after": right.get(field),
                     "before_present": field in left, "after_present": field in right}
            report["changed" if field in fields else "ignored_fields"].append(entry)
    report["added"] = [new[key] for key in sorted(new.keys() - old.keys())]
    report["removed"] = [old[key] for key in sorted(old.keys() - new.keys())]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--id", default="id", dest="id_field")
    parser.add_argument("--fields", nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = compare(read_rows(args.before), read_rows(args.after), args.id_field, args.fields)
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(output)
        else:
            print(output, end="")
        return 0
    except (OSError, ValueError) as error:
        print(f"content diff error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
