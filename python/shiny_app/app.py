from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, reactive, render, req, ui
from shinywidgets import output_widget, render_widget

APP_ROOT = Path(__file__).resolve().parent
PYTHON_ROOT = APP_ROOT.parent
DATA_ROOT = PYTHON_ROOT / "data"
SSI_ROOT = DATA_ROOT / "ssi_denmark"
GEOJSON_PATH = DATA_ROOT / "geo" / "denmark_regions_simple.geojson"

METRICS: Dict[str, Dict[str, Any]] = {
    "hospitalizations": {
        "label": "Indlæggelser",
        "path": SSI_ROOT / "06_nye_indlaeggelser_pr_region_pr_dag.csv",
        "color": "Reds",
        "unit": "personer",
    },
    "cases": {
        "label": "Bekræftede tilfælde",
        "path": SSI_ROOT / "08_bekraeftede_tilfaelde_pr_dag_pr_regions.csv",
        "color": "Blues",
        "unit": "personer",
    },
    "deaths": {
        "label": "Dødsfald",
        "path": SSI_ROOT / "07_antal_doede_pr_dag_pr_region.csv",
        "color": "Purples",
        "unit": "personer",
    },
}


def _read_ssi_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", encoding="latin-1")


def _load_hospitalizations() -> pd.DataFrame:
    df = _read_ssi_csv(METRICS["hospitalizations"]["path"])
    columns = df.columns.tolist()
    rename_map = {
        columns[0]: "region_code",
        columns[1]: "region_name",
        columns[2]: "date",
        columns[3]: "value",
    }
    df = df.rename(columns=rename_map)
    df = df.dropna(subset=["region_code", "date"])
    df["metric"] = "hospitalizations"
    return df[["region_code", "region_name", "date", "metric", "value"]]


def _load_cases() -> pd.DataFrame:
    df = _read_ssi_csv(METRICS["cases"]["path"])
    columns = df.columns.tolist()
    rename_map = {
        columns[0]: "region_code",
        columns[1]: "region_name",
        columns[2]: "date",
        columns[3]: "cumulative",
    }
    df = df.rename(columns=rename_map)
    df = df.dropna(subset=["region_code", "date"])
    df["region_code"] = df["region_code"].astype(str)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values(["region_code", "date"])
    df["cumulative"] = pd.to_numeric(df["cumulative"], errors="coerce")
    df["cumulative"] = df["cumulative"].ffill().fillna(0)
    df["value"] = df.groupby("region_code", group_keys=False)["cumulative"].diff().fillna(df["cumulative"])
    df["value"] = df["value"].clip(lower=0)
    df["metric"] = "cases"
    return df[["region_code", "region_name", "date", "metric", "value"]]


def _load_deaths() -> pd.DataFrame:
    df = _read_ssi_csv(METRICS["deaths"]["path"])
    columns = df.columns.tolist()
    rename_map = {
        columns[0]: "region_code",
        columns[1]: "region_name",
        columns[2]: "date",
        columns[3]: "value",
    }
    df = df.rename(columns=rename_map)
    df = df.dropna(subset=["region_code", "date"])
    df["metric"] = "deaths"
    return df[["region_code", "region_name", "date", "metric", "value"]]


