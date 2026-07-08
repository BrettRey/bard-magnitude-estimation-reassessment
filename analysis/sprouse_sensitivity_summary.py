#!/usr/bin/env python3
"""Aggregate-unit bootstrap sensitivity summaries for the Sprouse diagnostics.

This script does not read or write participant-level data. It resamples the
aggregate condition/item/pair rows already produced by the approved Sprouse
pipeline and reports descriptive uncertainty intervals for the compact
diagnostics that appear in the manuscript.
"""

from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable

import numpy as np


SUMMARY_FIELDS = (
    "metric_group",
    "dataset",
    "unit_type",
    "source_file",
    "statistic",
    "x_signal",
    "y_signal",
    "predictors",
    "n_units",
    "point_estimate",
    "ci_level",
    "ci_low",
    "ci_high",
    "n_boot_requested",
    "n_boot_used",
    "seed",
    "note",
)

MANIFEST_FIELDS = (
    "created_at",
    "analysis",
    "output_file",
    "rows",
    "seed",
    "n_boot_requested",
    "note",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap aggregate-unit sensitivity intervals for Sprouse diagnostics."
    )
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Directory containing approved derived Sprouse outputs.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Ignored output directory for sensitivity summaries.",
    )
    parser.add_argument(
        "--bootstraps",
        type=int,
        default=5000,
        help="Number of aggregate-unit bootstrap draws per statistic.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260708,
        help="Random seed for reproducible bootstrap draws.",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
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
    if not math.isfinite(number):
        return None
    return number


def require_approved_gate(analysis_dir: Path) -> None:
    readiness_path = analysis_dir / "analysis_readiness.csv"
    if not readiness_path.exists():
        raise SystemExit(
            "Missing approved readiness manifest. Run "
            "`python3 scripts/sprouse_analysis_gate.py --reuse-status approved` first."
        )
    readiness = read_csv(readiness_path)
    status_rows = [row for row in readiness if row.get("gate") == "sprouse_reuse_status"]
    failures = [row for row in readiness if row.get("passed") != "True"]
    status = status_rows[0].get("status") if status_rows else ""
    if status != "approved" or failures:
        raise SystemExit(
            "Sprouse sensitivity summaries require all readiness gates to pass "
            "with reuse status approved."
        )


def require_sources(analysis_dir: Path) -> None:
    required = (
        "sprouse_signal_correlations.csv",
        "sprouse_item_signal_matrix.csv",
        "sprouse_pair_contrasts.csv",
        "sprouse_pair_resolution_rows.csv",
    )
    missing = [name for name in required if not (analysis_dir / name).exists()]
    if missing:
        formatted = "\n".join(f"- {name}" for name in missing)
        raise SystemExit(f"Missing required derived outputs:\n{formatted}")


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = mean(values)
    return math.sqrt(sum((value - center) ** 2 for value in values) / (len(values) - 1))


def pearson_pairs(pairs: list[tuple[float, float]]) -> float | None:
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


def paired_numeric(
    rows: list[dict[str, str]], x_column: str, y_column: str
) -> list[tuple[float, float]]:
    pairs = []
    for row in rows:
        x = as_float(row.get(x_column))
        y = as_float(row.get(y_column))
        if x is not None and y is not None:
            pairs.append((x, y))
    return pairs


def ols_r_squared(rows: list[dict[str, str]], y_column: str, predictors: list[str]) -> float | None:
    if len(rows) < len(predictors) + 2:
        return None
    y_values = []
    predictor_values: dict[str, list[float]] = {predictor: [] for predictor in predictors}
    for row in rows:
        y = as_float(row.get(y_column))
        predictor_numbers = [as_float(row.get(predictor)) for predictor in predictors]
        if y is None or any(value is None for value in predictor_numbers):
            continue
        y_values.append(y)
        for predictor, value in zip(predictors, predictor_numbers, strict=True):
            predictor_values[predictor].append(float(value))
    if len(y_values) < len(predictors) + 2 or sample_sd(y_values) == 0:
        return None

    matrix_columns = [np.ones(len(y_values))]
    for predictor in predictors:
        values = predictor_values[predictor]
        sd = sample_sd(values)
        if sd == 0:
            return None
        column = np.asarray([(value - mean(values)) / sd for value in values], dtype=float)
        matrix_columns.append(column)

    y = np.asarray(y_values, dtype=float)
    design = np.column_stack(matrix_columns)
    params, _residuals, _rank, _singular = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ params
    rss = float(np.sum((y - fitted) ** 2))
    tss = float(np.sum((y - float(np.mean(y))) ** 2))
    if tss == 0:
        return None
    return 1.0 - rss / tss


def bootstrap_statistic(
    units: list[object],
    statistic: Callable[[list[object]], float | None],
    n_boot: int,
    rng: np.random.Generator,
) -> tuple[float, float, int]:
    values: list[float] = []
    n_units = len(units)
    for _draw in range(n_boot):
        indices = rng.integers(0, n_units, size=n_units)
        sample = [units[int(index)] for index in indices]
        value = statistic(sample)
        if value is not None and math.isfinite(value):
            values.append(float(value))
    if not values:
        raise SystemExit("No valid bootstrap draws were produced.")
    low, high = np.percentile(np.asarray(values, dtype=float), [2.5, 97.5])
    return float(low), float(high), len(values)


def source_for_unit_type(unit_type: str) -> str:
    if unit_type in {"condition", "item"}:
        return "sprouse_item_signal_matrix.csv"
    if unit_type == "pair":
        return "sprouse_pair_contrasts.csv"
    raise ValueError(f"Unsupported unit type: {unit_type}")


def correlation_rows(
    analysis_dir: Path, n_boot: int, seed: int, rng: np.random.Generator
) -> list[dict[str, object]]:
    rows_by_source = {
        "sprouse_item_signal_matrix.csv": read_csv(analysis_dir / "sprouse_item_signal_matrix.csv"),
        "sprouse_pair_contrasts.csv": read_csv(analysis_dir / "sprouse_pair_contrasts.csv"),
    }
    correlation_manifest = read_csv(analysis_dir / "sprouse_signal_correlations.csv")
    output: list[dict[str, object]] = []

    for row in correlation_manifest:
        dataset = row["dataset"]
        unit_type = row["unit_type"]
        x_signal = row["x_signal"]
        y_signal = row["y_signal"]
        source_file = source_for_unit_type(unit_type)
        source_rows = [
            source_row
            for source_row in rows_by_source[source_file]
            if source_row.get("dataset") == dataset and source_row.get("unit_type", unit_type) == unit_type
        ]
        pairs = paired_numeric(source_rows, x_signal, y_signal)
        point = pearson_pairs(pairs)
        recorded = as_float(row.get("pearson_r"))
        if point is None:
            raise SystemExit(f"Could not compute correlation for {dataset} {x_signal}/{y_signal}.")
        if recorded is not None and abs(point - recorded) > 1e-9:
            raise SystemExit(
                "Recomputed correlation does not match recorded summary for "
                f"{dataset} {x_signal}/{y_signal}: {point} vs {recorded}"
            )
        low, high, used = bootstrap_statistic(
            pairs,
            lambda sample: pearson_pairs(sample),  # type: ignore[arg-type]
            n_boot,
            rng,
        )
        output.append(
            {
                "metric_group": "cross_method_correlation",
                "dataset": dataset,
                "unit_type": unit_type,
                "source_file": source_file,
                "statistic": "pearson_r",
                "x_signal": x_signal,
                "y_signal": y_signal,
                "predictors": "",
                "n_units": len(pairs),
                "point_estimate": point,
                "ci_level": "0.95",
                "ci_low": low,
                "ci_high": high,
                "n_boot_requested": n_boot,
                "n_boot_used": used,
                "seed": seed,
                "note": "Percentile bootstrap over aggregate rows; not participant-level uncertainty.",
            }
        )
    return output


def bounded_r2_rows(
    analysis_dir: Path, n_boot: int, seed: int, rng: np.random.Generator
) -> list[dict[str, object]]:
    pair_rows = read_csv(analysis_dir / "sprouse_pair_resolution_rows.csv")
    output: list[dict[str, object]] = []
    for dataset in sorted({row["dataset"] for row in pair_rows}):
        rows = [row for row in pair_rows if row["dataset"] == dataset]
        predictor_spec = next((row["bounded_predictors"] for row in rows if row["bounded_predictors"]), "")
        predictors = [predictor for predictor in predictor_spec.split(";") if predictor]
        if not predictors:
            raise SystemExit(f"No bounded predictors found for dataset {dataset}.")
        complete_rows = [
            row
            for row in rows
            if as_float(row.get("me_contrast")) is not None
            and all(as_float(row.get(predictor)) is not None for predictor in predictors)
        ]
        point = ols_r_squared(complete_rows, "me_contrast", predictors)
        if point is None:
            raise SystemExit(f"Could not compute bounded-model R2 for dataset {dataset}.")
        low, high, used = bootstrap_statistic(
            complete_rows,
            lambda sample: ols_r_squared(  # type: ignore[arg-type]
                sample, "me_contrast", predictors
            ),
            n_boot,
            rng,
        )
        output.append(
            {
                "metric_group": "pair_bounded_model",
                "dataset": dataset,
                "unit_type": "pair",
                "source_file": "sprouse_pair_resolution_rows.csv",
                "statistic": "bounded_model_r_squared",
                "x_signal": "",
                "y_signal": "me_contrast",
                "predictors": ";".join(predictors),
                "n_units": len(complete_rows),
                "point_estimate": point,
                "ci_level": "0.95",
                "ci_low": low,
                "ci_high": high,
                "n_boot_requested": n_boot,
                "n_boot_used": used,
                "seed": seed,
                "note": (
                    "Bounded-predictor regression refit within each aggregate-pair "
                    "bootstrap draw; not participant-level uncertainty."
                ),
            }
        )
    return output


def manifest_rows(
    created_at: str,
    summary_path: Path,
    summary_rows: list[dict[str, object]],
    seed: int,
    n_boot: int,
) -> list[dict[str, object]]:
    return [
        {
            "created_at": created_at,
            "analysis": "sprouse_sensitivity_summary",
            "output_file": summary_path.name,
            "rows": len(summary_rows),
            "seed": seed,
            "n_boot_requested": n_boot,
            "note": (
                "All intervals resample aggregate condition/item/pair rows from "
                "ignored derived outputs; raw participant rows are neither read nor written."
            ),
        }
    ]


def main() -> None:
    args = parse_args()
    if args.bootstraps < 100:
        raise SystemExit("--bootstraps must be at least 100 for a useful interval.")
    require_approved_gate(args.analysis_dir)
    require_sources(args.analysis_dir)

    rng = np.random.default_rng(args.seed)
    rows = []
    rows.extend(correlation_rows(args.analysis_dir, args.bootstraps, args.seed, rng))
    rows.extend(bounded_r2_rows(args.analysis_dir, args.bootstraps, args.seed, rng))

    summary_path = args.out_dir / "sprouse_sensitivity_summary.csv"
    manifest_path = args.out_dir / "sprouse_sensitivity_manifest.csv"
    created_at = datetime.now().isoformat(timespec="seconds")
    write_csv(summary_path, SUMMARY_FIELDS, rows)
    write_csv(
        manifest_path,
        MANIFEST_FIELDS,
        manifest_rows(created_at, summary_path, rows, args.seed, args.bootstraps),
    )

    print(f"Wrote {summary_path} ({len(rows)} rows)")
    print(f"Wrote {manifest_path} (1 row)")
    for row in rows:
        label = row["statistic"]
        if row["x_signal"]:
            label = f"{label} {row['x_signal']}/{row['y_signal']}"
        elif row["predictors"]:
            label = f"{label} {row['predictors']}"
        print(
            f"{row['dataset']} {row['unit_type']} {label}: "
            f"point={float(row['point_estimate']):.3f}, "
            f"95% CI [{float(row['ci_low']):.3f}, {float(row['ci_high']):.3f}]"
        )


if __name__ == "__main__":
    main()
