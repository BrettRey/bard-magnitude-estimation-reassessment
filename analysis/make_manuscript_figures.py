#!/usr/bin/env python3
"""Build the manuscript's aggregate-data figures.

The script reads only analysis products with condition-, item-, pair-, or
specification-level rows. It never reads or writes participant-level data.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANALYSIS_ROOT = ROOT / "data" / "derived"
DEFAULT_OUT_DIR = ROOT / "figures"
PDF_METADATA = {
    "Title": "Bard magnitude-estimation reassessment manuscript figure",
    "Author": "Brett Reynolds",
    "Creator": "analysis/make_manuscript_figures.py",
    "CreationDate": None,
    "ModDate": None,
}
CORAL_TEXT = "#C74F41"
GOLD_TEXT = "#94702B"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build aggregate-only figures for the ME reassessment."
    )
    parser.add_argument(
        "--analysis-root",
        type=Path,
        default=DEFAULT_ANALYSIS_ROOT,
        help="Root containing sprouse_analysis/ and sprouse_multiverse/.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Destination for vector PDFs and PNG previews.",
    )
    return parser.parse_args()


def load_house_style() -> object:
    """Load the central plot style through the project's house-style symlink."""

    preamble = (ROOT / ".house-style" / "preamble.tex").resolve(strict=True)
    style_path = preamble.parent / "plot_style.py"
    if not style_path.exists():
        raise FileNotFoundError(f"Central plot style not found: {style_path}")
    spec = importlib.util.spec_from_file_location("house_plot_style", style_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load central plot style: {style_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv_checked(
    path: Path,
    required_columns: Iterable[str],
    expected_rows: int,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required aggregate analysis product is missing: {path}")
    frame = pd.read_csv(path)
    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")
    if len(frame) != expected_rows:
        raise ValueError(
            f"{path} has {len(frame)} rows; expected {expected_rows}. "
            "Rerun the analysis pipeline before plotting."
        )
    datasets = set(frame["dataset"].astype(str))
    if datasets != {"2013", "2017"}:
        raise ValueError(f"{path} has unexpected dataset labels: {sorted(datasets)}")
    return frame


def save_figure(fig: plt.Figure, base: Path) -> None:
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".pdf"), metadata=PDF_METADATA)
    fig.savefig(base.with_suffix(".png"), dpi=300)
    plt.close(fig)


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.06,
        label,
        transform=ax.transAxes,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def build_response_figure(
    residuals: pd.DataFrame,
    out_dir: Path,
    colors: dict[str, str],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.15), sharey=True)
    panel_specs = [
        ("2013", "2013 comparison", "298 shared stimulus IDs"),
        ("2017", "2017 comparison", "786 shared stimulus IDs"),
    ]

    for index, (dataset, title, unit_note) in enumerate(panel_specs):
        ax = axes[index]
        data = residuals.loc[residuals["dataset"].astype(str) == dataset].copy()
        data = data.sort_values("me_z_mean")
        ax.scatter(
            data["me_z_mean"],
            data["ls_raw_mean"],
            s=10,
            color=colors["primary"],
            alpha=0.24,
            edgecolors="none",
            rasterized=True,
            label="Stimulus means",
        )
        ax.plot(
            data["me_z_mean"],
            data["linear_fitted"],
            color=colors["dark"],
            linestyle=(0, (4, 3)),
            linewidth=1.25,
            label="Linear fit",
        )
        ax.plot(
            data["me_z_mean"],
            data["bounded_logistic_fitted"],
            color=CORAL_TEXT,
            linewidth=1.6,
            label="Bounded logistic fit",
        )
        ax.set_title(f"{title}\n{unit_note}", pad=7)
        ax.set_xlabel("Mean standardized ME judgment")
        ax.set_ylim(0.8, 7.2)
        ax.set_yticks(range(1, 8))
        ax.tick_params(length=3)
        panel_label(ax, chr(ord("A") + index))

    axes[0].set_ylabel("Mean Likert judgment (1–7)")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.045),
        ncol=3,
        handlelength=2.8,
        columnspacing=1.4,
    )
    fig.subplots_adjust(left=0.09, right=0.99, top=0.82, bottom=0.24, wspace=0.18)
    save_figure(fig, out_dir / "response-functions")


