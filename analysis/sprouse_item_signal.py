#!/usr/bin/env python3
"""First descriptive Sprouse item/contrast signal analysis.

This script runs only after the Sprouse reuse gate is approved. It writes
ignored derived outputs under data/derived/ and does not copy or redistribute
participant-level raw rows.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Callable, Iterable


RESULT_HEADER_NAMES = {"participant", "subject"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build first descriptive Sprouse item/contrast signal outputs."
    )
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=Path("/tmp/bard-data-check"),
        help="Directory containing Sprouse2013/ and Sprouse2017/ working copies.",
    )
    parser.add_argument(
        "--derived-dir",
        type=Path,
        default=Path("data/derived/sprouse"),
        help="Directory produced by scripts/build_sprouse_crosswalks.py.",
    )
    parser.add_argument(
        "--gate-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Directory produced by scripts/sprouse_analysis_gate.py.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Ignored output directory for descriptive analysis files.",
    )
    parser.add_argument(
        "--max-disagreements",
        type=int,
        default=25,
        help="Maximum ME-vs-other disagreement rows per comparison.",
    )
    return parser.parse_args()


def decode_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "mac_roman", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def first_csv_cell(line: str) -> str:
    try:
        return next(csv.reader([line]))[0].lstrip("\ufeff").strip()
    except (csv.Error, IndexError):
        return ""


def read_result_csv(path: Path) -> list[dict[str, str]]:
    text, _encoding = decode_text(path)
    lines = text.splitlines(True)
    for index, line in enumerate(lines):
        if first_csv_cell(line) in RESULT_HEADER_NAMES:
            return list(csv.DictReader(lines[index:]))
    raise ValueError(f"Could not find data header in {path}")


def read_plain_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    fields = list(fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def as_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return math.sqrt(sum((value - center) ** 2 for value in values) / (len(values) - 1))


def summarize(values: list[float]) -> dict[str, float | int]:
    return {
        "n": len(values),
        "mean": mean(values),
        "sd": sample_sd(values),
        "min": min(values),
        "max": max(values),
    }


def aggregate(
    rows: list[dict[str, str]],
    unit_getter: Callable[[dict[str, str]], str],
    value_getter: Callable[[dict[str, str]], float | None],
) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        unit = unit_getter(row)
        value = value_getter(row)
        if unit and value is not None:
            grouped[unit].append(value)
    return {unit: summarize(values) for unit, values in grouped.items() if values}


def normalize_item_to_condition(value: str) -> str:
    value = (value or "").strip()
    if value.startswith("good."):
        value = value[len("good.") :]
    parts = value.rsplit(".", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return value


def pearson(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 3:
        return None
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    x_denom = math.sqrt(sum((x - x_mean) ** 2 for x in xs))
    y_denom = math.sqrt(sum((y - y_mean) ** 2 for y in ys))
    if x_denom == 0 or y_denom == 0:
        return None
    return numerator / (x_denom * y_denom)


def value(row: dict[str, object], key: str) -> float | None:
    return as_float(row.get(key))


def add_aggregate_rows(
    output: list[dict[str, object]],
    dataset: str,
    unit_type: str,
    method: str,
    signal_name: str,
    summaries: dict[str, dict[str, float | int]],
) -> None:
    for unit_id, summary in sorted(summaries.items()):
        output.append(
            {
                "dataset": dataset,
                "unit_type": unit_type,
                "unit_id": unit_id,
                "method": method,
                "signal_name": signal_name,
                "n": summary["n"],
                "mean": summary["mean"],
                "sd": summary["sd"],
                "min": summary["min"],
                "max": summary["max"],
            }
        )


def add_correlations(
    output: list[dict[str, object]],
    dataset: str,
    unit_type: str,
    rows: list[dict[str, object]],
    columns: list[str],
) -> None:
    for x_column, y_column in combinations(columns, 2):
        pairs = []
        for row in rows:
            x = value(row, x_column)
            y = value(row, y_column)
            if x is not None and y is not None:
                pairs.append((x, y))
        r = pearson(pairs)
        output.append(
            {
                "dataset": dataset,
                "unit_type": unit_type,
                "x_signal": x_column,
                "y_signal": y_column,
                "n_units": len(pairs),
                "pearson_r": "" if r is None else r,
            }
        )


def add_disagreements(
    output: list[dict[str, object]],
    dataset: str,
    unit_type: str,
    rows: list[dict[str, object]],
    unit_field: str,
    me_column: str,
    other_columns: list[str],
    max_rows: int,
) -> None:
    for other_column in other_columns:
        complete = []
        for row in rows:
            me_raw = value(row, me_column)
            other_raw = value(row, other_column)
            if me_raw is not None and other_raw is not None:
                complete.append((row, me_raw, other_raw))
        if len(complete) < 3:
            continue

        me_values = [entry[1] for entry in complete]
        other_values = [entry[2] for entry in complete]
        me_mean = mean(me_values)
        other_mean = mean(other_values)
        me_sd = sample_sd(me_values)
        other_sd = sample_sd(other_values)
        if me_sd == 0 or other_sd == 0:
            continue

        ranked = []
        for row, me_raw, other_raw in complete:
            me_z = (me_raw - me_mean) / me_sd
            other_z = (other_raw - other_mean) / other_sd
            ranked.append((abs(me_z - other_z), row, me_raw, other_raw, me_z, other_z))
        ranked.sort(key=lambda entry: entry[0], reverse=True)

        for rank, (difference, row, me_raw, other_raw, me_z, other_z) in enumerate(
            ranked[:max_rows], start=1
        ):
            output.append(
                {
                    "dataset": dataset,
                    "unit_type": unit_type,
                    "rank": rank,
                    "unit_id": row.get(unit_field, ""),
                    "comparison": f"{me_column} vs {other_column}",
                    "me_signal": me_column,
                    "other_signal": other_column,
                    "me_value": me_raw,
                    "other_value": other_raw,
                    "me_z": me_z,
                    "other_z": other_z,
                    "abs_z_difference": difference,
                }
            )


def require_inputs(raw_root: Path, derived_dir: Path, gate_dir: Path) -> None:
    required = [
        raw_root / "Sprouse2013/SSA.data/ME experiment/LI.me.results.csv",
        raw_root / "Sprouse2013/SSA.data/LS experiment/LI.ls.results.csv",
        raw_root / "Sprouse2013/SSA.data/FC experiment/FC.signtest.csv",
        raw_root / "Sprouse2017/SA2017.data/ME.results.csv",
        raw_root / "Sprouse2017/SA2017.data/LS.results.csv",
        raw_root / "Sprouse2017/SA2017.data/FC.results.csv",
        raw_root / "Sprouse2017/SA2017.data/YN.results.csv",
        derived_dir / "2013_condition_crosswalk.csv",
        derived_dir / "2017_label_crosswalk.csv",
        derived_dir / "2017_yn_item_inclusion.csv",
        gate_dir / "analysis_readiness.csv",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        for path in missing:
            print(f"Missing input: {path}", file=sys.stderr)
        raise SystemExit(2)


def require_approved_gate(gate_dir: Path) -> None:
    readiness = read_plain_csv(gate_dir / "analysis_readiness.csv")
    failures = [row for row in readiness if row.get("passed") != "True"]
    status_rows = [row for row in readiness if row.get("gate") == "sprouse_reuse_status"]
    status = status_rows[0].get("status") if status_rows else ""
    if failures or status != "approved":
        raise SystemExit(
            "Sprouse outcome analysis requires an approved gate. Run "
            "`python3 scripts/sprouse_analysis_gate.py --reuse-status approved` first."
        )


def build_2013_outputs(
    raw_root: Path,
    derived_dir: Path,
    aggregate_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    me_rows = read_result_csv(raw_root / "Sprouse2013/SSA.data/ME experiment/LI.me.results.csv")
    ls_rows = read_result_csv(raw_root / "Sprouse2013/SSA.data/LS experiment/LI.ls.results.csv")
    fc_rows = read_result_csv(raw_root / "Sprouse2013/SSA.data/FC experiment/FC.signtest.csv")
    crosswalk = read_plain_csv(derived_dir / "2013_condition_crosswalk.csv")

    me_by_condition = aggregate(
        me_rows,
        lambda row: row["condition"],
        lambda row: as_float(row.get("zscores")),
    )
    ls_by_condition = aggregate(
        ls_rows,
        lambda row: row["condition"],
        lambda row: as_float(row.get("zscores")),
    )
    fc_by_pair = aggregate(
        fc_rows,
        lambda row: row["condition"],
        lambda row: as_float(row.get("pattern")),
    )

    add_aggregate_rows(
        aggregate_rows, "2013", "condition", "magnitude_estimation", "zscore", me_by_condition
    )
    add_aggregate_rows(aggregate_rows, "2013", "condition", "likert", "zscore", ls_by_condition)
    add_aggregate_rows(
        aggregate_rows,
        "2013",
        "pair",
        "forced_choice",
        "expected_agreement_rate",
        fc_by_pair,
    )

    condition_matrix = []
    for condition in sorted(set(me_by_condition) | set(ls_by_condition)):
        condition_matrix.append(
            {
                "dataset": "2013",
                "unit_type": "condition",
                "unit_id": condition,
                "me_zscore": me_by_condition.get(condition, {}).get("mean", ""),
                "ls_zscore": ls_by_condition.get(condition, {}).get("mean", ""),
            }
        )

    pair_rows = []
    for row in crosswalk:
        pair_id = row["pair_index"]
        fc_key = row["bad_condition_base"]
        me_bad_key = normalize_item_to_condition(row["me_bad_item"])
        me_good_key = normalize_item_to_condition(row["me_good_item"])
        ls_bad_key = normalize_item_to_condition(row["ls_bad_item"])
        ls_good_key = normalize_item_to_condition(row["ls_good_item"])
        me_bad = me_by_condition.get(me_bad_key, {})
        me_good = me_by_condition.get(me_good_key, {})
        ls_bad = ls_by_condition.get(ls_bad_key, {})
        ls_good = ls_by_condition.get(ls_good_key, {})
        fc = fc_by_pair.get(fc_key, {})
        me_contrast = ""
        ls_contrast = ""
        if "mean" in me_bad and "mean" in me_good:
            me_contrast = float(me_good["mean"]) - float(me_bad["mean"])
        if "mean" in ls_bad and "mean" in ls_good:
            ls_contrast = float(ls_good["mean"]) - float(ls_bad["mean"])
        pair_rows.append(
            {
                "dataset": "2013",
                "pair_id": pair_id,
                "label": "",
                "bad_condition": fc_key,
                "good_condition": me_good_key,
                "me_contrast": me_contrast,
                "ls_contrast": ls_contrast,
                "fc_selected_contrast": "",
                "yn_yes_contrast": "",
                "fc_expected_agreement_rate": fc.get("mean", ""),
                "me_bad_n": me_bad.get("n", ""),
                "me_good_n": me_good.get("n", ""),
                "ls_bad_n": ls_bad.get("n", ""),
                "ls_good_n": ls_good.get("n", ""),
                "fc_n": fc.get("n", ""),
                "match_basis": row.get("match_basis", ""),
            }
        )

    return condition_matrix, pair_rows


def build_2017_outputs(
    raw_root: Path,
    derived_dir: Path,
    aggregate_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    me_rows = read_result_csv(raw_root / "Sprouse2017/SA2017.data/ME.results.csv")
    ls_rows = read_result_csv(raw_root / "Sprouse2017/SA2017.data/LS.results.csv")
    fc_rows = read_result_csv(raw_root / "Sprouse2017/SA2017.data/FC.results.csv")
    yn_rows = read_result_csv(raw_root / "Sprouse2017/SA2017.data/YN.results.csv")
    labels = read_plain_csv(derived_dir / "2017_label_crosswalk.csv")
    yn_inclusion = {
        row["item"]: row["include_in_item_level_comparison"] == "True"
        for row in read_plain_csv(derived_dir / "2017_yn_item_inclusion.csv")
    }

    me_by_item = aggregate(me_rows, lambda row: row["item"], lambda row: as_float(row.get("zscores")))
    ls_by_item = aggregate(ls_rows, lambda row: row["item"], lambda row: as_float(row.get("zscores")))
    fc_selected_by_item = aggregate(
        fc_rows,
        lambda row: row["condition"],
        lambda row: 1.0 if row.get("judgment") == "1" else 0.0,
    )
    fc_agreement_by_label = aggregate(
        fc_rows,
        lambda row: row["label"],
        lambda row: as_float(row.get("pattern")),
    )
    yn_by_item = aggregate(
        [row for row in yn_rows if yn_inclusion.get(row.get("item", ""), False)],
        lambda row: row["item"],
        lambda row: as_float(row.get("judgment")),
    )

    add_aggregate_rows(aggregate_rows, "2017", "item", "magnitude_estimation", "zscore", me_by_item)
    add_aggregate_rows(aggregate_rows, "2017", "item", "likert", "zscore", ls_by_item)
    add_aggregate_rows(
        aggregate_rows, "2017", "item", "forced_choice", "selected_rate", fc_selected_by_item
    )
    add_aggregate_rows(aggregate_rows, "2017", "item", "yes_no", "yes_rate", yn_by_item)
    add_aggregate_rows(
        aggregate_rows,
        "2017",
        "pair",
        "forced_choice",
        "expected_agreement_rate",
        fc_agreement_by_label,
    )

    item_matrix = []
    item_universe = set(me_by_item) | set(ls_by_item) | set(fc_selected_by_item) | set(yn_by_item)
    for item in sorted(item_universe):
        item_matrix.append(
            {
                "dataset": "2017",
                "unit_type": "item",
                "unit_id": item,
                "me_zscore": me_by_item.get(item, {}).get("mean", ""),
                "ls_zscore": ls_by_item.get(item, {}).get("mean", ""),
                "fc_selected_rate": fc_selected_by_item.get(item, {}).get("mean", ""),
                "yn_yes_rate": yn_by_item.get(item, {}).get("mean", ""),
            }
        )

    me_by_base = aggregate(
        me_rows,
        lambda row: normalize_item_to_condition(row["item"]),
        lambda row: as_float(row.get("zscores")),
    )
    ls_by_base = aggregate(
        ls_rows,
        lambda row: normalize_item_to_condition(row["item"]),
        lambda row: as_float(row.get("zscores")),
    )
    fc_selected_by_base = aggregate(
        fc_rows,
        lambda row: normalize_item_to_condition(row["condition"]),
        lambda row: 1.0 if row.get("judgment") == "1" else 0.0,
    )
    yn_by_base = aggregate(
        [row for row in yn_rows if yn_inclusion.get(row.get("item", ""), False)],
        lambda row: normalize_item_to_condition(row["item"]),
        lambda row: as_float(row.get("judgment")),
    )

    pair_rows = []
    for row in labels:
        label = row["label"]
        bad_key = row["bad_condition"]
        good_key = row["good_condition"]
        me_bad = me_by_base.get(bad_key, {})
        me_good = me_by_base.get(good_key, {})
        ls_bad = ls_by_base.get(bad_key, {})
        ls_good = ls_by_base.get(good_key, {})
        fc_bad = fc_selected_by_base.get(bad_key, {})
        fc_good = fc_selected_by_base.get(good_key, {})
        yn_bad = yn_by_base.get(bad_key, {})
        yn_good = yn_by_base.get(good_key, {})
        fc_agreement = fc_agreement_by_label.get(label, {})
        pair_rows.append(
            {
                "dataset": "2017",
                "pair_id": label,
                "label": label,
                "bad_condition": bad_key,
                "good_condition": good_key,
                "me_contrast": contrast(me_bad, me_good),
                "ls_contrast": contrast(ls_bad, ls_good),
                "fc_selected_contrast": contrast(fc_bad, fc_good),
                "yn_yes_contrast": contrast(yn_bad, yn_good),
                "fc_expected_agreement_rate": fc_agreement.get("mean", ""),
                "me_bad_n": me_bad.get("n", ""),
                "me_good_n": me_good.get("n", ""),
                "ls_bad_n": ls_bad.get("n", ""),
                "ls_good_n": ls_good.get("n", ""),
                "fc_n": fc_agreement.get("n", ""),
                "match_basis": "label_crosswalk",
            }
        )

    return item_matrix, pair_rows


def contrast(bad_summary: dict[str, float | int], good_summary: dict[str, float | int]) -> float | str:
    if "mean" not in bad_summary or "mean" not in good_summary:
        return ""
    return float(good_summary["mean"]) - float(bad_summary["mean"])


def write_manifest(path: Path, raw_root: Path, out_dir: Path) -> None:
    rows = [
        {"key": "permission_status", "value": "approved"},
        {
            "key": "permission_source",
            "value": "Jon Sprouse correspondence reported by Brett on 2026-07-07",
        },
        {
            "key": "permission_boundary",
            "value": (
                "Limited secondary methodological analysis of magnitude estimation's "
                "contribution to an item-level signal; no redistribution of "
                "participant-level raw files."
            ),
        },
        {"key": "raw_root", "value": str(raw_root)},
        {"key": "out_dir", "value": str(out_dir)},
        {"key": "raw_files_committed", "value": "false"},
        {
            "key": "unit_note_2013_fc",
            "value": (
                "2013 forced choice is represented at pair/contrast level via "
                "FC.signtest.csv expected-agreement rates."
            ),
        },
        {
            "key": "unit_note_2017_fc",
            "value": (
                "2017 forced choice exposes item IDs in the condition field; "
                "selected_rate is the rate of judgment == 1 for that condition."
            ),
        },
    ]
    write_csv(path, ("key", "value"), rows)


def main() -> int:
    args = parse_args()
    require_inputs(args.raw_root, args.derived_dir, args.gate_dir)
    require_approved_gate(args.gate_dir)

    aggregate_rows: list[dict[str, object]] = []
    item_matrix_2013, pair_rows_2013 = build_2013_outputs(
        args.raw_root, args.derived_dir, aggregate_rows
    )
    item_matrix_2017, pair_rows_2017 = build_2017_outputs(
        args.raw_root, args.derived_dir, aggregate_rows
    )
    item_matrix = item_matrix_2013 + item_matrix_2017
    pair_rows = pair_rows_2013 + pair_rows_2017

    correlations: list[dict[str, object]] = []
    disagreements: list[dict[str, object]] = []
    add_correlations(correlations, "2013", "condition", item_matrix_2013, ["me_zscore", "ls_zscore"])
    add_correlations(
        correlations,
        "2013",
        "pair",
        pair_rows_2013,
        ["me_contrast", "ls_contrast", "fc_expected_agreement_rate"],
    )
    add_correlations(
        correlations,
        "2017",
        "item",
        item_matrix_2017,
        ["me_zscore", "ls_zscore", "fc_selected_rate", "yn_yes_rate"],
    )
    add_correlations(
        correlations,
        "2017",
        "pair",
        pair_rows_2017,
        ["me_contrast", "ls_contrast", "fc_selected_contrast", "yn_yes_contrast"],
    )
    add_disagreements(
        disagreements,
        "2013",
        "condition",
        item_matrix_2013,
        "unit_id",
        "me_zscore",
        ["ls_zscore"],
        args.max_disagreements,
    )
    add_disagreements(
        disagreements,
        "2013",
        "pair",
        pair_rows_2013,
        "pair_id",
        "me_contrast",
        ["ls_contrast", "fc_expected_agreement_rate"],
        args.max_disagreements,
    )
    add_disagreements(
        disagreements,
        "2017",
        "item",
        item_matrix_2017,
        "unit_id",
        "me_zscore",
        ["ls_zscore", "fc_selected_rate", "yn_yes_rate"],
        args.max_disagreements,
    )
    add_disagreements(
        disagreements,
        "2017",
        "pair",
        pair_rows_2017,
        "pair_id",
        "me_contrast",
        ["ls_contrast", "fc_selected_contrast", "yn_yes_contrast"],
        args.max_disagreements,
    )

    write_csv(
        args.out_dir / "sprouse_item_method_aggregates.csv",
        ("dataset", "unit_type", "unit_id", "method", "signal_name", "n", "mean", "sd", "min", "max"),
        aggregate_rows,
    )
    write_csv(
        args.out_dir / "sprouse_item_signal_matrix.csv",
        (
            "dataset",
            "unit_type",
            "unit_id",
            "me_zscore",
            "ls_zscore",
            "fc_selected_rate",
            "yn_yes_rate",
        ),
        item_matrix,
    )
    write_csv(
        args.out_dir / "sprouse_pair_contrasts.csv",
        (
            "dataset",
            "pair_id",
            "label",
            "bad_condition",
            "good_condition",
            "me_contrast",
            "ls_contrast",
            "fc_selected_contrast",
            "yn_yes_contrast",
            "fc_expected_agreement_rate",
            "me_bad_n",
            "me_good_n",
            "ls_bad_n",
            "ls_good_n",
            "fc_n",
            "match_basis",
        ),
        pair_rows,
    )
    write_csv(
        args.out_dir / "sprouse_signal_correlations.csv",
        ("dataset", "unit_type", "x_signal", "y_signal", "n_units", "pearson_r"),
        correlations,
    )
    write_csv(
        args.out_dir / "sprouse_me_disagreements.csv",
        (
            "dataset",
            "unit_type",
            "rank",
            "unit_id",
            "comparison",
            "me_signal",
            "other_signal",
            "me_value",
            "other_value",
            "me_z",
            "other_z",
            "abs_z_difference",
        ),
        disagreements,
    )
    write_manifest(args.out_dir / "sprouse_analysis_manifest.csv", args.raw_root, args.out_dir)

    print(f"Wrote Sprouse descriptive analysis outputs to {args.out_dir}")
    print(f"Item/condition matrix rows: {len(item_matrix)}")
    print(f"Pair contrast rows: {len(pair_rows)}")
    print(f"Correlation rows: {len(correlations)}")
    print(f"ME disagreement rows: {len(disagreements)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
