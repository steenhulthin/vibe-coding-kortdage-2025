"""Helpers for working with Danish SSI COVID-19 datasets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd


SSI_DAILY_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "ssi_denmark"
    / "03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv"
)

AggregationFreq = Literal["D", "W", "M"]


@dataclass(frozen=True)
class SSIDataset:
    """Basic data holder describing the SSI source file and aggregation."""

    source_path: Path = SSI_DAILY_PATH
    frequency: AggregationFreq = "M"


def _load_raw_daily(path: Path) -> pd.DataFrame:
    """Load the raw SSI CSV with consistent column names."""
    df = pd.read_csv(
        path,
        sep=";",
        encoding="latin-1",
        parse_dates=["Prøvetagningsdato"],
        dayfirst=False,
    )

    df = df.rename(
        columns={
            "Regionskode": "region_code",
            "Region": "region_name",
            "Prøvetagningsdato": "date",
            "Køn": "sex",
            "Indlæggelser": "hospitalizations",
        }
    )
    df["region_code"] = df["region_code"].astype(str).str.strip()
    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["sex"] = df["sex"].astype(str).str.strip()
    df["hospitalizations"] = pd.to_numeric(df["hospitalizations"], errors="coerce").fillna(0)

    return df


def load_aggregated_hospitalizations(dataset: SSIDataset) -> pd.DataFrame:
    """Return region-level hospitalizations aggregated to the configured frequency."""
    df = _load_raw_daily(dataset.source_path)
    df = (
        df.groupby(["region_code", "region_name", "date"], as_index=False)["hospitalizations"]
        .sum()
        .sort_values(["region_code", "date"])
    )

    if dataset.frequency == "D":
        df["period_start"] = df["date"]
        df["period_label"] = df["period_start"].dt.strftime("%Y-%m-%d")
        return df

    freq = {"W": "W-MON", "M": "M"}[dataset.frequency]
    df["period"] = df["date"].dt.to_period(freq)
    agg_df = (
        df.groupby(["region_code", "region_name", "period"], as_index=False)["hospitalizations"]
        .sum()
        .sort_values(["region_code", "period"])
    )

    agg_df["period_start"] = agg_df["period"].dt.to_timestamp()
    if dataset.frequency == "W":
        agg_df["period_label"] = agg_df["period_start"].dt.strftime("Uge %V %Y")
    else:
        agg_df["period_label"] = agg_df["period_start"].dt.strftime("%Y-%m")

    return agg_df[
        ["region_code", "region_name", "period_start", "period_label", "hospitalizations"]
    ]


def load_monthly_hospitalizations(path: Path | None = None) -> pd.DataFrame:
    """Convenience wrapper returning monthly totals per region."""
    dataset = SSIDataset(source_path=path or SSI_DAILY_PATH, frequency="M")
    return load_aggregated_hospitalizations(dataset)