def _prepare_dataset() -> pd.DataFrame:
    frames: List[pd.DataFrame] = [
        _load_hospitalizations(),
        _load_cases(),
        _load_deaths(),
    ]
    df = pd.concat(frames, ignore_index=True)
    df["region_code"] = (
        df["region_code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )
    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    df = df.dropna(subset=["date"])
    df = df.sort_values(["metric", "region_code", "date"]).reset_index(drop=True)
    df["value_7d"] = (
        df.groupby(["metric", "region_code"])["value"]
        .transform(lambda s: s.rolling(window=7, min_periods=1).sum())
    )
    return df


def _load_geojson(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _format_value(val: float) -> str:
    return f"{int(round(float(val))):,}".replace(",", ".")


def _build_map_figure(
    df: pd.DataFrame,
    geojson: Dict[str, Any],
    metric_key: str,
    selected_date: pd.Timestamp,
) -> go.Figure:
    metric_meta = METRICS[metric_key]
    plot_df = df.copy()

    max_value = plot_df["value_7d"].max() or 0
    max_value = max_value * 1.05 if max_value > 0 else 1

    fig = px.choropleth(
        plot_df,
        geojson=geojson,
        locations="region_code",
        featureidkey="properties.region_code",
        color="value_7d",
        hover_name="region_name",
        custom_data=["value", "value_7d"],
        color_continuous_scale=metric_meta["color"],
        range_color=(0, max_value),
        labels={"value_7d": "7-dages sum"},
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Daglig: %{customdata[0]:,.0f}<br>"
            "7 dage: %{customdata[1]:,.0f}<extra></extra>"
        )
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=(
            f"{metric_meta['label']} - 7-dages sum "
            f"({selected_date.strftime('%d-%m-%Y')})"
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        coloraxis_colorbar=dict(
            title=f"7 dage ({metric_meta['unit']})",
            thickness=18,
            lenmode="fraction",
            len=0.6,
        ),
    )
    return fig


def _build_timeseries_figure(
    df: pd.DataFrame,
    metric_key: str,
    region_code: str,
    *,
    selected_date: pd.Timestamp | None = None,
) -> go.Figure:
    metric_meta = METRICS[metric_key]
    data = df.sort_values("date").copy()

    if region_code == "ALL":
        grouped = data.groupby("date", as_index=False)["value"].sum()
        grouped["rolling"] = grouped["value"].rolling(window=7, min_periods=1).sum()
        title = f"{metric_meta['label']} - Alle regioner"
    else:
        data = data[data["region_code"] == region_code]
        req(not data.empty)
        region_name = data["region_name"].iloc[0]
        grouped = data[["date", "value"]].copy()
        grouped["rolling"] = grouped["value"].rolling(window=7, min_periods=1).sum()
        title = f"{metric_meta['label']} - {region_name}"

    display_dates = grouped["date"].dt.strftime("%Y-%m-%d")
    hover_dates = grouped["date"].dt.strftime("%d-%m-%Y")

    fig = go.Figure()
    fig.add_bar(
        x=display_dates,
        y=grouped["value"],
        name="Daglig",
        marker_color="#1f77b4",
        customdata=hover_dates,
        hovertemplate="%{customdata}<br>Daglig: %{y:,.0f}<extra></extra>",
    )
    fig.add_scatter(
        x=display_dates,
        y=grouped["rolling"],
        name="7 dage",
        mode="lines",
        line=dict(color="#d62728", width=3),
        customdata=hover_dates,
        hovertemplate="%{customdata}<br>7 dage: %{y:,.0f}<extra></extra>",
    )
    if selected_date is not None:
        selected_str = pd.Timestamp(selected_date).strftime("%Y-%m-%d")
        hover_str = pd.Timestamp(selected_date).strftime("%d-%m-%Y")
        y_lower = min(0, grouped["value"].min(), grouped["rolling"].min())
        y_upper = max(grouped["value"].max(), grouped["rolling"].max())
        fig.add_trace(
            go.Scatter(
                x=[selected_str, selected_str],
                y=[y_lower, y_upper],
                mode="lines",
                line=dict(color="#444", dash="dash", width=2),
                name="Valgt dato",
                hoverinfo="text",
                text=[hover_str, hover_str],
                showlegend=False,
            )
        )

    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_title=f"Antal {metric_meta['unit']}",
        xaxis_title="Dato",
        hovermode="x unified",
    )
    return fig


def _compute_summary(
    df: pd.DataFrame,
    metric_key: str,
    region_code: str,
    selected_date: pd.Timestamp,
) -> Dict[str, str]:
    metric_meta = METRICS[metric_key]
    daily_slice = df[df["date"] == selected_date]
    if daily_slice.empty:
        return {
            "title": metric_meta["label"],
            "daily": "Ingen data",
            "rolling": "",
        }

    if region_code == "ALL":
        daily_value = daily_slice["value"].sum()
        mask = (df["date"] <= selected_date) & (
            df["date"] >= selected_date - pd.Timedelta(days=6)
        )
        rolling_value = df.loc[mask, "value"].sum()
        region_label = "Alle regioner"
    else:
        daily_slice = daily_slice[daily_slice["region_code"] == region_code]
        if daily_slice.empty:
            return {
                "title": metric_meta["label"],
                "daily": "Ingen data",
                "rolling": "",
            }
        daily_value = daily_slice["value"].iloc[0]
        rolling_value = daily_slice["value_7d"].iloc[0]
        region_label = daily_slice["region_name"].iloc[0]

    return {
        "title": f"{metric_meta['label']} - {region_label}",
        "daily": f"Daglig værdi: {_format_value(daily_value)} {metric_meta['unit']}",
        "rolling": f"7-dages sum: {_format_value(rolling_value)} {metric_meta['unit']}",
    }


DATASET = _prepare_dataset()
GEOJSON = _load_geojson(GEOJSON_PATH)
AVAILABLE_DATES = DATASET["date"].drop_duplicates().sort_values()
DATE_MIN = AVAILABLE_DATES.min().date()
DATE_MAX = AVAILABLE_DATES.max().date()

REGION_CHOICES = {"ALL": "Alle regioner"}
region_pairs = (
    DATASET[["region_code", "region_name"]]
    .drop_duplicates()
    .sort_values("region_name")
    .values
)
for code, name in region_pairs:
    REGION_CHOICES[str(code)] = name


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Kontroller"),
        ui.input_select(
            "metric",
            "Nøgletal",
            choices={key: meta["label"] for key, meta in METRICS.items()},
            selected="hospitalizations",
        ),
        ui.input_slider(
            "selected_date",
            "Dato",
            min=DATE_MIN,
            max=DATE_MAX,
            value=DATE_MAX,
            step=timedelta(days=1),
        ),
        ui.input_select(
            "region",
            "Region (detaljer)",
            choices=REGION_CHOICES,
            selected="ALL",
        ),
        ui.help_text(
            "Kortet viser 7-dages summen pr. region for den valgte dato. "
            "Tidsserien opdateres efter nøgletal og region."
        ),
        width=320,
    ),
    ui.div(
        ui.card(
            ui.card_header("Kort"),
            output_widget("region_map"),
        ),
        ui.card(
            ui.card_header("Udvikling"),
            output_widget("metric_timeseries"),
        ),
        class_="main-content",
    ),
    title="COVID-19 regionalt overblik",
    fillable=True,
)


def server(input, output, session):
    @reactive.Calc
    def filtered_dataset() -> pd.DataFrame:
        metric = input.metric()
        return DATASET[DATASET["metric"] == metric]

    @render_widget
    def region_map():
        metric = input.metric()
        selected_date = pd.Timestamp(input.selected_date())
        daily_data = filtered_dataset().query("date == @selected_date")
        req(not daily_data.empty)
        fig = _build_map_figure(
            daily_data,
            GEOJSON,
            metric,
            selected_date,
        )
        return fig

    @render_widget
    def metric_timeseries():
        metric = input.metric()
        region_code = input.region()
        selected_date = pd.Timestamp(input.selected_date())
        metric_df = filtered_dataset()
        req(not metric_df.empty)
        fig = _build_timeseries_figure(
            metric_df,
            metric,
            region_code,
            selected_date=selected_date,
        )
        return fig

app = App(app_ui, server)