def symmetric_stack_offsets(
    values: np.ndarray,
    bin_width: float,
    step: float,
) -> np.ndarray:
    """Stack nearby x values symmetrically around a categorical study row."""

    offsets = np.zeros(len(values), dtype=float)
    bin_ids = np.round(np.asarray(values, dtype=float) / bin_width).astype(int)
    for bin_id in np.unique(bin_ids):
        indices = np.flatnonzero(bin_ids == bin_id)
        ordered = indices[np.argsort(values[indices], kind="stable")]
        levels = np.arange(len(ordered), dtype=float) - (len(ordered) - 1) / 2
        offsets[ordered] = levels * step
    return offsets


def target_group(value: str) -> str:
    return "Yes/no" if "yn" in value.lower() else "Forced choice"


def build_multiverse_figure(
    endpoint: pd.DataFrame,
    prediction: pd.DataFrame,
    decision: pd.DataFrame,
    pair_scores: pd.DataFrame,
    out_dir: Path,
    colors: dict[str, str],
) -> None:
    fig = plt.figure(figsize=(7.2, 5.25))
    grid = fig.add_gridspec(2, 2, height_ratios=(1.0, 0.62), hspace=0.86, wspace=0.34)
    ax_endpoint = fig.add_subplot(grid[0, 0])
    ax_prediction = fig.add_subplot(grid[0, 1])
    ax_decision = fig.add_subplot(grid[1, :])

    endpoint = endpoint.loc[endpoint["admissible"].astype(str).str.lower() == "true"].copy()
    for index, dataset in enumerate(("2013", "2017")):
        data = endpoint.loc[endpoint["dataset"].astype(str) == dataset].reset_index(drop=True)
        y = np.full(len(data), index) + symmetric_stack_offsets(
            data["minimum_endpoint_ratio"].to_numpy(),
            bin_width=0.025,
            step=0.05,
        )
        notable = data["notable_support"].astype(str).str.lower() == "true"
        ax_endpoint.scatter(
            data.loc[~notable, "minimum_endpoint_ratio"],
            y[~notable],
            s=24,
            facecolors="none",
            edgecolors=colors["dark"],
            alpha=0.42,
            linewidths=0.75,
        )
        ax_endpoint.scatter(
            data.loc[notable, "minimum_endpoint_ratio"],
            y[notable],
            s=105,
            marker="*",
            color=colors["quinary"],
            edgecolors=colors["dark"],
            linewidths=0.85,
            zorder=3,
        )
        if notable.any():
            point_index = int(np.flatnonzero(notable.to_numpy())[0])
            ax_endpoint.annotate(
                "Endpoint criterion met",
                (float(data.loc[notable, "minimum_endpoint_ratio"].iloc[0]), float(y[point_index])),
                xytext=(-8, 18),
                textcoords="offset points",
                ha="right",
                va="bottom",
                arrowprops={"arrowstyle": "-", "color": colors["dark"], "linewidth": 0.6},
            )
    ax_endpoint.axvline(1.0, color=colors["dark"], linestyle=(0, (3, 3)), linewidth=1.0)
    ax_endpoint.set_yticks([0, 1], ["2013", "2017"])
    ax_endpoint.set_ylim(-0.45, 1.45)
    ax_endpoint.set_xlabel("Minimum endpoint / middle spread ratio")
    ax_endpoint.set_title("Endpoint specifications")
    ax_endpoint.grid(axis="x", color=colors["light"], linewidth=0.5)
    panel_label(ax_endpoint, "A")

    target_colors = {
        "Forced choice": colors["primary"],
        "Yes/no": GOLD_TEXT,
    }
    mapping_markers = {"raw_ols": "o", "rank_ols": "^"}
    for dataset_index, dataset in enumerate(("2013", "2017")):
        data = prediction.loc[prediction["dataset"].astype(str) == dataset].reset_index(drop=True)
        vertical_offsets = symmetric_stack_offsets(
            data["delta_r2_add_me_mean"].to_numpy(),
            bin_width=0.0035,
            step=0.03,
        )
        for target in ("Forced choice", "Yes/no"):
            for mapping, marker in mapping_markers.items():
                mask = (
                    data["validation_target"].map(target_group).eq(target)
                    & data["mapping"].eq(mapping)
                )
                if not mask.any():
                    continue
                supported = data.loc[mask, "specification_support"].astype(str).str.lower().eq("true")
                row_positions = np.flatnonzero(mask.to_numpy())
                values = data.loc[mask, "delta_r2_add_me_mean"].to_numpy()
                positions = np.full(mask.sum(), dataset_index) + vertical_offsets[row_positions]
                for meets_rule in (False, True):
                    subset = supported.to_numpy() == meets_rule
                    if not subset.any():
                        continue
                    marker_for_status = "s" if meets_rule else marker
                    facecolor = (
                        colors["quinary"]
                        if meets_rule
                        else target_colors[target] if target == "Forced choice" else "none"
                    )
                    edgecolor = colors["quinary"] if meets_rule else target_colors[target]
                    ax_prediction.scatter(
                        values[subset],
                        positions[subset],
                        s=48 if meets_rule else 27,
                        marker=marker_for_status,
                        facecolors=facecolor,
                        edgecolors=edgecolor,
                        alpha=1.0 if meets_rule else 0.68,
                        linewidths=0.9,
                        zorder=3 if meets_rule else 2,
                    )
    ax_prediction.axvline(0.02, color=colors["dark"], linestyle=(0, (3, 3)), linewidth=1.0)
    ax_prediction.axvline(0.0, color=colors["light"], linewidth=0.8)
    ax_prediction.set_yticks([0, 1], ["2013", "2017"])
    ax_prediction.set_ylim(-0.45, 1.45)
    ax_prediction.set_xlabel(r"Cross-validated $\Delta R^2$ from adding ME")
    ax_prediction.set_title("Incremental-prediction specifications")
    ax_prediction.grid(axis="x", color=colors["light"], linewidth=0.5)
    endpoint_legend_handles = [
        plt.Line2D(
            [], [], linestyle="none", marker="o", markerfacecolor="none",
            markeredgecolor=colors["dark"], alpha=0.55, label="Other specifications",
        ),
        plt.Line2D(
            [], [], linestyle="none", marker="*", markersize=9,
            markerfacecolor=colors["quinary"], markeredgecolor=colors["dark"],
            label="Endpoint criterion met",
        ),
    ]
    prediction_legend_handles = [
        plt.Line2D(
            [], [], linestyle="none", marker="o", markerfacecolor=target_colors["Forced choice"],
            markeredgecolor=target_colors["Forced choice"], label="Forced choice + raw",
        ),
        plt.Line2D(
            [], [], linestyle="none", marker="o", markerfacecolor="none",
            markeredgecolor=target_colors["Yes/no"], label="Yes/no + raw",
        ),
        plt.Line2D(
            [], [], linestyle="none", marker="s", markersize=7,
            markerfacecolor=colors["quinary"], markeredgecolor=colors["quinary"],
            label="Prediction criterion met",
        ),
        plt.Line2D(
            [], [], linestyle="none", marker="^", markerfacecolor=target_colors["Forced choice"],
            markeredgecolor=target_colors["Forced choice"], label="Forced choice + rank",
        ),
        plt.Line2D(
            [], [], linestyle="none", marker="^", markerfacecolor="none",
            markeredgecolor=target_colors["Yes/no"], label="Yes/no + rank",
        ),
    ]
    fig.legend(
        handles=endpoint_legend_handles,
        title="Panel A",
        ncol=1,
        loc="upper center",
        bbox_to_anchor=(0.27, 0.50),
        handletextpad=0.4,
        labelspacing=0.65,
        alignment="left",
    )
    fig.legend(
        handles=prediction_legend_handles,
        title="Panel B",
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.74, 0.50),
        handletextpad=0.4,
        columnspacing=0.9,
        labelspacing=0.65,
        alignment="left",
    )
    panel_label(ax_prediction, "B")

    me_score_columns = (
        "me_provided_z",
        "me_log_subject_z",
        "me_subject_percentile",
    )
    ls_score_columns = (
        "ls_provided_z",
        "ls_raw_mean",
        "ls_subject_percentile",
    )
    decision_rows = []
    for dataset in ("2013", "2017"):
        data = decision.loc[decision["dataset"].astype(str) == dataset]
        pairs = int(data["n_pairs"].iloc[0])
        discordant = int(data["n_sign_discordant"].iloc[0])
        if not (data["n_pairs"].eq(pairs) & data["n_sign_discordant"].eq(discordant)).all():
            raise ValueError(f"Decision denominators vary unexpectedly within {dataset}.")
        pair_data = pair_scores.loc[
            pair_scores["dataset"].astype(str) == dataset
        ].reset_index(drop=True)
        discordant_id_sets: set[tuple[str, ...]] = set()
        for me_column in me_score_columns:
            me_values = pair_data[me_column].to_numpy(dtype=float)
            me_signs = np.where(me_values > 1e-12, 1, np.where(me_values < -1e-12, -1, 0))
            for ls_column in ls_score_columns:
                ls_values = pair_data[ls_column].to_numpy(dtype=float)
                ls_signs = np.where(ls_values > 1e-12, 1, np.where(ls_values < -1e-12, -1, 0))
                discordant_ids = tuple(
                    pair_data.loc[me_signs != ls_signs, "pair_id"].astype(str)
                )
                discordant_id_sets.add(discordant_ids)
        if len(discordant_id_sets) != 1:
            raise ValueError(f"Discordant pair identities vary across scores within {dataset}.")
        discordant_ids = next(iter(discordant_id_sets))
        if len(pair_data) != pairs or len(discordant_ids) != discordant:
            raise ValueError(f"Pair-level disagreement audit does not match decision rows for {dataset}.")
        decision_rows.append(
            (dataset, discordant, pairs, discordant / pairs, discordant_ids)
        )

    x = np.arange(2)
    heights = [row[3] for row in decision_rows]
    bars = ax_decision.bar(
        x,
        heights,
        width=0.42,
        color=colors["primary"],
        alpha=0.74,
    )
    for bar, (_, discordant, pairs, rate, discordant_ids) in zip(bars, decision_rows):
        noun = "pair" if discordant == 1 else "pairs"
        id_noun = "ID" if discordant == 1 else "IDs"
        ax_decision.text(
            bar.get_x() + bar.get_width() / 2,
            rate + 0.0014,
            f"{discordant} discordant {noun} of {pairs}\n"
            f"{id_noun} {', '.join(discordant_ids)}",
            ha="center",
            va="bottom",
        )
    ax_decision.set_xticks(x, ["2013", "2017"])
    ax_decision.set_ylabel("Pairs with different ME/Likert signs")
    ax_decision.set_ylim(0, 0.034)
    ax_decision.set_yticks([0, 0.01, 0.02, 0.03], ["0%", "1%", "2%", "3%"])
    ax_decision.set_title("Pair-level sign disagreements")
    ax_decision.grid(axis="y", color=colors["light"], linewidth=0.5)
    panel_label(ax_decision, "C")

    fig.subplots_adjust(left=0.11, right=0.99, top=0.91, bottom=0.10)
    save_figure(fig, out_dir / "multiverse-landscape")


