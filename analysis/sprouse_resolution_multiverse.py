#!/usr/bin/env python3
"""Bounded robustness multiverse for the Sprouse ME reassessment.

The analysis is deliberately aggregate-facing. Participant-level rows are read
locally to construct alternative scores, but no participant identifier or row is
written. The specification universe is frozen in
``notes/sprouse-resolution-multiverse-plan.md``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np
import pandas as pd
from scipy.stats import rankdata


SEED = 20260829
ME_SCORES = ("provided_z", "log_subject_z", "subject_percentile")
LS_SCORES = ("provided_z", "raw_mean", "subject_percentile")
ENDPOINT_RULES = ("fixed", "quintile", "quartile")
SPREADS = ("sd", "iqr", "mad")
MAPPINGS = ("raw_ols", "rank_ols")


@dataclass(frozen=True)
class DatasetPaths:
    dataset: str
    subject: str
    me: Path
    ls: Path
    fc: Path
    yn: Path | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the bounded Sprouse resolution multiverse."
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
        help="Directory produced by build_sprouse_crosswalks.py.",
    )
    parser.add_argument(
        "--analysis-dir",
        type=Path,
        default=Path("data/derived/sprouse_analysis"),
        help="Directory containing the approved primary-analysis outputs.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/derived/sprouse_multiverse"),
        help="Ignored output directory for aggregate multiverse products.",
    )
    parser.add_argument("--permutations", type=int, default=5000)
    parser.add_argument("--cv-repeats", type=int, default=50)
    parser.add_argument("--cv-folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--source-archive",
        action="append",
        default=[],
        type=Path,
        help="Downloaded archive/material file to hash in the manifest; repeatable.",
    )
    return parser.parse_args()


def dataset_paths(raw_root: Path) -> dict[str, DatasetPaths]:
    return {
        "2013": DatasetPaths(
            dataset="2013",
            subject="participant",
            me=raw_root
            / "Sprouse2013/SSA.data/ME experiment/LI.me.results.csv",
            ls=raw_root
            / "Sprouse2013/SSA.data/LS experiment/LI.ls.results.csv",
            fc=raw_root
            / "Sprouse2013/SSA.data/FC experiment/FC.logistic.csv",
            yn=None,
        ),
        "2017": DatasetPaths(
            dataset="2017",
            subject="subject",
            me=raw_root / "Sprouse2017/SA2017.data/ME.results.csv",
            ls=raw_root / "Sprouse2017/SA2017.data/LS.results.csv",
            fc=raw_root / "Sprouse2017/SA2017.data/FC.results.csv",
            yn=raw_root / "Sprouse2017/SA2017.data/YN.results.csv",
        ),
    }


def require_files(paths: Iterable[Path]) -> None:
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))


def read_public_csv(path: Path) -> pd.DataFrame:
    last_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "mac_roman", "cp1252", "latin-1"):
        try:
            return pd.read_csv(
                path, skiprows=5, low_memory=False, encoding=encoding
            )
        except UnicodeDecodeError as error:
            last_error = error
    assert last_error is not None
    raise last_error


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def ensure_approved(analysis_dir: Path) -> None:
    readiness = read_csv(analysis_dir / "analysis_readiness.csv")
    failed = readiness.loc[readiness["passed"].astype(str).str.lower() != "true"]
    if not failed.empty:
        raise RuntimeError("The approved Sprouse readiness gate is not clear.")
    reuse = readiness.loc[readiness["gate"] == "sprouse_reuse_status", "status"]
    if reuse.empty or str(reuse.iloc[0]).lower() != "approved":
        raise RuntimeError("Sprouse reuse status is not recorded as approved.")


def z_within(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    present = numeric.notna()
    mean = numeric.mean()
    sd = numeric.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        output = pd.Series(np.nan, index=values.index, dtype=float)
        output.loc[present] = 0.0
        return output
    return (numeric - mean) / sd


def add_scores(frame: pd.DataFrame, subject: str, method: str) -> pd.DataFrame:
    data = frame.copy()
    data["judgment"] = pd.to_numeric(data["judgment"], errors="coerce")
    data["zscores"] = pd.to_numeric(data["zscores"], errors="coerce")
    data = data.dropna(subset=[subject, "condition"])
    data["subject_percentile"] = data.groupby(subject, sort=False)["judgment"].rank(
        method="average", pct=True
    )
    data["provided_z"] = data["zscores"]
    if method == "me":
        data["log_judgment"] = np.nan
        positive = data["judgment"] > 0
        data.loc[positive, "log_judgment"] = np.log(
            data.loc[positive, "judgment"]
        )
        data["log_subject_z"] = data.groupby(subject, sort=False)[
            "log_judgment"
        ].transform(z_within)
    else:
        data["raw_mean"] = data["judgment"]
    return data


def aggregate_scores(
    frame: pd.DataFrame, method: str, unit: str
) -> tuple[dict[str, dict[str, float]], dict[str, int]]:
    score_names = ME_SCORES if method == "me" else LS_SCORES
    grouped = frame.groupby(unit, sort=False)
    maps: dict[str, dict[str, float]] = {}
    for score in score_names:
        maps[score] = grouped[score].mean().astype(float).to_dict()
    counts = grouped["provided_z"].count().astype(int).to_dict()
    return maps, counts


def compact(value: str) -> str:
    return "".join(str(value).split()).casefold()


def resolve(mapping: dict[str, float], key: str) -> float:
    if key in mapping:
        return float(mapping[key])
    compact_map = {compact(candidate): value for candidate, value in mapping.items()}
    wanted = compact(key)
    if wanted not in compact_map:
        raise KeyError(f"No score found for {key!r}")
    return float(compact_map[wanted])


def pair_contrast(mapping: dict[str, float], bad: str, good: str) -> float:
    return resolve(mapping, good) - resolve(mapping, bad)


def output_rows_to_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_seed(seed: int, *parts: str) -> int:
    label = "|".join((str(seed), *parts)).encode("utf-8")
    return int.from_bytes(hashlib.sha256(label).digest()[:8], "big") % (2**32)


def build_unit_rows(
    analysis_dir: Path,
    me_maps: dict[str, dict[str, dict[str, float]]],
    ls_maps: dict[str, dict[str, dict[str, float]]],
    me_counts: dict[str, dict[str, int]],
    ls_counts: dict[str, dict[str, int]],
) -> list[dict[str, object]]:
    inventory = read_csv(analysis_dir / "sprouse_item_signal_matrix.csv")
    rows: list[dict[str, object]] = []
    for record in inventory.to_dict("records"):
        dataset = str(record["dataset"])
        unit_id = str(record["unit_id"])
        row: dict[str, object] = {
            "dataset": dataset,
            "unit_type": record["unit_type"],
            "unit_id": unit_id,
        }
        for score in ME_SCORES:
            row[f"me_{score}"] = resolve(me_maps[dataset][score], unit_id)
        for score in LS_SCORES:
            row[f"ls_{score}"] = resolve(ls_maps[dataset][score], unit_id)
        row["me_n"] = int(resolve(me_counts[dataset], unit_id))
        row["ls_n"] = int(resolve(ls_counts[dataset], unit_id))
        rows.append(row)
    return rows


def logistic_target_2013(
    fc_path: Path, crosswalk: pd.DataFrame
) -> dict[int, float]:
    fc = read_public_csv(fc_path)
    fc["judgment"] = pd.to_numeric(fc["judgment"], errors="coerce")
    means = fc.dropna(subset=["condition", "judgment"]).groupby("condition")[
        "judgment"
    ].mean().to_dict()
    targets: dict[int, float] = {}
    for row in crosswalk.to_dict("records"):
        targets[int(row["pair_index"])] = pair_contrast(
            means, str(row["fc_bad_condition"]), str(row["fc_good_condition"])
        )
    return targets


def build_pair_rows(
    analysis_dir: Path,
    derived_dir: Path,
    paths: dict[str, DatasetPaths],
    me_maps: dict[str, dict[str, dict[str, float]]],
    ls_maps: dict[str, dict[str, dict[str, float]]],
) -> list[dict[str, object]]:
    pairs = read_csv(analysis_dir / "sprouse_pair_contrasts.csv")
    crosswalk_2013 = read_csv(derived_dir / "2013_condition_crosswalk.csv")
    logistic_2013 = logistic_target_2013(paths["2013"].fc, crosswalk_2013)
    rows: list[dict[str, object]] = []
    for record in pairs.to_dict("records"):
        dataset = str(record["dataset"])
        pair_id = str(record["pair_id"])
        bad = str(record["bad_condition"])
        good = str(record["good_condition"])
        row: dict[str, object] = {
            "dataset": dataset,
            "pair_id": pair_id,
            "bad_condition": bad,
            "good_condition": good,
        }
        for score in ME_SCORES:
            row[f"me_{score}"] = pair_contrast(
                me_maps[dataset][score], bad, good
            )
        for score in LS_SCORES:
            row[f"ls_{score}"] = pair_contrast(
                ls_maps[dataset][score], bad, good
            )
        if dataset == "2013":
            row["target_fc_sign"] = float(record["fc_expected_agreement_rate"]) - 0.5
            row["target_fc_logistic"] = logistic_2013[int(pair_id)]
            row["target_fc"] = ""
            row["target_yn"] = ""
        else:
            row["target_fc_sign"] = ""
            row["target_fc_logistic"] = ""
            row["target_fc"] = float(record["fc_selected_contrast"])
            row["target_yn"] = float(record["yn_yes_contrast"])
        rows.append(row)
    return rows


def spread_sd(values: np.ndarray) -> float:
    return float(np.std(values, ddof=1))


def spread_iqr(values: np.ndarray) -> float:
    return float(np.quantile(values, 0.75) - np.quantile(values, 0.25))


def spread_mad(values: np.ndarray) -> float:
    median = np.median(values)
    return float(np.median(np.abs(values - median)))


SPREAD_FUNCTIONS: dict[str, Callable[[np.ndarray], float]] = {
    "sd": spread_sd,
    "iqr": spread_iqr,
    "mad": spread_mad,
}


def endpoint_masks(ls_raw: np.ndarray, rule: str) -> tuple[np.ndarray, ...]:
    if rule == "fixed":
        return (
            ls_raw <= 2.5,
            (ls_raw >= 3.5) & (ls_raw <= 4.5),
            ls_raw >= 5.5,
        )
    if rule == "quintile":
        q20, q40, q60, q80 = np.quantile(ls_raw, [0.2, 0.4, 0.6, 0.8])
        return ls_raw <= q20, (ls_raw >= q40) & (ls_raw <= q60), ls_raw >= q80
    if rule == "quartile":
        q25, q375, q625, q75 = np.quantile(ls_raw, [0.25, 0.375, 0.625, 0.75])
        return ls_raw <= q25, (ls_raw >= q375) & (ls_raw <= q625), ls_raw >= q75
    raise ValueError(f"Unknown endpoint rule: {rule}")


def endpoint_statistic(
    me: np.ndarray,
    masks: tuple[np.ndarray, np.ndarray, np.ndarray],
    spread_name: str,
) -> tuple[float, float, float, float, float]:
    function = SPREAD_FUNCTIONS[spread_name]
    lower = function(me[masks[0]])
    middle = function(me[masks[1]])
    upper = function(me[masks[2]])
    if not np.isfinite(middle) or middle <= 0:
        return lower, middle, upper, math.nan, math.nan
    return lower, middle, upper, lower / middle, upper / middle


def endpoint_multiverse(
    unit_rows: list[dict[str, object]], permutations: int, seed: int
) -> list[dict[str, object]]:
    frame = pd.DataFrame(unit_rows)
    rows: list[dict[str, object]] = []
    for dataset, dataset_frame in frame.groupby("dataset", sort=True):
        ls_raw = dataset_frame["ls_raw_mean"].to_numpy(dtype=float)
        for me_score in ME_SCORES:
            me = dataset_frame[f"me_{me_score}"].to_numpy(dtype=float)
            for endpoint_rule in ENDPOINT_RULES:
                masks = endpoint_masks(ls_raw, endpoint_rule)
                counts = [int(mask.sum()) for mask in masks]
                for spread_name in SPREADS:
                    lower, middle, upper, lower_ratio, upper_ratio = endpoint_statistic(
                        me, masks, spread_name
                    )
                    admissible = min(counts) >= 10 and np.isfinite(
                        [lower_ratio, upper_ratio]
                    ).all()
                    probability: float | str = ""
                    observed_min: float | str = ""
                    if admissible:
                        observed_min = min(lower_ratio, upper_ratio)
                        rng = np.random.default_rng(
                            stable_seed(
                                seed,
                                str(dataset),
                                me_score,
                                endpoint_rule,
                                spread_name,
                            )
                        )
                        at_least = 0
                        for _ in range(permutations):
                            permuted = rng.permutation(me)
                            *_, perm_lower_ratio, perm_upper_ratio = endpoint_statistic(
                                permuted, masks, spread_name
                            )
                            perm_min = min(perm_lower_ratio, perm_upper_ratio)
                            if np.isfinite(perm_min) and perm_min >= observed_min:
                                at_least += 1
                        probability = (at_least + 1) / (permutations + 1)
                    ordinary = bool(
                        admissible and lower_ratio > 1.0 and upper_ratio > 1.0
                    )
                    notable = bool(
                        admissible
                        and lower_ratio >= 1.25
                        and upper_ratio >= 1.25
                        and float(probability) < 0.05
                    )
                    rows.append(
                        {
                            "dataset": dataset,
                            "me_score": me_score,
                            "endpoint_rule": endpoint_rule,
                            "spread": spread_name,
                            "n_lower": counts[0],
                            "n_middle": counts[1],
                            "n_upper": counts[2],
                            "lower_spread": lower,
                            "middle_spread": middle,
                            "upper_spread": upper,
                            "lower_middle_ratio": lower_ratio,
                            "upper_middle_ratio": upper_ratio,
                            "minimum_endpoint_ratio": observed_min,
                            "permutation_probability": probability,
                            "admissible": admissible,
                            "ordinary_support": ordinary,
                            "notable_support": notable,
                        }
                    )
    return rows


def standardize_train_test(
    train: np.ndarray, test: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    mean = train.mean(axis=0)
    sd = train.std(axis=0, ddof=0)
    sd = np.where(sd == 0, 1.0, sd)
    return (train - mean) / sd, (test - mean) / sd


def empirical_percentile(train: np.ndarray, values: np.ndarray) -> np.ndarray:
    ordered = np.sort(train)
    left = np.searchsorted(ordered, values, side="left")
    right = np.searchsorted(ordered, values, side="right")
    return (left + right + 1) / (2 * (len(ordered) + 1))


def rank_train_test(
    train: np.ndarray, test: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    train_rank = rankdata(train, method="average") / (len(train) + 1)
    test_rank = empirical_percentile(train, test)
    return train_rank, test_rank


def ols_predict(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray) -> np.ndarray:
    design_train = np.column_stack([np.ones(len(x_train)), x_train])
    design_test = np.column_stack([np.ones(len(x_test)), x_test])
    coefficients, *_ = np.linalg.lstsq(design_train, y_train, rcond=None)
    return design_test @ coefficients


def r_squared(actual: np.ndarray, predicted: np.ndarray) -> float:
    denominator = float(np.sum((actual - actual.mean()) ** 2))
    if denominator == 0:
        return math.nan
    return 1.0 - float(np.sum((actual - predicted) ** 2)) / denominator


def fold_assignments(n: int, folds: int, rng: np.random.Generator) -> list[np.ndarray]:
    indices = rng.permutation(n)
    return [part for part in np.array_split(indices, folds) if len(part)]


def cv_model_scores(
    x_ls: np.ndarray,
    x_me: np.ndarray,
    target: np.ndarray,
    mapping: str,
    repeats: int,
    folds: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(target)
    rng = np.random.default_rng(seed)
    ls_scores: list[float] = []
    me_scores: list[float] = []
    full_scores: list[float] = []
    for _ in range(repeats):
        split = fold_assignments(n, folds, rng)
        actual_parts: list[np.ndarray] = []
        predicted_ls: list[np.ndarray] = []
        predicted_me: list[np.ndarray] = []
        predicted_full: list[np.ndarray] = []
        for test_index in split:
            train_mask = np.ones(n, dtype=bool)
            train_mask[test_index] = False
            train_index = np.flatnonzero(train_mask)
            ls_train = x_ls[train_index]
            ls_test = x_ls[test_index]
            me_train = x_me[train_index]
            me_test = x_me[test_index]
            y_train = target[train_index]
            y_test = target[test_index]
            if mapping == "rank_ols":
                ls_train, ls_test = rank_train_test(ls_train, ls_test)
                me_train, me_test = rank_train_test(me_train, me_test)
                y_train, y_test = rank_train_test(y_train, y_test)
            ls_train_2d, ls_test_2d = standardize_train_test(
                ls_train[:, None], ls_test[:, None]
            )
            me_train_2d, me_test_2d = standardize_train_test(
                me_train[:, None], me_test[:, None]
            )
            full_train, full_test = standardize_train_test(
                np.column_stack([ls_train, me_train]),
                np.column_stack([ls_test, me_test]),
            )
            actual_parts.append(y_test)
            predicted_ls.append(ols_predict(ls_train_2d, y_train, ls_test_2d))
            predicted_me.append(ols_predict(me_train_2d, y_train, me_test_2d))
            predicted_full.append(ols_predict(full_train, y_train, full_test))
        actual = np.concatenate(actual_parts)
        ls_scores.append(r_squared(actual, np.concatenate(predicted_ls)))
        me_scores.append(r_squared(actual, np.concatenate(predicted_me)))
        full_scores.append(r_squared(actual, np.concatenate(predicted_full)))
    return np.asarray(ls_scores), np.asarray(me_scores), np.asarray(full_scores)


def prediction_multiverse(
    pair_rows: list[dict[str, object]], repeats: int, folds: int, seed: int
) -> list[dict[str, object]]:
    frame = pd.DataFrame(pair_rows)
    targets = {
        "2013": ("fc_sign", "fc_logistic"),
        "2017": ("fc", "yn"),
    }
    rows: list[dict[str, object]] = []
    for dataset, dataset_frame in frame.groupby("dataset", sort=True):
        for me_score in ME_SCORES:
            me = dataset_frame[f"me_{me_score}"].to_numpy(dtype=float)
            for ls_score in LS_SCORES:
                ls = dataset_frame[f"ls_{ls_score}"].to_numpy(dtype=float)
                for target_name in targets[dataset]:
                    target = dataset_frame[f"target_{target_name}"].to_numpy(dtype=float)
                    for mapping in MAPPINGS:
                        spec_seed = stable_seed(
                            seed, dataset, me_score, ls_score, target_name, mapping
                        )
                        r2_ls, r2_me, r2_full = cv_model_scores(
                            ls, me, target, mapping, repeats, folds, spec_seed
                        )
                        delta_me = r2_full - r2_ls
                        delta_ls = r2_full - r2_me
                        delta_difference = delta_me - delta_ls
                        support = bool(
                            float(delta_me.mean()) >= 0.02
                            and float(delta_difference.mean()) > 0
                        )
                        rows.append(
                            {
                                "dataset": dataset,
                                "me_score": me_score,
                                "ls_score": ls_score,
                                "validation_target": target_name,
                                "mapping": mapping,
                                "n_pairs": len(dataset_frame),
                                "cv_repeats": repeats,
                                "cv_folds": folds,
                                "r2_ls_only_mean": float(r2_ls.mean()),
                                "r2_me_only_mean": float(r2_me.mean()),
                                "r2_full_mean": float(r2_full.mean()),
                                "delta_r2_add_me_mean": float(delta_me.mean()),
                                "delta_r2_add_me_p10": float(np.quantile(delta_me, 0.10)),
                                "delta_r2_add_me_p90": float(np.quantile(delta_me, 0.90)),
                                "delta_r2_add_ls_mean": float(delta_ls.mean()),
                                "delta_r2_add_ls_p10": float(np.quantile(delta_ls, 0.10)),
                                "delta_r2_add_ls_p90": float(np.quantile(delta_ls, 0.90)),
                                "delta_me_minus_ls_mean": float(delta_difference.mean()),
                                "specification_support": support,
                            }
                        )
    return rows


def sign(value: float, tolerance: float = 1e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def decision_multiverse(pair_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    frame = pd.DataFrame(pair_rows)
    targets = {
        "2013": ("fc_sign", "fc_logistic"),
        "2017": ("fc", "yn"),
    }
    rows: list[dict[str, object]] = []
    for dataset, dataset_frame in frame.groupby("dataset", sort=True):
        for me_score in ME_SCORES:
            me_values = dataset_frame[f"me_{me_score}"].to_numpy(dtype=float)
            for ls_score in LS_SCORES:
                ls_values = dataset_frame[f"ls_{ls_score}"].to_numpy(dtype=float)
                for target_name in targets[dataset]:
                    target_values = dataset_frame[f"target_{target_name}"].to_numpy(
                        dtype=float
                    )
                    discordant = 0
                    me_agrees = 0
                    ls_agrees = 0
                    ties = 0
                    for me_value, ls_value, target_value in zip(
                        me_values, ls_values, target_values, strict=True
                    ):
                        me_sign = sign(me_value)
                        ls_sign = sign(ls_value)
                        target_sign = sign(target_value)
                        if me_sign == ls_sign:
                            continue
                        discordant += 1
                        if target_sign == 0:
                            ties += 1
                        elif target_sign == me_sign:
                            me_agrees += 1
                        elif target_sign == ls_sign:
                            ls_agrees += 1
                        else:
                            ties += 1
                    adjudicated = me_agrees + ls_agrees
                    me_rate: float | str = (
                        me_agrees / adjudicated if adjudicated else ""
                    )
                    support = bool(adjudicated >= 5 and float(me_rate) >= 0.70)
                    rows.append(
                        {
                            "dataset": dataset,
                            "me_score": me_score,
                            "ls_score": ls_score,
                            "validation_target": target_name,
                            "n_pairs": len(dataset_frame),
                            "n_sign_discordant": discordant,
                            "n_adjudicated": adjudicated,
                            "me_agrees": me_agrees,
                            "ls_agrees": ls_agrees,
                            "ties": ties,
                            "me_agreement_rate": me_rate,
                            "specification_support": support,
                        }
                    )
    return rows


def truth(value: object) -> bool:
    return str(value).lower() == "true"


def summarize(
    endpoint_rows: list[dict[str, object]],
    prediction_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, bool]], bool]:
    endpoint = pd.DataFrame(endpoint_rows)
    prediction = pd.DataFrame(prediction_rows)
    decision = pd.DataFrame(decision_rows)
    summary: list[dict[str, object]] = []
    clears: dict[str, dict[str, bool]] = {family: {} for family in (
        "endpoint", "prediction", "decision"
    )}
    for dataset in ("2013", "2017"):
        ep = endpoint.loc[
            (endpoint["dataset"] == dataset) & endpoint["admissible"].map(truth)
        ]
        ep_ordinary = float(ep["ordinary_support"].map(truth).mean())
        ep_notable = float(ep["notable_support"].map(truth).mean())
        ep_clear = ep_ordinary >= 0.80 and ep_notable >= 0.50
        clears["endpoint"][dataset] = ep_clear
        summary.append(
            {
                "dataset": dataset,
                "family": "endpoint",
                "n_specifications": len(ep),
                "support_proportion": ep_ordinary,
                "secondary_support_proportion": ep_notable,
                "median_primary_effect": float(ep["minimum_endpoint_ratio"].median()),
                "median_secondary_effect": "",
                "family_clear": ep_clear,
                "criterion": "ordinary>=.80 and notable>=.50",
            }
        )

        pred = prediction.loc[prediction["dataset"] == dataset]
        pred_support = float(pred["specification_support"].map(truth).mean())
        pred_delta = float(pred["delta_r2_add_me_mean"].median())
        pred_clear = pred_support >= 0.80 and pred_delta >= 0.02
        clears["prediction"][dataset] = pred_clear
        summary.append(
            {
                "dataset": dataset,
                "family": "prediction",
                "n_specifications": len(pred),
                "support_proportion": pred_support,
                "secondary_support_proportion": "",
                "median_primary_effect": pred_delta,
                "median_secondary_effect": float(
                    pred["delta_me_minus_ls_mean"].median()
                ),
                "family_clear": pred_clear,
                "criterion": "support>=.80 and median delta ME>=.02",
            }
        )

        dec = decision.loc[decision["dataset"] == dataset]
        dec_support = float(dec["specification_support"].map(truth).mean())
        dec_clear = dec_support >= 0.80
        clears["decision"][dataset] = dec_clear
        eligible = dec.loc[dec["n_adjudicated"] >= 5, "me_agreement_rate"]
        summary.append(
            {
                "dataset": dataset,
                "family": "decision",
                "n_specifications": len(dec),
                "support_proportion": dec_support,
                "secondary_support_proportion": "",
                "median_primary_effect": (
                    float(pd.to_numeric(eligible).median()) if len(eligible) else ""
                ),
                "median_secondary_effect": "",
                "family_clear": dec_clear,
                "criterion": "support>=.80",
            }
        )

    families_clearing_both = sum(
        clears[family]["2013"] and clears[family]["2017"] for family in clears
    )
    conclusion_changes = families_clearing_both >= 2
    summary.append(
        {
            "dataset": "both",
            "family": "overall",
            "n_specifications": len(endpoint) + len(prediction) + len(decision),
            "support_proportion": "",
            "secondary_support_proportion": "",
            "median_primary_effect": families_clearing_both,
            "median_secondary_effect": "",
            "family_clear": conclusion_changes,
            "criterion": "at least two families clear in both datasets",
        }
    )
    return summary, clears, conclusion_changes


def main() -> None:
    args = parse_args()
    paths = dataset_paths(args.raw_root)
    required = [
        args.analysis_dir / "analysis_readiness.csv",
        args.analysis_dir / "sprouse_item_signal_matrix.csv",
        args.analysis_dir / "sprouse_pair_contrasts.csv",
        args.derived_dir / "2013_condition_crosswalk.csv",
    ]
    for dataset in paths.values():
        required.extend([dataset.me, dataset.ls, dataset.fc])
        if dataset.yn is not None:
            required.append(dataset.yn)
    required.extend(args.source_archive)
    require_files(required)
    ensure_approved(args.analysis_dir)

    me_unit_maps: dict[str, dict[str, dict[str, float]]] = {}
    ls_unit_maps: dict[str, dict[str, dict[str, float]]] = {}
    me_pair_maps: dict[str, dict[str, dict[str, float]]] = {}
    ls_pair_maps: dict[str, dict[str, dict[str, float]]] = {}
    me_counts: dict[str, dict[str, int]] = {}
    ls_counts: dict[str, dict[str, int]] = {}
    me_nonpositive_rows: dict[str, int] = {}
    for dataset, dataset_path in paths.items():
        me_frame = add_scores(
            read_public_csv(dataset_path.me), dataset_path.subject, "me"
        )
        ls_frame = add_scores(
            read_public_csv(dataset_path.ls), dataset_path.subject, "ls"
        )
        me_nonpositive_rows[dataset] = int((me_frame["judgment"] <= 0).sum())
        unit_column = "condition" if dataset == "2013" else "item"
        me_unit_maps[dataset], me_counts[dataset] = aggregate_scores(
            me_frame, "me", unit_column
        )
        ls_unit_maps[dataset], ls_counts[dataset] = aggregate_scores(
            ls_frame, "ls", unit_column
        )
        me_pair_maps[dataset], _ = aggregate_scores(me_frame, "me", "condition")
        ls_pair_maps[dataset], _ = aggregate_scores(ls_frame, "ls", "condition")

    unit_rows = build_unit_rows(
        args.analysis_dir, me_unit_maps, ls_unit_maps, me_counts, ls_counts
    )
    pair_rows = build_pair_rows(
        args.analysis_dir, args.derived_dir, paths, me_pair_maps, ls_pair_maps
    )
    endpoint_rows = endpoint_multiverse(unit_rows, args.permutations, args.seed)
    prediction_rows = prediction_multiverse(
        pair_rows, args.cv_repeats, args.cv_folds, args.seed
    )
    decision_rows = decision_multiverse(pair_rows)
    summary_rows, clears, conclusion_changes = summarize(
        endpoint_rows, prediction_rows, decision_rows
    )

    outputs = {
        "sprouse_multiverse_unit_scores.csv": unit_rows,
        "sprouse_multiverse_pair_scores.csv": pair_rows,
        "sprouse_endpoint_multiverse.csv": endpoint_rows,
        "sprouse_prediction_multiverse.csv": prediction_rows,
        "sprouse_decision_multiverse.csv": decision_rows,
        "sprouse_multiverse_summary.csv": summary_rows,
    }
    for name, rows in outputs.items():
        output_rows_to_csv(args.out_dir / name, rows)

    manifest: list[dict[str, object]] = [
        {"key": "analysis", "value": "sprouse_resolution_multiverse"},
        {"key": "status", "value": "post_outcome_robustness"},
        {"key": "run_at", "value": datetime.now(timezone.utc).isoformat()},
        {"key": "seed", "value": args.seed},
        {"key": "permutations", "value": args.permutations},
        {"key": "cv_repeats", "value": args.cv_repeats},
        {"key": "cv_folds", "value": args.cv_folds},
        {"key": "unit_rows", "value": len(unit_rows)},
        {"key": "pair_rows", "value": len(pair_rows)},
        {"key": "endpoint_specifications", "value": len(endpoint_rows)},
        {"key": "prediction_specifications", "value": len(prediction_rows)},
        {"key": "decision_specifications", "value": len(decision_rows)},
        {"key": "conclusion_changes", "value": conclusion_changes},
        {
            "key": "participant_data_written",
            "value": False,
        },
    ]
    for dataset in ("2013", "2017"):
        manifest.append(
            {
                "key": f"me_nonpositive_rows_excluded_from_log_only:{dataset}",
                "value": me_nonpositive_rows[dataset],
            }
        )
    for path in args.source_archive:
        manifest.append({"key": f"sha256:{path.name}", "value": sha256(path)})
    for dataset, dataset_path in paths.items():
        for label, path in (
            ("me", dataset_path.me),
            ("ls", dataset_path.ls),
            ("fc", dataset_path.fc),
            ("yn", dataset_path.yn),
        ):
            if path is not None:
                manifest.append(
                    {"key": f"sha256:{dataset}:{label}:{path.name}", "value": sha256(path)}
                )
    for name in outputs:
        path = args.out_dir / name
        manifest.append({"key": f"sha256:output:{name}", "value": sha256(path)})
    manifest.append(
        {
            "key": "family_clears",
            "value": ";".join(
                f"{family}:{dataset}={clears[family][dataset]}"
                for family in ("endpoint", "prediction", "decision")
                for dataset in ("2013", "2017")
            ),
        }
    )
    output_rows_to_csv(args.out_dir / "sprouse_multiverse_manifest.csv", manifest)

    print(f"Wrote bounded multiverse outputs to {args.out_dir}")
    for row in summary_rows:
        print(
            f"{row['dataset']} {row['family']}: n={row['n_specifications']} "
            f"support={row['support_proportion']} effect={row['median_primary_effect']} "
            f"clear={row['family_clear']}"
        )
    print(f"Primary conclusion changes: {conclusion_changes}")


if __name__ == "__main__":
    main()
