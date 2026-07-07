#!/usr/bin/env python3
"""Pair-level robustness diagnostics for Sprouse ME resolution claims.

The response-function diagnostic tests whether raw Likert means look bounded
relative to ME. This script asks the contrast-level follow-up: after aggregating
ME and Likert by condition, do good-vs-bad pairs reveal ME-specific distinctions
that bounded methods blur?
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import numpy as np


RESULT_HEADER_NAMES = {"participant", "subject"}

ROW_FIELDS = (
    "dataset",
    "pair_id",
    "label",
    "bad_condition",
    "good_condition",
    "me_contrast",
    "me_contrast_from_raw",
    "ls_raw_contrast",
    "ls_z_contrast",
    "ls_z_contrast_from_raw",
    "fc_expected_agreement_rate",
    "fc_expected_margin",
    "fc_selected_contrast",
    "yn_yes_contrast",
    "bounded_predictors",
    "bounded_prediction",
    "me_residual_after_bounded",
    "me_residual_z",
    "me_rank",
    "bounded_prediction_rank",
    "ls_raw_rank",
    "rank_shift_me_over_bounded",
    "me_top_quartile",
    "bounded_top_quartile",
    "me_top_quartile_bounded_bottom_half",
    "residual_direction",
)

SUMMARY_FIELDS = (
    "dataset",
    "n_pairs",
    "bounded_predictors",
    "bounded_model_r_squared",
    "bounded_model_residual_sd",
    "bounded_model_mean_abs_residual",
    "pearson_me_ls_raw",
    "spearman_me_ls_raw",
    "pearson_me_ls_z",
    "spearman_me_ls_z",
    "pearson_me_bounded_prediction",
    "spearman_me_bounded_prediction",
    "pearson_me_fc_expected",
    "pearson_me_fc_selected",
    "pearson_me_yn_yes",
    "top_quartile_overlap_count",
    "top_quartile_overlap_rate",
    "bottom_quartile_overlap_count",
    "bottom_quartile_overlap_rate",
    "me_top_quartile_bounded_bottom_half_count",
    "large_positive_residual_count",
    "large_negative_residual_count",
    "mean_abs_rank_shift",
    "max_abs_rank_shift",
)

EXTREME_FIELDS = (
    "dataset",
    "extreme_type",
    "rank",
    "pair_id",
    "label",
    "bad_condition",
    "good_condition",
    "me_contrast",
    "ls_raw_contrast",
    "bounded_prediction",
    "me_residual_after_bounded",
    "me_residual_z",
    "rank_shift_me_over_bounded",
    "fc_expected_agreement_rate",
    "fc_selected_contrast",
    "yn_yes_contrast",
)

MANIFEST_FIELDS = (
    "created_at",
    "analysis",
    "raw_root",
    "output_file",
    "rows",
    "note",
)


@dataclass(frozen=True)
class RawSpec:
    dataset: str
    me_path: Path
    ls_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pair-level resolution robustness diagnostics for Sprouse data."
    )
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=Path("/tmp/bard-data-check"),
        help="Directory containing Sprouse2013/ and Sprouse2017/ working copies.",
    )
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Directory containing approved readiness and descriptive Sprouse outputs.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Ignored output directory for pair-level diagnostics.",
    )
    parser.add_argument(
        "--max-extremes",
        type=int,
        default=10,
        help="Rows per dataset and direction in the residual-extremes output.",
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


def finite_or_blank(value: float | None) -> float | str:
    if value is None or not math.isfinite(value):
        return ""
    return value


def require_approved_gate(analysis_dir: Path) -> None:
    readiness_path = analysis_dir / "analysis_readiness.csv"
    if not readiness_path.exists():
        raise SystemExit(
            "Missing approved readiness manifest. Run "
            "`python3 scripts/sprouse_analysis_gate.py --reuse-status approved` first."
        )
    readiness = read_plain_csv(readiness_path)
    status_rows = [row for row in readiness if row.get("gate") == "sprouse_reuse_status"]
    failures = [row for row in readiness if row.get("passed") != "True"]
    status = status_rows[0].get("status") if status_rows else ""
    if status != "approved" or failures:
        raise SystemExit(
            "Sprouse pair-level analysis requires all readiness gates to pass "
            "with reuse status approved."
        )


def require_pair_outputs(analysis_dir: Path) -> None:
    path = analysis_dir / "sprouse_pair_contrasts.csv"
    if not path.exists():
        raise SystemExit(
            "Missing pair contrasts. Run `python3 analysis/sprouse_item_signal.py` first."
        )


def raw_specs(raw_root: Path) -> tuple[RawSpec, ...]:
    return (
        RawSpec(
            dataset="2013",
            me_path=raw_root / "Sprouse2013/SSA.data/ME experiment/LI.me.results.csv",
            ls_path=raw_root / "Sprouse2013/SSA.data/LS experiment/LI.ls.results.csv",
        ),
        RawSpec(
            dataset="2017",
            me_path=raw_root / "Sprouse2017/SA2017.data/ME.results.csv",
            ls_path=raw_root / "Sprouse2017/SA2017.data/LS.results.csv",
        ),
    )


def aggregate_by_condition(
    rows: list[dict[str, str]], value_column: str
) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        condition = (row.get("condition") or "").strip()
        value = as_float(row.get(value_column))
        if condition and value is not None:
            grouped[condition].append(value)
    return {
        condition: {
            "n": len(values),
            "mean": mean(values),
            "sd": sample_sd(values),
            "min": min(values),
            "max": max(values),
        }
        for condition, values in grouped.items()
        if values
    }


def condition_summaries(raw_root: Path) -> dict[str, dict[str, dict[str, float | int]]]:
    output: dict[str, dict[str, dict[str, float | int]]] = {}
    for spec in raw_specs(raw_root):
        for path in (spec.me_path, spec.ls_path):
            if not path.exists():
                raise SystemExit(f"Missing raw Sprouse file: {path}")
        me_rows = read_result_csv(spec.me_path)
        ls_rows = read_result_csv(spec.ls_path)
        me_z = aggregate_by_condition(me_rows, "zscores")
        ls_raw = aggregate_by_condition(ls_rows, "judgment")
        ls_z = aggregate_by_condition(ls_rows, "zscores")
        conditions = sorted(set(me_z) & set(ls_raw) & set(ls_z))
        output[spec.dataset] = {
            condition: {
                "me_z_mean": me_z[condition]["mean"],
                "me_n": me_z[condition]["n"],
                "ls_raw_mean": ls_raw[condition]["mean"],
                "ls_raw_n": ls_raw[condition]["n"],
                "ls_z_mean": ls_z[condition]["mean"],
                "ls_z_n": ls_z[condition]["n"],
            }
            for condition in conditions
        }
    return output


def compact_condition_key(value: str) -> str:
    return "".join(value.split())


def condition_lookup(
    conditions: dict[str, dict[str, float | int]]
) -> dict[str, dict[str, float | int]]:
    lookup = dict(conditions)
    compact: dict[str, list[dict[str, float | int]]] = defaultdict(list)
    for condition, summary in conditions.items():
        compact[compact_condition_key(condition)].append(summary)
    for key, matches in compact.items():
        if len(matches) == 1 and key not in lookup:
            lookup[key] = matches[0]
    return lookup


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys, strict=True))
    x_denom = math.sqrt(sum((x - x_mean) ** 2 for x in xs))
    y_denom = math.sqrt(sum((y - y_mean) ** 2 for y in ys))
    if x_denom == 0 or y_denom == 0:
        return None
    return numerator / (x_denom * y_denom)


def average_ranks(values: list[float], descending: bool = False) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda pair: pair[1], reverse=descending)
    ranks = [0.0] * len(values)
    index = 0
    while index < len(indexed):
        end = index + 1
        while end < len(indexed) and indexed[end][1] == indexed[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        for subindex in range(index, end):
            ranks[indexed[subindex][0]] = average_rank
        index = end
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    return pearson(average_ranks(xs), average_ranks(ys))


def numeric_column(rows: list[dict[str, object]], column: str) -> list[float]:
    return [float(row[column]) for row in rows if row.get(column) != ""]


def paired_numeric(
    rows: list[dict[str, object]], x_column: str, y_column: str
) -> tuple[list[float], list[float]]:
    xs = []
    ys = []
    for row in rows:
        x = as_float(row.get(x_column))
        y = as_float(row.get(y_column))
        if x is not None and y is not None:
            xs.append(x)
            ys.append(y)
    return xs, ys


def build_pair_rows(
    analysis_dir: Path, condition_data: dict[str, dict[str, dict[str, float | int]]]
) -> list[dict[str, object]]:
    pair_rows = read_plain_csv(analysis_dir / "sprouse_pair_contrasts.csv")
    output = []
    missing = []
    for row in pair_rows:
        dataset = row["dataset"]
        bad_condition = row["bad_condition"]
        good_condition = row["good_condition"]
        dataset_conditions = condition_data.get(dataset, {})
        lookup = condition_lookup(dataset_conditions)
        bad = dataset_conditions.get(bad_condition) or lookup.get(compact_condition_key(bad_condition))
        good = dataset_conditions.get(good_condition) or lookup.get(compact_condition_key(good_condition))
        if bad is None or good is None:
            missing.append((dataset, row["pair_id"], bad_condition, good_condition))
            continue

        fc_expected = as_float(row.get("fc_expected_agreement_rate"))
        output.append(
            {
                "dataset": dataset,
                "pair_id": row["pair_id"],
                "label": row.get("label", ""),
                "bad_condition": bad_condition,
                "good_condition": good_condition,
                "me_contrast": as_float(row.get("me_contrast")),
                "me_contrast_from_raw": float(good["me_z_mean"]) - float(bad["me_z_mean"]),
                "ls_raw_contrast": float(good["ls_raw_mean"]) - float(bad["ls_raw_mean"]),
                "ls_z_contrast": as_float(row.get("ls_contrast")),
                "ls_z_contrast_from_raw": float(good["ls_z_mean"]) - float(bad["ls_z_mean"]),
                "fc_expected_agreement_rate": finite_or_blank(fc_expected),
                "fc_expected_margin": finite_or_blank(fc_expected - 0.5 if fc_expected is not None else None),
                "fc_selected_contrast": finite_or_blank(as_float(row.get("fc_selected_contrast"))),
                "yn_yes_contrast": finite_or_blank(as_float(row.get("yn_yes_contrast"))),
            }
        )

    if missing:
        formatted = "\n".join(
            f"{dataset} {pair_id}: {bad} / {good}"
            for dataset, pair_id, bad, good in missing[:10]
        )
        raise SystemExit(f"Missing condition summaries for pair rows:\n{formatted}")
    return output


def select_predictors(rows: list[dict[str, object]]) -> list[str]:
    candidates = [
        "ls_raw_contrast",
        "fc_expected_margin",
        "fc_selected_contrast",
        "yn_yes_contrast",
    ]
    selected = []
    for column in candidates:
        values = [as_float(row.get(column)) for row in rows]
        complete = [value for value in values if value is not None]
        if len(complete) == len(rows) and sample_sd(complete) > 0:
            selected.append(column)
    return selected


def fit_bounded_prediction(rows: list[dict[str, object]], predictors: list[str]) -> float:
    y = np.asarray([float(row["me_contrast"]) for row in rows], dtype=float)
    matrix_columns = [np.ones(len(rows))]
    for predictor in predictors:
        values = np.asarray([float(row[predictor]) for row in rows], dtype=float)
        sd = float(np.std(values, ddof=1))
        if sd == 0:
            raise ValueError(f"Zero-variance predictor: {predictor}")
        matrix_columns.append((values - float(np.mean(values))) / sd)
    design = np.column_stack(matrix_columns)
    params, _residuals, _rank, _singular = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ params
    residuals = y - fitted
    residual_sd = sample_sd([float(value) for value in residuals])
    for index, row in enumerate(rows):
        row["bounded_predictors"] = ";".join(predictors)
        row["bounded_prediction"] = float(fitted[index])
        row["me_residual_after_bounded"] = float(residuals[index])
        row["me_residual_z"] = float(residuals[index]) / residual_sd if residual_sd else 0.0
        if row["me_residual_z"] >= 1.5:
            row["residual_direction"] = "me_over_bounded"
        elif row["me_residual_z"] <= -1.5:
            row["residual_direction"] = "bounded_over_me"
        else:
            row["residual_direction"] = "within_1.5_sd"

    tss = float(np.sum((y - float(np.mean(y))) ** 2))
    rss = float(np.sum(residuals * residuals))
    return 1.0 - rss / tss if tss > 0 else float("nan")


def add_ranks_and_flags(rows: list[dict[str, object]]) -> None:
    n_rows = len(rows)
    top_cutoff = math.ceil(n_rows * 0.25)
    bottom_half_cutoff = math.floor(n_rows * 0.50)
    me_ranks = average_ranks([float(row["me_contrast"]) for row in rows], descending=True)
    bounded_ranks = average_ranks(
        [float(row["bounded_prediction"]) for row in rows], descending=True
    )
    ls_raw_ranks = average_ranks([float(row["ls_raw_contrast"]) for row in rows], descending=True)
    for index, row in enumerate(rows):
        row["me_rank"] = me_ranks[index]
        row["bounded_prediction_rank"] = bounded_ranks[index]
        row["ls_raw_rank"] = ls_raw_ranks[index]
        rank_shift = bounded_ranks[index] - me_ranks[index]
        row["rank_shift_me_over_bounded"] = rank_shift
        row["me_top_quartile"] = me_ranks[index] <= top_cutoff
        row["bounded_top_quartile"] = bounded_ranks[index] <= top_cutoff
        row["me_top_quartile_bounded_bottom_half"] = (
            me_ranks[index] <= top_cutoff and bounded_ranks[index] > bottom_half_cutoff
        )


def summarize_dataset(rows: list[dict[str, object]], model_r_squared: float) -> dict[str, object]:
    n_rows = len(rows)
    top_cutoff = math.ceil(n_rows * 0.25)
    bottom_cutoff = n_rows - top_cutoff + 1
    residuals = [float(row["me_residual_after_bounded"]) for row in rows]
    rank_shifts = [abs(float(row["rank_shift_me_over_bounded"])) for row in rows]

    me_ls_raw_x, me_ls_raw_y = paired_numeric(rows, "me_contrast", "ls_raw_contrast")
    me_ls_z_x, me_ls_z_y = paired_numeric(rows, "me_contrast", "ls_z_contrast")
    me_bound_x, me_bound_y = paired_numeric(rows, "me_contrast", "bounded_prediction")
    me_fc_expected_x, me_fc_expected_y = paired_numeric(
        rows, "me_contrast", "fc_expected_agreement_rate"
    )
    me_fc_selected_x, me_fc_selected_y = paired_numeric(
        rows, "me_contrast", "fc_selected_contrast"
    )
    me_yn_x, me_yn_y = paired_numeric(rows, "me_contrast", "yn_yes_contrast")

    top_overlap = [
        row
        for row in rows
        if float(row["me_rank"]) <= top_cutoff
        and float(row["bounded_prediction_rank"]) <= top_cutoff
    ]
    bottom_overlap = [
        row
        for row in rows
        if float(row["me_rank"]) >= bottom_cutoff
        and float(row["bounded_prediction_rank"]) >= bottom_cutoff
    ]

    return {
        "dataset": rows[0]["dataset"],
        "n_pairs": n_rows,
        "bounded_predictors": rows[0]["bounded_predictors"],
        "bounded_model_r_squared": finite_or_blank(model_r_squared),
        "bounded_model_residual_sd": sample_sd(residuals),
        "bounded_model_mean_abs_residual": mean([abs(value) for value in residuals]),
        "pearson_me_ls_raw": finite_or_blank(pearson(me_ls_raw_x, me_ls_raw_y)),
        "spearman_me_ls_raw": finite_or_blank(spearman(me_ls_raw_x, me_ls_raw_y)),
        "pearson_me_ls_z": finite_or_blank(pearson(me_ls_z_x, me_ls_z_y)),
        "spearman_me_ls_z": finite_or_blank(spearman(me_ls_z_x, me_ls_z_y)),
        "pearson_me_bounded_prediction": finite_or_blank(pearson(me_bound_x, me_bound_y)),
        "spearman_me_bounded_prediction": finite_or_blank(spearman(me_bound_x, me_bound_y)),
        "pearson_me_fc_expected": finite_or_blank(
            pearson(me_fc_expected_x, me_fc_expected_y)
        ),
        "pearson_me_fc_selected": finite_or_blank(
            pearson(me_fc_selected_x, me_fc_selected_y)
        ),
        "pearson_me_yn_yes": finite_or_blank(pearson(me_yn_x, me_yn_y)),
        "top_quartile_overlap_count": len(top_overlap),
        "top_quartile_overlap_rate": len(top_overlap) / top_cutoff,
        "bottom_quartile_overlap_count": len(bottom_overlap),
        "bottom_quartile_overlap_rate": len(bottom_overlap) / top_cutoff,
        "me_top_quartile_bounded_bottom_half_count": sum(
            row["me_top_quartile_bounded_bottom_half"] is True for row in rows
        ),
        "large_positive_residual_count": sum(
            float(row["me_residual_z"]) >= 1.5 for row in rows
        ),
        "large_negative_residual_count": sum(
            float(row["me_residual_z"]) <= -1.5 for row in rows
        ),
        "mean_abs_rank_shift": mean(rank_shifts),
        "max_abs_rank_shift": max(rank_shifts),
    }


def build_extremes(rows: list[dict[str, object]], max_extremes: int) -> list[dict[str, object]]:
    output = []
    directions = (
        ("me_over_bounded", lambda row: float(row["me_residual_z"]), True),
        ("bounded_over_me", lambda row: float(row["me_residual_z"]), False),
        ("absolute_rank_shift", lambda row: abs(float(row["rank_shift_me_over_bounded"])), True),
    )
    for name, key, reverse in directions:
        sorted_rows = sorted(rows, key=key, reverse=reverse)
        for rank, row in enumerate(sorted_rows[:max_extremes], start=1):
            output.append(
                {
                    "dataset": row["dataset"],
                    "extreme_type": name,
                    "rank": rank,
                    "pair_id": row["pair_id"],
                    "label": row["label"],
                    "bad_condition": row["bad_condition"],
                    "good_condition": row["good_condition"],
                    "me_contrast": row["me_contrast"],
                    "ls_raw_contrast": row["ls_raw_contrast"],
                    "bounded_prediction": row["bounded_prediction"],
                    "me_residual_after_bounded": row["me_residual_after_bounded"],
                    "me_residual_z": row["me_residual_z"],
                    "rank_shift_me_over_bounded": row["rank_shift_me_over_bounded"],
                    "fc_expected_agreement_rate": row["fc_expected_agreement_rate"],
                    "fc_selected_contrast": row["fc_selected_contrast"],
                    "yn_yes_contrast": row["yn_yes_contrast"],
                }
            )
    return output


def process_pairs(pair_rows: list[dict[str, object]], max_extremes: int) -> tuple[
    list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]
]:
    all_rows = []
    summary_rows = []
    extreme_rows = []
    for dataset in sorted({str(row["dataset"]) for row in pair_rows}):
        rows = [row for row in pair_rows if row["dataset"] == dataset]
        predictors = select_predictors(rows)
        if not predictors:
            raise SystemExit(f"No complete bounded predictors for dataset {dataset}")
        model_r_squared = fit_bounded_prediction(rows, predictors)
        add_ranks_and_flags(rows)
        all_rows.extend(rows)
        summary_rows.append(summarize_dataset(rows, model_r_squared))
        extreme_rows.extend(build_extremes(rows, max_extremes))
    return all_rows, summary_rows, extreme_rows


def manifest_rows(args: argparse.Namespace, outputs: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    timestamp = datetime.now().isoformat(timespec="seconds")
    notes = {
        "sprouse_pair_resolution_rows.csv": "Pair-level contrast rows with ME residual diagnostics.",
        "sprouse_pair_resolution_summary.csv": "Per-dataset pair-level robustness summaries.",
        "sprouse_pair_resolution_extremes.csv": "Largest residual and rank-shift pairs for audit.",
    }
    return [
        {
            "created_at": timestamp,
            "analysis": "sprouse_pair_resolution_robustness",
            "raw_root": str(args.raw_root),
            "output_file": name,
            "rows": len(rows),
            "note": notes[name],
        }
        for name, rows in outputs.items()
    ]


def main() -> None:
    args = parse_args()
    require_approved_gate(args.analysis_dir)
    require_pair_outputs(args.analysis_dir)

    summaries = condition_summaries(args.raw_root)
    pair_rows = build_pair_rows(args.analysis_dir, summaries)
    row_output, summary_output, extreme_output = process_pairs(pair_rows, args.max_extremes)

    outputs = {
        "sprouse_pair_resolution_rows.csv": row_output,
        "sprouse_pair_resolution_summary.csv": summary_output,
        "sprouse_pair_resolution_extremes.csv": extreme_output,
    }
    write_csv(args.out_dir / "sprouse_pair_resolution_rows.csv", ROW_FIELDS, row_output)
    write_csv(
        args.out_dir / "sprouse_pair_resolution_summary.csv",
        SUMMARY_FIELDS,
        summary_output,
    )
    write_csv(
        args.out_dir / "sprouse_pair_resolution_extremes.csv",
        EXTREME_FIELDS,
        extreme_output,
    )
    write_csv(
        args.out_dir / "sprouse_pair_resolution_manifest.csv",
        MANIFEST_FIELDS,
        manifest_rows(args, outputs),
    )

    for row in summary_output:
        print(
            f"{row['dataset']}: n={row['n_pairs']} "
            f"bounded_r2={row['bounded_model_r_squared']} "
            f"me_ls_raw_r={row['pearson_me_ls_raw']} "
            f"me_bounded_r={row['pearson_me_bounded_prediction']} "
            f"me_top_bounded_bottom_half={row['me_top_quartile_bounded_bottom_half_count']}"
        )


if __name__ == "__main__":
    main()
