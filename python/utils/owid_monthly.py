"""Utilities for building a month-level OWID COVID-19 dataset for the Streamlit app."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


METRIC_COLUMNS: tuple[str, ...] = (
    "hosp_patients_per_million",
    "weekly_hosp_admissions_per_million",
    "icu_patients_per_million",
    "new_deaths_per_million",
    "total_deaths_per_million",
)


@dataclass(frozen=True)
class MonthlyDatasetConfig:
    source_path: Path
    output_path: Path
    metric_columns: Iterable[str] = METRIC_COLUMNS


def _coerce_metric_columns(df: pd.DataFrame, metrics: Iterable[str]) -> pd.DataFrame:
    """Ensure metric columns are numeric so monthly aggregations work as expected."""
    for col in metrics:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_owid_daily(path: Path, metrics: Iterable[str]) -> pd.DataFrame:
    """Load the daily OWID CSV with parsed dates and numeric metrics."""
    df = pd.read_csv(path, parse_dates=["date"])
    df = _coerce_metric_columns(df, metrics)
    return df


def aggregate_to_monthly(df: pd.DataFrame, metrics: Iterable[str]) -> pd.DataFrame:
    """Aggregate daily rows to month level per country."""
    if "date" not in df.columns:
        raise ValueError("DataFrame needs a 'date' column for monthly aggregation.")

    df = df.copy()
    df["year_month"] = df["date"].dt.to_period("M")

    group_keys = ["iso_code", "location", "continent", "year_month"]
    agg_map: Mapping[str, str] = {col: "sum" for col in metrics if col in df.columns}

    monthly_df = (
        df.groupby(group_keys, dropna=False)
        .agg(agg_map)
        .reset_index()
        .sort_values(group_keys)
    )
    monthly_df["month_start"] = monthly_df["year_month"].dt.to_timestamp()
    monthly_df["year_month"] = monthly_df["year_month"].astype(str)
    return monthly_df


def build_monthly_dataset(config: MonthlyDatasetConfig) -> pd.DataFrame:
    """Read the OWID daily file, aggregate to months, and write the result."""
    df = load_owid_daily(config.source_path, config.metric_columns)
    monthly_df = aggregate_to_monthly(df, config.metric_columns)
    monthly_df.to_csv(config.output_path, index=False)
    return monthly_df


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    source = project_root / "data" / "owid_covid_global.csv"
    target = project_root / "data" / "owid_covid_global_monthly.csv"
    config = MonthlyDatasetConfig(source_path=source, output_path=target)
    build_monthly_dataset(config)


if __name__ == "__main__":
    main()
