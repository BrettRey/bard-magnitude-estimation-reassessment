#!/usr/bin/env python3
"""Response-function diagnostics for the Sprouse ME-vs-Likert data.

This script asks whether raw bounded Likert means behave as if they are a
saturating response function of the unbounded ME aggregate. It is a targeted
diagnostic for Bard-style resolution claims, not a claim that ME is the true
latent acceptability scale.
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
from scipy.optimize import curve_fit


RESULT_HEADER_NAMES = {"participant", "subject"}


@dataclass(frozen=True)
class RawSpec:
    dataset: str
    unit_type: str
    unit_column: str
    me_path: Path
    ls_path: Path

    @property
    def name(self) -> str:
        return f"{self.dataset}_{self.unit_type}"


@dataclass(frozen=True)
class FitResult:
    model: str
    params: tuple[float, float] | None
    fitted: np.ndarray
    residuals: np.ndarray
    rss: float | None
    rmse: float | None
    aic: float | None
    r_squared: float | None


MODEL_FIELDS = (
    "dataset",
    "unit_type",
    "model",
    "x_signal",
    "y_signal",
    "n_units",
    "rss",
    "rmse",
    "aic",
    "delta_aic_from_best",
    "r_squared",
    "intercept",
    "slope",
)

BIN_FIELDS = (
    "dataset",
    "unit_type",
    "likert_band",
    "n_units",
    "ls_raw_min",
    "ls_raw_mean",
    "ls_raw_max",
    "ls_raw_range",
    "me_z_min",
    "me_z_mean",
    "me_z_max",
    "me_z_sd",
    "me_z_range",
    "linear_residual_sd",
    "bounded_logistic_residual_sd",
    "linear_mean_abs_residual",
    "bounded_logistic_mean_abs_residual",
)

RESIDUAL_FIELDS = (
    "dataset",
    "unit_type",
    "unit_id",
    "likert_band",
    "me_z_mean",
    "ls_raw_mean",
    "me_n",
    "ls_n",
    "linear_fitted",
    "linear_residual",
    "bounded_logistic_fitted",
    "bounded_logistic_residual",
)

MANIFEST_FIELDS = (
    "created_at",
    "analysis",
    "raw_root",
    "output_file",
    "rows",
    "note",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run response-function diagnostics for Sprouse ME and Likert data."
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
        help="Ignored output directory for response-function diagnostics.",
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
            "Sprouse response-function analysis requires all readiness gates to pass "
            "with reuse status approved."
        )


def require_descriptive_outputs(analysis_dir: Path) -> None:
    required = {
        "sprouse_item_signal_matrix.csv",
        "sprouse_pair_contrasts.csv",
        "sprouse_signal_correlations.csv",
    }
    missing = [analysis_dir / name for name in sorted(required) if not (analysis_dir / name).exists()]
    if missing:
        for path in missing:
            print(f"Missing input: {path}")
        raise SystemExit(
            "Missing descriptive outputs. Run `python3 analysis/sprouse_item_signal.py` first."
        )


def raw_specs(raw_root: Path) -> tuple[RawSpec, ...]:
    return (
        RawSpec(
            dataset="2013",
            unit_type="condition",
            unit_column="condition",
            me_path=raw_root / "Sprouse2013/SSA.data/ME experiment/LI.me.results.csv",
            ls_path=raw_root / "Sprouse2013/SSA.data/LS experiment/LI.ls.results.csv",
        ),
        RawSpec(
            dataset="2017",
            unit_type="item",
            unit_column="item",
            me_path=raw_root / "Sprouse2017/SA2017.data/ME.results.csv",
            ls_path=raw_root / "Sprouse2017/SA2017.data/LS.results.csv",
        ),
    )


def aggregate_signal(
    rows: list[dict[str, str]], unit_column: str, value_column: str
) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        unit_id = (row.get(unit_column) or "").strip()
        value = as_float(row.get(value_column))
        if unit_id and value is not None:
            grouped[unit_id].append(value)
    return {
        unit_id: {
            "n": len(values),
            "mean": mean(values),
            "sd": sample_sd(values),
            "min": min(values),
            "max": max(values),
        }
        for unit_id, values in grouped.items()
        if values
    }


def build_response_rows(spec: RawSpec) -> list[dict[str, object]]:
    for path in (spec.me_path, spec.ls_path):
        if not path.exists():
            raise SystemExit(f"Missing raw Sprouse file: {path}")

    me_rows = read_result_csv(spec.me_path)
    ls_rows = read_result_csv(spec.ls_path)
    me_summary = aggregate_signal(me_rows, spec.unit_column, "zscores")
    ls_summary = aggregate_signal(ls_rows, spec.unit_column, "judgment")

    complete_units = sorted(set(me_summary) & set(ls_summary))
    output = []
    for unit_id in complete_units:
        me = me_summary[unit_id]
        ls = ls_summary[unit_id]
        output.append(
            {
                "dataset": spec.dataset,
                "unit_type": spec.unit_type,
                "unit_id": unit_id,
                "me_z_mean": me["mean"],
                "me_n": me["n"],
                "ls_raw_mean": ls["mean"],
                "ls_n": ls["n"],
            }
        )

    if len(output) < 3:
        raise ValueError(f"Too few complete units for {spec.name}: {len(output)}")
    return output


def linear_predict(x: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    return intercept + slope * x


def bounded_logistic_predict(x: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    eta = np.clip(intercept + slope * x, -60.0, 60.0)
    return 1.0 + 6.0 / (1.0 + np.exp(-eta))


def fit_statistics(y: np.ndarray, fitted: np.ndarray, parameter_count: int) -> tuple[float, float, float, float]:
    residuals = y - fitted
    rss = float(np.sum(residuals * residuals))
    rmse = float(math.sqrt(rss / len(y)))
    safe_rss = max(rss, np.finfo(float).tiny)
    aic = float(len(y) * math.log(safe_rss / len(y)) + 2 * parameter_count)
    tss = float(np.sum((y - float(np.mean(y))) ** 2))
    r_squared = float(1.0 - rss / tss) if tss > 0 else float("nan")
    return rss, rmse, aic, r_squared


def fit_linear(x: np.ndarray, y: np.ndarray) -> FitResult:
    design = np.column_stack([np.ones_like(x), x])
    params, _residuals, _rank, _singular = np.linalg.lstsq(design, y, rcond=None)
    intercept = float(params[0])
    slope = float(params[1])
    fitted = linear_predict(x, intercept, slope)
    residuals = y - fitted
    rss, rmse, aic, r_squared = fit_statistics(y, fitted, 2)
    return FitResult(
        model="linear",
        params=(intercept, slope),
        fitted=fitted,
        residuals=residuals,
        rss=rss,
        rmse=rmse,
        aic=aic,
        r_squared=r_squared,
    )


def initial_logistic_params(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    scaled = np.clip((y - 1.0) / 6.0, 1e-6, 1.0 - 1e-6)
    logits = np.log(scaled / (1.0 - scaled))
    design = np.column_stack([np.ones_like(x), x])
    params, _residuals, _rank, _singular = np.linalg.lstsq(design, logits, rcond=None)
    intercept = float(params[0])
    slope = max(float(params[1]), 1e-6)
    return intercept, slope


def fit_bounded_logistic(x: np.ndarray, y: np.ndarray) -> FitResult:
    try:
        p0 = initial_logistic_params(x, y)
        params, _covariance = curve_fit(
            bounded_logistic_predict,
            x,
            y,
            p0=p0,
            bounds=([-np.inf, 0.0], [np.inf, np.inf]),
            maxfev=20000,
        )
    except (RuntimeError, ValueError, FloatingPointError):
        nan_values = np.full_like(y, np.nan, dtype=float)
        return FitResult(
            model="bounded_logistic_1_7",
            params=None,
            fitted=nan_values,
            residuals=nan_values,
            rss=None,
            rmse=None,
            aic=None,
            r_squared=None,
        )

    intercept = float(params[0])
    slope = float(params[1])
    fitted = bounded_logistic_predict(x, intercept, slope)
    residuals = y - fitted
    rss, rmse, aic, r_squared = fit_statistics(y, fitted, 2)
    return FitResult(
        model="bounded_logistic_1_7",
        params=(intercept, slope),
        fitted=fitted,
        residuals=residuals,
        rss=rss,
        rmse=rmse,
        aic=aic,
        r_squared=r_squared,
    )


def assign_likert_bands(rows: list[dict[str, object]]) -> None:
    ordered = sorted(
        range(len(rows)),
        key=lambda index: (float(rows[index]["ls_raw_mean"]), str(rows[index]["unit_id"])),
    )
    n_rows = len(rows)
    for rank, index in enumerate(ordered):
        percentile = (rank + 0.5) / n_rows
        if percentile <= 0.10:
            band = "lower_endpoint"
        elif percentile <= 0.30:
            band = "lower_middle"
        elif percentile <= 0.70:
            band = "middle"
        elif percentile <= 0.90:
            band = "upper_middle"
        else:
            band = "upper_endpoint"
        rows[index]["likert_band"] = band


def summarize_band(rows: list[dict[str, object]], band: str) -> dict[str, object]:
    selected = [row for row in rows if row["likert_band"] == band]
    ls_values = [float(row["ls_raw_mean"]) for row in selected]
    me_values = [float(row["me_z_mean"]) for row in selected]
    linear_residuals = [float(row["linear_residual"]) for row in selected]
    logistic_residuals = [
        float(row["bounded_logistic_residual"])
        for row in selected
        if row["bounded_logistic_residual"] != ""
    ]

    return {
        "likert_band": band,
        "n_units": len(selected),
        "ls_raw_min": min(ls_values),
        "ls_raw_mean": mean(ls_values),
        "ls_raw_max": max(ls_values),
        "ls_raw_range": max(ls_values) - min(ls_values),
        "me_z_min": min(me_values),
        "me_z_mean": mean(me_values),
        "me_z_max": max(me_values),
        "me_z_sd": sample_sd(me_values),
        "me_z_range": max(me_values) - min(me_values),
        "linear_residual_sd": sample_sd(linear_residuals),
        "bounded_logistic_residual_sd": sample_sd(logistic_residuals)
        if logistic_residuals
        else "",
        "linear_mean_abs_residual": mean([abs(value) for value in linear_residuals]),
        "bounded_logistic_mean_abs_residual": mean([abs(value) for value in logistic_residuals])
        if logistic_residuals
        else "",
    }


def add_fit_rows(
    output: list[dict[str, object]],
    dataset: str,
    unit_type: str,
    n_units: int,
    fits: list[FitResult],
) -> None:
    finite_aics = [fit.aic for fit in fits if fit.aic is not None and math.isfinite(fit.aic)]
    best_aic = min(finite_aics) if finite_aics else None
    for fit in fits:
        intercept = slope = ""
        if fit.params is not None:
            intercept, slope = fit.params
        delta_aic = (
            fit.aic - best_aic
            if fit.aic is not None and best_aic is not None and math.isfinite(fit.aic)
            else None
        )
        output.append(
            {
                "dataset": dataset,
                "unit_type": unit_type,
                "model": fit.model,
                "x_signal": "me_z_mean",
                "y_signal": "ls_raw_mean",
                "n_units": n_units,
                "rss": finite_or_blank(fit.rss),
                "rmse": finite_or_blank(fit.rmse),
                "aic": finite_or_blank(fit.aic),
                "delta_aic_from_best": finite_or_blank(delta_aic),
                "r_squared": finite_or_blank(fit.r_squared),
                "intercept": intercept,
                "slope": slope,
            }
        )


def add_residual_columns(rows: list[dict[str, object]], fits: dict[str, FitResult]) -> None:
    linear = fits["linear"]
    logistic = fits["bounded_logistic_1_7"]
    for index, row in enumerate(rows):
        row["linear_fitted"] = float(linear.fitted[index])
        row["linear_residual"] = float(linear.residuals[index])
        if logistic.params is None:
            row["bounded_logistic_fitted"] = ""
            row["bounded_logistic_residual"] = ""
        else:
            row["bounded_logistic_fitted"] = float(logistic.fitted[index])
            row["bounded_logistic_residual"] = float(logistic.residuals[index])


def response_outputs(spec: RawSpec) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    rows = build_response_rows(spec)
    x = np.asarray([float(row["me_z_mean"]) for row in rows], dtype=float)
    y = np.asarray([float(row["ls_raw_mean"]) for row in rows], dtype=float)

    linear = fit_linear(x, y)
    logistic = fit_bounded_logistic(x, y)
    fits = {"linear": linear, "bounded_logistic_1_7": logistic}

    assign_likert_bands(rows)
    add_residual_columns(rows, fits)

    model_rows: list[dict[str, object]] = []
    add_fit_rows(model_rows, spec.dataset, spec.unit_type, len(rows), [linear, logistic])

    bin_rows: list[dict[str, object]] = []
    for band in ("lower_endpoint", "lower_middle", "middle", "upper_middle", "upper_endpoint"):
        summary = summarize_band(rows, band)
        summary["dataset"] = spec.dataset
        summary["unit_type"] = spec.unit_type
        bin_rows.append(summary)

    residual_rows = [
        {
            "dataset": row["dataset"],
            "unit_type": row["unit_type"],
            "unit_id": row["unit_id"],
            "likert_band": row["likert_band"],
            "me_z_mean": row["me_z_mean"],
            "ls_raw_mean": row["ls_raw_mean"],
            "me_n": row["me_n"],
            "ls_n": row["ls_n"],
            "linear_fitted": row["linear_fitted"],
            "linear_residual": row["linear_residual"],
            "bounded_logistic_fitted": row["bounded_logistic_fitted"],
            "bounded_logistic_residual": row["bounded_logistic_residual"],
        }
        for row in rows
    ]
    return model_rows, bin_rows, residual_rows


def manifest_rows(args: argparse.Namespace, outputs: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    timestamp = datetime.now().isoformat(timespec="seconds")
    notes = {
        "sprouse_response_function_model_fits.csv": (
            "Bounded Likert response-function fits; no participant rows written."
        ),
        "sprouse_response_function_bins.csv": (
            "Likert-band ME-spread diagnostics; endpoint labels are quantile diagnostics."
        ),
        "sprouse_response_function_residuals.csv": (
            "Per-unit fitted values and residuals for audit and plotting."
        ),
    }
    return [
        {
            "created_at": timestamp,
            "analysis": "sprouse_response_function_resolution",
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
    require_descriptive_outputs(args.analysis_dir)

    all_model_rows: list[dict[str, object]] = []
    all_bin_rows: list[dict[str, object]] = []
    all_residual_rows: list[dict[str, object]] = []

    for spec in raw_specs(args.raw_root):
        model_rows, bin_rows, residual_rows = response_outputs(spec)
        all_model_rows.extend(model_rows)
        all_bin_rows.extend(bin_rows)
        all_residual_rows.extend(residual_rows)

    outputs = {
        "sprouse_response_function_model_fits.csv": all_model_rows,
        "sprouse_response_function_bins.csv": all_bin_rows,
        "sprouse_response_function_residuals.csv": all_residual_rows,
    }
    write_csv(
        args.out_dir / "sprouse_response_function_model_fits.csv",
        MODEL_FIELDS,
        all_model_rows,
    )
    write_csv(
        args.out_dir / "sprouse_response_function_bins.csv",
        BIN_FIELDS,
        all_bin_rows,
    )
    write_csv(
        args.out_dir / "sprouse_response_function_residuals.csv",
        RESIDUAL_FIELDS,
        all_residual_rows,
    )
    write_csv(
        args.out_dir / "sprouse_response_function_manifest.csv",
        MANIFEST_FIELDS,
        manifest_rows(args, outputs),
    )

    for row in all_model_rows:
        print(
            f"{row['dataset']} {row['unit_type']} {row['model']}: "
            f"n={row['n_units']} r2={row['r_squared']} "
            f"aic={row['aic']} delta={row['delta_aic_from_best']}"
        )


if __name__ == "__main__":
    main()