def main() -> None:
    args = parse_args()
    style = load_house_style()
    style.setup_minimal()
    plt.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.unicode_minus": True,
            "mathtext.fontset": "custom",
            "mathtext.rm": "EB Garamond",
            "mathtext.it": "EB Garamond:italic",
            "mathtext.bf": "EB Garamond:bold",
            "mathtext.fallback": "stix",
        }
    )

    analysis_dir = args.analysis_root / "sprouse_analysis"
    multiverse_dir = args.analysis_root / "sprouse_multiverse"
    residuals = read_csv_checked(
        analysis_dir / "sprouse_response_function_residuals.csv",
        {
            "dataset",
            "me_z_mean",
            "ls_raw_mean",
            "linear_fitted",
            "bounded_logistic_fitted",
        },
        1084,
    )
    endpoint = read_csv_checked(
        multiverse_dir / "sprouse_endpoint_multiverse.csv",
        {
            "dataset",
            "minimum_endpoint_ratio",
            "admissible",
            "notable_support",
        },
        54,
    )
    prediction = read_csv_checked(
        multiverse_dir / "sprouse_prediction_multiverse.csv",
        {
            "dataset",
            "validation_target",
            "mapping",
            "delta_r2_add_me_mean",
            "specification_support",
        },
        72,
    )
    decision = read_csv_checked(
        multiverse_dir / "sprouse_decision_multiverse.csv",
        {
            "dataset",
            "n_pairs",
            "n_sign_discordant",
            "specification_support",
        },
        36,
    )
    pair_scores = read_csv_checked(
        multiverse_dir / "sprouse_multiverse_pair_scores.csv",
        {
            "dataset",
            "pair_id",
            "me_provided_z",
            "me_log_subject_z",
            "me_subject_percentile",
            "ls_provided_z",
            "ls_raw_mean",
            "ls_subject_percentile",
        },
        200,
    )

    build_response_figure(residuals, args.out_dir, style.COLORS)
    build_multiverse_figure(
        endpoint, prediction, decision, pair_scores, args.out_dir, style.COLORS
    )
    print(f"Wrote manuscript figures to {args.out_dir}")


if __name__ == "__main__":
    main()
