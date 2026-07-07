#!/usr/bin/env python3
"""First-pass dimensionality gate for the Sprouse method-comparison matrices.

This is an approximation to the chartered measurement-structure gate. It tests
whether aggregate cross-method item/contrast matrices behave like one dominant
dimension before any magnitude-estimation-specific term is adjudicated.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MatrixSpec:
    dataset: str
    unit_type: str
    source_file: str
    signals: tuple[str, ...]

    @property
    def name(self) -> str:
        return f"{self.dataset}_{self.unit_type}"


MATRICES = (
    MatrixSpec(
        dataset="2013",
        unit_type="pair",
        source_file="sprouse_pair_contrasts.csv",
        signals=("me_contrast", "ls_contrast", "fc_expected_agreement_rate"),
    ),
    MatrixSpec(
        dataset="2017",
        unit_type="item",
        source_file="sprouse_item_signal_matrix.csv",
        signals=("me_zscore", "ls_zscore", "fc_selected_rate", "yn_yes_rate"),
    ),
    MatrixSpec(
        dataset="2017",
        unit_type="pair",
        source_file="sprouse_pair_contrasts.csv",
        signals=("me_contrast", "ls_contrast", "fc_selected_contrast", "yn_yes_contrast"),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a first-pass dimensionality gate over Sprouse derived matrices."
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
        help="Ignored output directory for dimensionality diagnostics.",
    )
    parser.add_argument(
        "--permutations",
        type=int,
        default=1000,
        help="Number of column-wise permutations for parallel analysis.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260707,
        help="Random seed for reproducible parallel analysis.",
    )
    parser.add_argument(
        "--rms-residual-threshold",
        type=float,
        default=0.10,
        help="Maximum one-factor off-diagonal RMS residual for first-pass sufficiency.",
    )
    parser.add_argument(
        "--max-residual-threshold",
        type=float,
        default=0.20,
        help="Maximum one-factor absolute off-diagonal residual for first-pass sufficiency.",
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
            "Sprouse dimensionality analysis requires all readiness gates to pass "
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


def zscore_complete_cases(frame: pd.DataFrame, signals: tuple[str, ...]) -> pd.DataFrame:
    numeric = frame.loc[:, list(signals)].apply(pd.to_numeric, errors="coerce").dropna()
    if numeric.shape[0] <= numeric.shape[1]:
        raise ValueError(
            f"Need more complete rows than signals for dimensionality analysis: "
            f"{numeric.shape[0]} rows, {numeric.shape[1]} signals"
        )
    std = numeric.std(axis=0, ddof=1)
    zero_std = [column for column, value in std.items() if value == 0 or math.isnan(value)]
    if zero_std:
        raise ValueError(f"Zero-variance signal columns: {', '.join(zero_std)}")
    return (numeric - numeric.mean(axis=0)) / std


def sorted_eigendecomposition(correlation: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(correlation)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    for index in range(eigenvectors.shape[1]):
        if eigenvectors[:, index].sum() < 0:
            eigenvectors[:, index] *= -1
    return eigenvalues, eigenvectors


def component_loadings(eigenvalues: np.ndarray, eigenvectors: np.ndarray) -> np.ndarray:
    safe_eigenvalues = np.maximum(eigenvalues, 0)
    return eigenvectors * np.sqrt(safe_eigenvalues)


def reproduce_correlation(loadings: np.ndarray, n_components: int) -> np.ndarray:
    selected = loadings[:, :n_components]
    reproduced = selected @ selected.T
    np.fill_diagonal(reproduced, 1.0)
    return reproduced


def offdiag_pairs(matrix: np.ndarray) -> Iterable[tuple[int, int]]:
    for row in range(matrix.shape[0]):
        for col in range(row + 1, matrix.shape[1]):
            yield row, col


def offdiag_rms(residual: np.ndarray) -> float:
    values = [float(residual[row, col]) for row, col in offdiag_pairs(residual)]
    return math.sqrt(sum(value * value for value in values) / len(values))


def offdiag_max_abs(residual: np.ndarray) -> float:
    return max(abs(float(residual[row, col])) for row, col in offdiag_pairs(residual))


def parallel_analysis(
    standardized: pd.DataFrame, permutations: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    values = standardized.to_numpy(copy=True)
    simulated = []
    for _index in range(permutations):
        permuted = values.copy()
        for column in range(permuted.shape[1]):
            rng.shuffle(permuted[:, column])
        correlation = np.corrcoef(permuted, rowvar=False)
        eigenvalues, _eigenvectors = sorted_eigendecomposition(correlation)
        simulated.append(eigenvalues)
    simulation = np.asarray(simulated)
    return simulation.mean(axis=0), np.percentile(simulation, 95, axis=0)


def load_matrix(analysis_dir: Path, spec: MatrixSpec) -> pd.DataFrame:
    frame = pd.read_csv(analysis_dir / spec.source_file)
    filtered = frame[frame["dataset"].astype(str) == spec.dataset]
    if "unit_type" in filtered.columns:
        filtered = filtered[filtered["unit_type"] == spec.unit_type]
    if filtered.empty:
        raise ValueError(f"No rows found for {spec.name} in {spec.source_file}")
    return filtered


def analyze_matrix(
    analysis_dir: Path,
    spec: MatrixSpec,
    permutations: int,
    seed: int,
    rms_threshold: float,
    max_residual_threshold: float,
) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    frame = load_matrix(analysis_dir, spec)
    standardized = zscore_complete_cases(frame, spec.signals)
    correlation = np.corrcoef(standardized.to_numpy(), rowvar=False)
    eigenvalues, eigenvectors = sorted_eigendecomposition(correlation)
    loadings = component_loadings(eigenvalues, eigenvectors)
    parallel_mean, parallel_p95 = parallel_analysis(
        standardized, permutations, np.random.default_rng(seed)
    )

    one_factor = reproduce_correlation(loadings, 1)
    two_factor = reproduce_correlation(loadings, min(2, len(spec.signals)))
    one_residual = correlation - one_factor
    two_residual = correlation - two_factor
    one_rms = offdiag_rms(one_residual)
    one_max = offdiag_max_abs(one_residual)
    two_rms = offdiag_rms(two_residual)
    second_exceeds = bool(eigenvalues[1] > parallel_p95[1])
    one_factor_passes = (
        not second_exceeds and one_rms <= rms_threshold and one_max <= max_residual_threshold
    )
    decision = (
        "single_dimension_sufficient_first_pass"
        if one_factor_passes
        else "possible_multidimensional_structure"
    )

    summary = {
        "dataset": spec.dataset,
        "unit_type": spec.unit_type,
        "matrix": spec.name,
        "n_units": standardized.shape[0],
        "n_signals": len(spec.signals),
        "signals": "|".join(spec.signals),
        "first_eigenvalue": eigenvalues[0],
        "second_eigenvalue": eigenvalues[1],
        "first_variance_share": eigenvalues[0] / len(spec.signals),
        "second_variance_share": eigenvalues[1] / len(spec.signals),
        "second_parallel_p95": parallel_p95[1],
        "second_exceeds_parallel_p95": second_exceeds,
        "one_factor_rms_offdiag_residual": one_rms,
        "one_factor_max_abs_offdiag_residual": one_max,
        "two_factor_rms_offdiag_residual": two_rms,
        "decision": decision,
        "decision_rule": (
            "second_eigenvalue <= parallel_p95_second and "
            f"one_factor_rms <= {rms_threshold} and "
            f"one_factor_max_abs <= {max_residual_threshold}"
        ),
        "approximation_note": "PCA/parallel-analysis first pass, not final response-function model",
    }

    eigen_rows = []
    for component_index, eigenvalue in enumerate(eigenvalues, start=1):
        eigen_rows.append(
            {
                "dataset": spec.dataset,
                "unit_type": spec.unit_type,
                "matrix": spec.name,
                "component": component_index,
                "observed_eigenvalue": eigenvalue,
                "variance_share": eigenvalue / len(spec.signals),
                "parallel_mean": parallel_mean[component_index - 1],
                "parallel_p95": parallel_p95[component_index - 1],
                "exceeds_parallel_p95": bool(eigenvalue > parallel_p95[component_index - 1]),
            }
        )

    loading_rows = []
    for signal_index, signal in enumerate(spec.signals):
        for component_index in range(len(spec.signals)):
            loading_rows.append(
                {
                    "dataset": spec.dataset,
                    "unit_type": spec.unit_type,
                    "matrix": spec.name,
                    "signal": signal,
                    "component": component_index + 1,
                    "loading": loadings[signal_index, component_index],
                }
            )

    residual_rows = []
    for row, col in offdiag_pairs(correlation):
        residual_rows.append(
            {
                "dataset": spec.dataset,
                "unit_type": spec.unit_type,
                "matrix": spec.name,
                "signal_x": spec.signals[row],
                "signal_y": spec.signals[col],
                "observed_correlation": correlation[row, col],
                "one_factor_reproduced": one_factor[row, col],
                "one_factor_residual": one_residual[row, col],
                "two_factor_reproduced": two_factor[row, col],
                "two_factor_residual": two_residual[row, col],
            }
        )

    return summary, eigen_rows, loading_rows, residual_rows


def write_manifest(args: argparse.Namespace) -> None:
    rows = [
        {"key": "analysis", "value": "sprouse_dimensionality_gate"},
        {"key": "status", "value": "first_pass_approximation"},
        {"key": "permission_status", "value": "approved"},
        {"key": "input_directory", "value": str(args.analysis_dir)},
        {"key": "output_directory", "value": str(args.out_dir)},
        {"key": "permutations", "value": args.permutations},
        {"key": "seed", "value": args.seed},
        {"key": "rms_residual_threshold", "value": args.rms_residual_threshold},
        {"key": "max_residual_threshold", "value": args.max_residual_threshold},
        {
            "key": "scope_note",
            "value": (
                "PCA/parallel-analysis dimensionality gate over aggregate signals; "
                "not a final response-function or confirmatory factor model."
            ),
        },
    ]
    write_csv(args.out_dir / "sprouse_dimensionality_manifest.csv", ("key", "value"), rows)


def main() -> int:
    args = parse_args()
    require_approved_gate(args.analysis_dir)
    require_descriptive_outputs(args.analysis_dir)

    summaries: list[dict[str, object]] = []
    eigen_rows: list[dict[str, object]] = []
    loading_rows: list[dict[str, object]] = []
    residual_rows: list[dict[str, object]] = []
    for index, spec in enumerate(MATRICES):
        summary, matrix_eigen, matrix_loadings, matrix_residuals = analyze_matrix(
            analysis_dir=args.analysis_dir,
            spec=spec,
            permutations=args.permutations,
            seed=args.seed + index,
            rms_threshold=args.rms_residual_threshold,
            max_residual_threshold=args.max_residual_threshold,
        )
        summaries.append(summary)
        eigen_rows.extend(matrix_eigen)
        loading_rows.extend(matrix_loadings)
        residual_rows.extend(matrix_residuals)

    write_csv(
        args.out_dir / "sprouse_dimensionality_gate_summary.csv",
        (
            "dataset",
            "unit_type",
            "matrix",
            "n_units",
            "n_signals",
            "signals",
            "first_eigenvalue",
            "second_eigenvalue",
            "first_variance_share",
            "second_variance_share",
            "second_parallel_p95",
            "second_exceeds_parallel_p95",
            "one_factor_rms_offdiag_residual",
            "one_factor_max_abs_offdiag_residual",
            "two_factor_rms_offdiag_residual",
            "decision",
            "decision_rule",
            "approximation_note",
        ),
        summaries,
    )
    write_csv(
        args.out_dir / "sprouse_dimensionality_eigenvalues.csv",
        (
            "dataset",
            "unit_type",
            "matrix",
            "component",
            "observed_eigenvalue",
            "variance_share",
            "parallel_mean",
            "parallel_p95",
            "exceeds_parallel_p95",
        ),
        eigen_rows,
    )
    write_csv(
        args.out_dir / "sprouse_dimensionality_loadings.csv",
        ("dataset", "unit_type", "matrix", "signal", "component", "loading"),
        loading_rows,
    )
    write_csv(
        args.out_dir / "sprouse_dimensionality_residuals.csv",
        (
            "dataset",
            "unit_type",
            "matrix",
            "signal_x",
            "signal_y",
            "observed_correlation",
            "one_factor_reproduced",
            "one_factor_residual",
            "two_factor_reproduced",
            "two_factor_residual",
        ),
        residual_rows,
    )
    write_manifest(args)

    decisions = ", ".join(f"{row['matrix']}={row['decision']}" for row in summaries)
    print(f"Wrote dimensionality diagnostics to {args.out_dir}")
    print(decisions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
