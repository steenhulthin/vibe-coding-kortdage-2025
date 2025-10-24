from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from plotly.graph_objects import Figure

from utils.ssi_denmark import load_monthly_hospitalizations

APP_ROOT = Path(__file__).resolve().parent
DATA_ROOT = APP_ROOT.parents[1] / "data"
SSI_PATH = DATA_ROOT / "ssi_denmark" / "03_bekraeftede_tilfaelde_doede_indlagte_pr_dag_pr_koen.csv"
GEOJSON_PATH = DATA_ROOT / "geo" / "denmark_regions_simple.geojson"


def load_geojson(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def prepare_dataset() -> pd.DataFrame:
    df = load_monthly_hospitalizations(SSI_PATH)
    df = df.sort_values("period_start")

    region_lookup = df[["region_code", "region_name"]].drop_duplicates().set_index("region_code")["region_name"]
    all_periods = pd.period_range(df["period_start"].min(), df["period_start"].max(), freq="M")
    full_index = pd.MultiIndex.from_product(
        [region_lookup.index, all_periods], names=["region_code", "period"]
    )

    df = (
        df.assign(period=lambda d: d["period_start"].dt.to_period("M"))
        .set_index(["region_code", "period"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )
    df["region_name"] = df["region_code"].map(region_lookup)
    df["period_start"] = df["period"].dt.to_timestamp()
    df["period_label"] = df["period_start"].dt.strftime("%Y-%m")
    df = df.rename(columns={"hospitalizations": "hospitalizations"})

    df["period_label"] = pd.Categorical(
        df["period_label"],
        categories=sorted(df["period_label"].unique()),
        ordered=True,
    )
    return df[
        ["region_code", "region_name", "period_start", "period_label", "hospitalizations"]
    ]


def build_map_figure(df: pd.DataFrame, regions_geojson: dict) -> Figure:
    max_value = df["hospitalizations"].max() or 0
    category_orders = {"period_label": list(df["period_label"].cat.categories)}

    fig = px.choropleth(
        df,
        geojson=regions_geojson,
        locations="region_code",
        color="hospitalizations",
        featureidkey="properties.region_code",
        animation_frame="period_label",
        hover_name="region_name",
        color_continuous_scale="Reds",
        range_color=(0, max_value * 1.05 if max_value else 1),
        labels={"hospitalizations": "Indlæggelser"},
        category_orders=category_orders,
    )
    fig.update_traces(marker_line_width=0.6, marker_line_color="#111")
    fig.update_geos(fitbounds="locations", visible=False, projection_scale=9.5, center={"lat": 56.0, "lon": 10.0})
    fig.update_layout(
        margin=dict(l=10, r=10, t=60, b=0),
        coloraxis_colorbar=dict(title="Indlæggelser"),
        transition={"duration": 400},
    )
    return fig


def build_timeseries(df: pd.DataFrame, region_code: Optional[str]) -> Figure:
    if not region_code or region_code == "ALL":
        filtered = (
            df.groupby("period_start", as_index=False)["hospitalizations"]
            .sum()
            .rename(columns={"hospitalizations": "total_hospitalizations"})
        )
        title = "Indlæggelser pr. måned – alle regioner"
        y = "total_hospitalizations"
    else:
        filtered = df.loc[df["region_code"] == region_code, ["region_name", "period_start", "hospitalizations"]]
        filtered = filtered.rename(columns={"hospitalizations": "region_hospitalizations"})
        title = f"Indlæggelser pr. måned – {filtered['region_name'].iloc[0]}"
        y = "region_hospitalizations"

    fig = px.line(
        filtered,
        x="period_start",
        y=y,
        markers=True,
        labels={y: "Indlæggelser", "period_start": "Måned"},
    )
    fig.update_layout(
        title=title,
        margin=dict(l=20, r=10, t=40, b=40),
        hovermode="x unified",
    )
    fig.update_traces(line=dict(width=3))
    return fig


df_regions = prepare_dataset()
regions_geojson = load_geojson(GEOJSON_PATH)
map_figure = build_map_figure(df_regions, regions_geojson)

region_options = [{"label": "Alle regioner", "value": "ALL"}] + [
    {"label": name, "value": code}
    for code, name in (
        df_regions[["region_code", "region_name"]]
        .drop_duplicates()
        .sort_values("region_name")
        .values.tolist()
    )
]

app = Dash(__name__)
app.title = "Vibe Demo – Dash"
server = app.server

app.layout = html.Div(
    className="app-container",
    children=[
        html.Header(
            [
                html.H1("COVID-19 indlæggelser – Danmark"),
                html.P("Månedlige indlæggelser pr. region med tidsanimation og linjegraf."),
            ],
            style={"padding": "1.5rem 2rem 0.5rem"},
        ),
        html.Main(
            [
                dcc.Graph(
                    id="hospital-map",
                    figure=map_figure,
                    config={"displaylogo": False},
                    style={"height": "70vh"},
                ),
                html.Div(
                    [
                        html.Label("Vælg region", htmlFor="region-dropdown"),
                        dcc.Dropdown(
                            id="region-dropdown",
                            options=region_options,
                            value="ALL",
                            clearable=False,
                        ),
                        dcc.Graph(
                            id="hospital-timeseries",
                            figure=build_timeseries(df_regions, "ALL"),
                            config={"displaylogo": False},
                        ),
                    ],
                    style={"padding": "0 2rem 2rem"},
                ),
            ]
        ),
    ],
)


@app.callback(Output("hospital-timeseries", "figure"), Input("region-dropdown", "value"))
def update_timeseries(region_code: Optional[str]):
    return build_timeseries(df_regions, region_code)


if __name__ == "__main__":
    app.run_server(debug=True)
