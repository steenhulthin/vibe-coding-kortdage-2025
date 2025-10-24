import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="COVID-19 – Globalt overblik", layout="wide")
st.title("Globalt COVID-19-overblik – Streamlit")
st.caption(
    "Data: Our World in Data (hospitaliserede og dødsfald pr. mio. indbyggere). "
    "Periodevælgeren opsummerer værdier for kortet og tidsserien."
)

DATA_PATH = "python/data/owid_covid_global_monthly.csv"
METRIC_COLUMNS = [
    "hosp_patients_per_million",
    "weekly_hosp_admissions_per_million",
    "icu_patients_per_million",
    "new_deaths_per_million",
    "total_deaths_per_million",
]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    elif "month_start" in df.columns:
        df["date"] = pd.to_datetime(df["month_start"])
    else:
        raise ValueError("Datasættet skal indeholde 'date' eller 'month_start'.")

    for col in METRIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["year_month"] = df["date"].dt.to_period("M")
    return df


df = load_data(DATA_PATH)
if df.empty:
    st.error("Kunne ikke indlæse OWID-data.")
    st.stop()

periods = (
    df["year_month"]
    .dropna()
    .sort_values()
    .unique()
)
period_labels = [f"{p.year}-{p.month:02d}" for p in periods]
period_map = dict(zip(period_labels, periods))

default_start = period_labels[-12] if len(period_labels) >= 12 else period_labels[0]
default_end = period_labels[-1]

col_period, col_country = st.columns([2, 1])
with col_period:
    start_label, end_label = st.select_slider(
        "Periode (år-måned)",
        options=period_labels,
        value=(default_start, default_end),
    )

start_period = period_map[start_label]
end_period = period_map[end_label]

with col_country:
    valid_countries = (
        df.loc[df["iso_code"].str.len() == 3, "location"].dropna().unique().tolist()
    )
    valid_countries.sort()
    country_label = st.selectbox("Land", ["Alle lande"] + valid_countries)

period_mask = df["year_month"].between(start_period, end_period)
period_df = df.loc[period_mask].copy()

map_metrics = ["hosp_patients_per_million", "new_deaths_per_million"]
missing_cols = [col for col in map_metrics if col not in period_df.columns]
if missing_cols:
    st.error(f"Mangler kolonner i datasættet: {', '.join(missing_cols)}")
    st.stop()

map_df = (
    period_df.groupby(["iso_code", "location"], as_index=False)[map_metrics].sum()
)
map_df = map_df[map_df["iso_code"].str.len() == 3].fillna(0)

if map_df.empty:
    st.warning("Ingen landedata tilgængelig for den valgte periode.")
else:
    hosp_max = map_df["hosp_patients_per_million"].max() or 0
    deaths_max = map_df["new_deaths_per_million"].max() or 0

    fig_map = go.Figure()
    fig_map.add_choropleth(
        locations=map_df["iso_code"],
        z=map_df["hosp_patients_per_million"],
        text=map_df["location"],
        colorscale="Blues",
        marker_line_width=0.2,
        colorbar_title="Indlæggelser pr. mio.",
        zmin=0,
        zmax=hosp_max if hosp_max > 0 else None,
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Indlæggelser pr. mio.: %{z:.1f}<br>"
            "Dødsfald pr. mio.: %{customdata:.1f}<extra></extra>"
        ),
        customdata=map_df["new_deaths_per_million"],
    )

    if deaths_max > 0:
        fig_map.add_choropleth(
            locations=map_df["iso_code"],
            z=map_df["new_deaths_per_million"],
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0.65)"]],
            showscale=False,
            marker_line_width=0,
            zmin=0,
            zmax=deaths_max,
            hoverinfo="skip",
        )

    fig_map.update_layout(
        title="Hospitaliserede (farve) og dødsfald (skraveret) pr. mio. indbyggere",
        margin=dict(l=0, r=0, t=60, b=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)

selection_df = period_df.copy()
if country_label != "Alle lande":
    selection_df = selection_df[selection_df["location"] == country_label]
    series_title = country_label
else:
    series_title = "Hele verden"
    selection_df = (
        selection_df.groupby(["year_month"], as_index=False)[map_metrics].sum()
    )

if selection_df.empty:
    st.warning("Ingen tidsserie tilgængelig for valget.")
else:
    if "location" in selection_df.columns and country_label == "Alle lande":
        # Already aggregated, ensure no leftover location column.
        selection_df = selection_df.drop(columns=["location"], errors="ignore")

    ts_df = (
        selection_df.groupby("year_month", as_index=False)[map_metrics].sum().sort_values("year_month")
    )
    ts_df["month_start"] = ts_df["year_month"].dt.to_timestamp()

    fig_series = go.Figure()
    fig_series.add_trace(
        go.Scatter(
            x=ts_df["month_start"],
            y=ts_df["hosp_patients_per_million"],
            name="Indlæggelser pr. mio.",
            mode="lines+markers",
        )
    )
    fig_series.add_trace(
        go.Scatter(
            x=ts_df["month_start"],
            y=ts_df["new_deaths_per_million"],
            name="Dødsfald pr. mio.",
            mode="lines+markers",
        )
    )
    fig_series.update_layout(
        title=f"Månedlig udvikling – {series_title}",
        xaxis_title="Måned",
        yaxis_title="Per mio. indbyggere",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    st.plotly_chart(fig_series, use_container_width=True)
