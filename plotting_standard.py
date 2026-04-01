"""Shared plotting and reporting utilities for publication-focused project code."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DISPLAY_DPI = 150
EXPORT_DPI = 600
DEFAULT_RASTER_FORMAT = "png"
DEFAULT_VECTOR_FORMAT = "pdf"

DEFAULT_PROFILE = "paper"

FIGURE_SIZES = {
    "single": (6.4, 4.8),
    "single_wide": (6.8, 4.2),
    "single_column": (3.35, 4.2),
    "comparison": (7.2, 3.4),
    "triptych": (11.4, 3.8),
    "tall": (7.2, 5.4),
    "square": (5.0, 5.0),
}

BASE_RCPARAMS = {
    "figure.dpi": DISPLAY_DPI,
    "savefig.dpi": EXPORT_DPI,
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Microsoft YaHei", "SimHei"],
    "mathtext.fontset": "dejavusans",
    "font.size": 9.0,
    "axes.titlesize": 10.0,
    "axes.titleweight": "normal",
    "axes.labelsize": 9.0,
    "axes.linewidth": 0.7,
    "axes.grid": False,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "legend.fontsize": 8.0,
    "legend.frameon": False,
    "grid.linestyle": "--",
    "grid.linewidth": 0.6,
    "grid.alpha": 0.35,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "axes.unicode_minus": False,
}

STYLE_PROFILES = {
    "paper": {},
    "compact": {
        "font.size": 8.0,
        "axes.labelsize": 8.0,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
    },
    "si": {
        "font.size": 9.0,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "legend.fontsize": 8.0,
    },
    "composite": {
        "font.size": 10.0,
        "axes.labelsize": 11.0,
        "xtick.labelsize": 10.0,
        "ytick.labelsize": 10.0,
        "legend.fontsize": 8.0,
    },
    "presentation": {
        "font.size": 11.0,
        "axes.labelsize": 14.0,
        "xtick.labelsize": 11.0,
        "ytick.labelsize": 11.0,
        "legend.fontsize": 10.0,
    },
    "single_column": {
        "font.family": "Arial",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 8.0,
        "axes.labelsize": 8.0,
        "axes.linewidth": 0.5,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "legend.fontsize": 7.0,
    },
}


def get_plot_rcparams(
    profile: str = DEFAULT_PROFILE,
    *,
    rc_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    """Return the merged rcParams dictionary for a named plotting profile."""
    if profile not in STYLE_PROFILES:
        raise KeyError(f"Unknown plotting profile '{profile}'. Available: {sorted(STYLE_PROFILES)}")

    rcparams = dict(BASE_RCPARAMS)
    rcparams.update(STYLE_PROFILES[profile])
    if rc_overrides:
        rcparams.update(rc_overrides)
    return rcparams


PROJECT_RCPARAMS = get_plot_rcparams()


def apply_plot_style(
    profile: str = DEFAULT_PROFILE,
    *,
    rc_overrides: dict[str, object] | None = None,
) -> None:
    """Apply a standardized plotting profile to matplotlib."""
    plt.rcParams.update(get_plot_rcparams(profile, rc_overrides=rc_overrides))


def get_figure_size(preset: str) -> tuple[float, float]:
    """Return a named figure size preset."""
    if preset not in FIGURE_SIZES:
        raise KeyError(f"Unknown figure preset '{preset}'. Available: {sorted(FIGURE_SIZES)}")
    return FIGURE_SIZES[preset]


def create_figure(
    preset: str = "single",
    *,
    profile: str = DEFAULT_PROFILE,
    nrows: int = 1,
    ncols: int = 1,
    dpi: int | None = None,
    constrained_layout: bool = False,
    **kwargs,
):
    """Create a standardized matplotlib figure using named size presets."""
    apply_plot_style(profile)
    return plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=get_figure_size(preset),
        dpi=dpi or DISPLAY_DPI,
        constrained_layout=constrained_layout,
        **kwargs,
    )


def create_single_axis_figure(
    preset: str = "single",
    *,
    profile: str = DEFAULT_PROFILE,
    dpi: int | None = None,
):
    """Create a standardized one-panel figure."""
    apply_plot_style(profile)
    fig = plt.figure(figsize=get_figure_size(preset), dpi=dpi or DISPLAY_DPI)
    ax = fig.add_subplot(1, 1, 1)
    return fig, ax


def style_axes(
    ax,
    *,
    grid: bool = False,
    grid_axis: str = "both",
    equal_aspect: bool = False,
) -> None:
    """Apply a consistent paper-ready axis style."""
    ax.grid(grid, axis=grid_axis, linestyle="--", linewidth=0.6, alpha=0.35 if grid else 0.0)
    ax.tick_params(
        direction="out",
        length=float(plt.rcParams.get("xtick.major.size", 3.0)),
        width=float(plt.rcParams.get("xtick.major.width", 0.7)),
    )
    for spine in ax.spines.values():
        spine.set_linewidth(float(plt.rcParams.get("axes.linewidth", 0.7)))
    if equal_aspect:
        ax.set_aspect("equal", adjustable="box")


def style_standard_axes(
    ax,
    *,
    grid: bool = False,
    grid_axis: str = "both",
    equal_aspect: bool = False,
) -> None:
    """Backward-compatible wrapper around the standardized axis style."""
    style_axes(ax, grid=grid, grid_axis=grid_axis, equal_aspect=equal_aspect)


def finalize_figure(
    fig,
    *,
    pad: float = 0.45,
    h_pad: float | None = None,
    w_pad: float | None = None,
    rect: tuple[float, float, float, float] | None = None,
) -> None:
    """Apply a consistent tight-layout pass to a figure."""
    tight_layout_kwargs: dict[str, object] = {"pad": pad}
    if h_pad is not None:
        tight_layout_kwargs["h_pad"] = h_pad
    if w_pad is not None:
        tight_layout_kwargs["w_pad"] = w_pad
    if rect is not None:
        tight_layout_kwargs["rect"] = rect
    fig.tight_layout(**tight_layout_kwargs)


def compute_plot_limits(*arrays: Sequence[float], pad_ratio: float = 0.03) -> tuple[float, float]:
    """Compute shared axis limits with a small padding."""
    flat_values = []
    for array in arrays:
        values = np.asarray(array, dtype=float).ravel()
        if values.size:
            flat_values.append(values)

    if not flat_values:
        raise ValueError("At least one non-empty array is required to compute plot limits.")

    merged = np.concatenate(flat_values)
    lo = float(np.min(merged))
    hi = float(np.max(merged))
    pad = pad_ratio * (hi - lo) if hi > lo else 1.0
    return lo - pad, hi + pad


def add_identity_line(
    ax,
    vmin: float,
    vmax: float,
    *,
    color: str = "black",
    linewidth: float = 1.2,
    linestyle: str = "--",
) -> None:
    """Draw a standardized y=x reference line."""
    ax.plot([vmin, vmax], [vmin, vmax], linestyle=linestyle, linewidth=linewidth, color=color)


def annotate_panel_text(
    ax,
    text: str,
    *,
    x: float = 0.03,
    y: float = 0.97,
    fontsize: int = 10,
    ha: str = "left",
    va: str = "top",
) -> None:
    """Place consistent annotation text in axes coordinates."""
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=fontsize)


def add_panel_label(
    ax,
    label: str,
    *,
    x: float = -0.12,
    y: float = 1.02,
    fontsize: float = 10.0,
    fontweight: str = "bold",
) -> None:
    """Add a standardized panel label such as 'a' or 'b'."""
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=fontsize,
        fontweight=fontweight,
    )


def annotate_bar_values(
    ax,
    *,
    bars=None,
    values: Sequence[float] | None = None,
    orientation: str = "h",
    fmt: str = "{:.3f}",
    anchor: str = "outside",
    pad_ratio: float = 0.015,
    fontsize: float = 8.0,
    color: str = "black",
) -> None:
    """Add standardized labels to bar charts."""
    if bars is None:
        bars = list(ax.patches)
    if values is None:
        if orientation == "h":
            values = [bar.get_width() for bar in bars]
        else:
            values = [bar.get_height() for bar in bars]

    if orientation == "h":
        x_min, x_max = ax.get_xlim()
        span = max(x_max - x_min, 1e-9)
        pad = pad_ratio * span
        axis_anchor = x_max - pad
        for bar, value in zip(bars, values):
            y_pos = bar.get_y() + bar.get_height() / 2
            if anchor == "axis_right":
                x_pos = axis_anchor
                ha = "right"
            elif anchor == "inside_right":
                x_pos = value - pad
                ha = "right"
            else:
                x_pos = value + pad
                ha = "left"
            ax.text(x_pos, y_pos, fmt.format(value), va="center", ha=ha, fontsize=fontsize, color=color)
        return

    y_min, y_max = ax.get_ylim()
    span = max(y_max - y_min, 1e-9)
    pad = pad_ratio * span
    axis_anchor = y_max - pad
    for bar, value in zip(bars, values):
        x_pos = bar.get_x() + bar.get_width() / 2
        if anchor == "axis_top":
            y_pos = axis_anchor
            va = "top"
        elif anchor == "inside_top":
            y_pos = value - pad
            va = "top"
        else:
            y_pos = value + pad
            va = "bottom"
        ax.text(x_pos, y_pos, fmt.format(value), va=va, ha="center", fontsize=fontsize, color=color)


def metric_text(
    mae: float,
    rmse: float,
    r2: float,
    *,
    decimals: int = 3,
    include_units: bool = True,
) -> str:
    """Create a standardized regression-metrics annotation string."""
    unit = " ppm" if include_units else ""
    return (
        f"MAE={mae:.{decimals}f}{unit}\n"
        f"RMSE={rmse:.{decimals}f}{unit}\n"
        f"R$^2$={r2:.{decimals}f}"
    )


def metric_row(
    label: str,
    mae: float,
    rmse: float,
    r2: float,
    *,
    label_width: int = 20,
    decimals: int = 3,
) -> str:
    """Create a one-line regression-metrics summary."""
    return (
        f"{label:<{label_width}} | "
        f"MAE={mae:.{decimals}f} ppm | "
        f"RMSE={rmse:.{decimals}f} ppm | "
        f"R2={r2:.{decimals}f}"
    )


def print_section(title: str) -> None:
    """Print a notebook section heading in a consistent scientific style."""
    line = "=" * len(title)
    print(f"\n{line}\n{title}\n{line}")


def print_key_value_rows(rows: Sequence[tuple[str, object]]) -> None:
    """Print aligned key-value rows."""
    if not rows:
        return
    width = max(len(str(key)) for key, _ in rows)
    for key, value in rows:
        print(f"{key:<{width}} : {value}")


def report_saved_paths(paths: Iterable[str | Path], heading: str = "Saved files") -> list[Path]:
    """Print a standardized list of generated output files."""
    resolved_paths = [Path(path).resolve() for path in paths]
    print_section(heading)
    for path in resolved_paths:
        print(f"- {path}")
    return resolved_paths


def prepare_display_table(df: pd.DataFrame, digits: int = 3) -> pd.DataFrame:
    """Return a copy of a DataFrame with numeric columns rounded for display."""
    display_df = df.copy()
    numeric_cols = display_df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        display_df.loc[:, numeric_cols] = display_df.loc[:, numeric_cols].round(digits)
    return display_df


def _normalize_formats(formats: Iterable[str]) -> list[str]:
    normalized = []
    for fmt in formats:
        clean = fmt.lower().lstrip(".")
        if clean and clean not in normalized:
            normalized.append(clean)
    return normalized


def save_figure(
    fig,
    out_path: str | Path,
    *,
    extra_formats: Iterable[str] | None = None,
    dpi: int = EXPORT_DPI,
    bbox_inches: str = "tight",
    close: bool = False,
) -> list[Path]:
    """Save a figure with consistent export settings."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix:
        primary = path
    else:
        primary = path.with_suffix(f".{DEFAULT_RASTER_FORMAT}")

    formats = [primary.suffix.lstrip(".")]
    if extra_formats is None and primary.suffix.lower() == f".{DEFAULT_RASTER_FORMAT}":
        formats.append(DEFAULT_VECTOR_FORMAT)
    elif extra_formats is not None:
        formats.extend(extra_formats)

    saved_paths: list[Path] = []
    for fmt in _normalize_formats(formats):
        target = primary.with_suffix(f".{fmt}")
        fig.savefig(target, dpi=dpi, bbox_inches=bbox_inches, facecolor="white")
        saved_paths.append(target)

    if close:
        plt.close(fig)

    return saved_paths
