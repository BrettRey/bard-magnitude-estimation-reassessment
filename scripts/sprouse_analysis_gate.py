#!/usr/bin/env python3
"""Create a gated Sprouse analysis readiness manifest.

This is the first outcome-analysis scaffold. It reads the machine-readable
pre-analysis rules produced by `build_sprouse_crosswalks.py`, verifies the
crosswalk state, and writes local readiness manifests. It does not compute
method rankings, means, convergence rates, model fits, or outcome summaries.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


EXPECTED_RULES = {
    ("2013", "forced_choice_primary_representation"): "FC.signtest.csv",
    ("2013", "forced_choice_sensitivity_representation"): "FC.logistic.csv",
    ("2017", "yes_no_item_level_exclusions"): "exclude item IDs B, G, and M from item-level comparisons",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify Sprouse pre-analysis rules and write readiness manifests."
    )
    parser.add_argument(
        "--derived-dir",
        type=Path,
        default=Path("data/derived/sprouse"),
        help="Directory produced by scripts/build_sprouse_crosswalks.py.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Ignored output directory for readiness manifests.",
    )
    parser.add_argument(
        "--reuse-status",
        choices=("pending", "approved", "verification_only", "denied"),
        default="pending",
        help="Current status of the Sprouse novel-reuse request.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(fieldnames)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def require_files(derived_dir: Path) -> dict[str, Path]:
    files = {
        "analysis_rules": derived_dir / "analysis_rules.csv",
        "schema_summary": derived_dir / "schema_summary.csv",
        "crosswalk_2013": derived_dir / "2013_condition_crosswalk.csv",
        "yn_inclusion_2017": derived_dir / "2017_yn_item_inclusion.csv",
    }
    missing = [path for path in files.values() if not path.exists()]
    if missing:
        missing_list = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(
            "Missing derived structural files. Run "
            "`python3 scripts/build_sprouse_crosswalks.py` first.\n"
            f"{missing_list}"
        )
    return files


def verify_rules(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    observed = {(row["dataset"], row["rule"]): row["decision"] for row in rows}
    checks = []
    for key, expected_decision in EXPECTED_RULES.items():
        observed_decision = observed.get(key, "")
        checks.append(
            {
                "check": f"rule:{key[0]}:{key[1]}",
                "passed": observed_decision == expected_decision,
                "expected": expected_decision,
                "observed": observed_decision,
            }
        )
    return checks


def build_manifest(
    schema_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
    yn_inclusion_rows: list[dict[str, str]],
    reuse_status: str,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    exact_2013 = sum(row["match_basis"] == "exact" for row in crosswalk_rows)
    compact_2013 = sum(row["match_basis"] == "compact_spacing_variant" for row in crosswalk_rows)
    unmatched_2013 = sum(row["match_basis"] == "unmatched" for row in crosswalk_rows)
    yn_included = sum(row["include_in_item_level_comparison"] == "True" for row in yn_inclusion_rows)
    yn_excluded = sum(row["include_in_item_level_comparison"] != "True" for row in yn_inclusion_rows)
    outcome_allowed = reuse_status in {"approved", "verification_only"}

    readiness = [
        {
            "gate": "sprouse_reuse_status",
            "status": reuse_status,
            "passed": outcome_allowed,
            "detail": "Novel outcome analysis is gated pending reuse approval or verification-only framing.",
        },
        {
            "gate": "analysis_rules_present",
            "status": "checked",
            "passed": len(rule_rows) >= len(EXPECTED_RULES),
            "detail": f"{len(rule_rows)} rule rows loaded.",
        },
        {
            "gate": "2013_pair_crosswalk",
            "status": "checked",
            "passed": unmatched_2013 == 0,
            "detail": f"{exact_2013} exact; {compact_2013} compact spacing-variant; {unmatched_2013} unmatched.",
        },
        {
            "gate": "2017_yes_no_item_inclusion",
            "status": "checked",
            "passed": yn_included == 786 and yn_excluded == 3,
            "detail": f"{yn_included} included; {yn_excluded} excluded.",
        },
    ]
    readiness.extend(verify_rules(rule_rows))

    planned_inputs = []
    roles = {
        ("2013", "me"): "primary",
        ("2013", "ls"): "primary",
        ("2013", "fc_signtest"): "primary_forced_choice",
        ("2013", "fc_logistic"): "sensitivity_forced_choice",
        ("2017", "me"): "secondary",
        ("2017", "ls"): "secondary",
        ("2017", "fc"): "secondary",
        ("2017", "yn"): "secondary_with_item_exclusion",
    }
    for row in schema_rows:
        key = (row["dataset"], row["role"])
        if key not in roles:
            continue
        planned_inputs.append(
            {
                "dataset": row["dataset"],
                "role": row["role"],
                "analysis_role": roles[key],
                "rows": row["rows"],
                "columns": row["columns"],
            }
        )
    return readiness, planned_inputs


def main() -> int:
    args = parse_args()
    files = require_files(args.derived_dir)
    rule_rows = read_csv(files["analysis_rules"])
    schema_rows = read_csv(files["schema_summary"])
    crosswalk_rows = read_csv(files["crosswalk_2013"])
    yn_inclusion_rows = read_csv(files["yn_inclusion_2017"])

    readiness, planned_inputs = build_manifest(
        schema_rows=schema_rows,
        rule_rows=rule_rows,
        crosswalk_rows=crosswalk_rows,
        yn_inclusion_rows=yn_inclusion_rows,
        reuse_status=args.reuse_status,
    )
    write_csv(
        args.out_dir / "analysis_readiness.csv",
        ("gate", "status", "passed", "detail", "check", "expected", "observed"),
        readiness,
    )
    write_csv(
        args.out_dir / "planned_inputs.csv",
        ("dataset", "role", "analysis_role", "rows", "columns"),
        planned_inputs,
    )

    failed = [row for row in readiness if row.get("passed") is False]
    print(f"Wrote readiness manifests to {args.out_dir}")
    print(f"Readiness gates failed: {len(failed)}")
    if failed:
        for row in failed:
            print(f"- {row.get('gate') or row.get('check')}: {row.get('detail') or row.get('observed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
