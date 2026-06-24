import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data
from format import format_currency, format_population, format_year


st.title("Trend Analysis")

if (
    "filtered_data" in st.session_state
    and isinstance(st.session_state.get("filtered_data"), pd.DataFrame)
    and not st.session_state.get("filtered_data").empty
):
    st.success(
        "Filters applied successfully."
    )
    data = st.session_state.get("filtered_data").copy()
else:
    st.info(
        "No filters are applied. The visualizations will use the full dataset."
    )
    data = load_data()

available_continents = sorted(data["continent"].dropna().unique())
available_years = sorted(data["year"].dropna().unique())

st.subheader("Choropleth Map")

# normalize ISO3 codes for choropleth
data = data.copy()
if "geo" in data.columns:
    data["iso_a3"] = data["geo"].str.upper()
else:
    data["iso_a3"] = None

c1, c2 = st.columns([1, 2], gap="medium")

with c1:
    metric_map = {"GDP per capita": "gdp_pcap", "Life expectancy": "lex", "Population": "pop"}
    metric_keys = list(metric_map.keys())
    choropleth_metric_label = st.selectbox("Metric", options=metric_keys, index=0, key="choropleth_metric")
    choropleth_step = st.slider("Year step", min_value=1, max_value=10, value=1, step=1, key="choropleth_step")

with c2:
    chosen_continents = st.multiselect(
        "Continents", options=available_continents, default=available_continents, key="choropleth_continents"
    )

st.space(size="xxsmall")

choropleth_metric = metric_map[choropleth_metric_label]
choropleth_df = data[data["continent"].isin(chosen_continents)].copy()
choropleth_df = choropleth_df[choropleth_df["year"].isin(available_years[::choropleth_step])]

if choropleth_df.empty:
    st.warning("No data available for the selected choropleth filters.")
else:
    color_arg = choropleth_metric

    fig = px.choropleth(
        choropleth_df,
        locations="iso_a3",
        color=choropleth_metric,
        hover_name="name",
        hover_data={
            "year": True,
            "continent": True,
            choropleth_metric: ":,.2f",
            "iso_a3": False,
        },
        animation_frame="year",
        color_continuous_scale="Viridis",
        projection="natural earth",
        labels={
            "gdp_pcap": "GDP per capita",
            "lex": "Life expectancy",
            "pop": "Population",
            "year": "Year",
        },
    )
    
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

st.divider()

st.subheader("Country Comparison")

c1, c2 = st.columns([1, 2], gap="medium")

with c1:
    ts_metric_label = st.selectbox(
        "Metric",
        options=list(metric_map.keys()),
        index=0,
        key="ts_metric",
    )
    ts_metric = metric_map[ts_metric_label]

with c2:
    countries_options = sorted(data["name"].dropna().unique())
    default_country = [countries_options[0]] if countries_options else []
    selected_countries = st.multiselect(
        "Countries",
        options=countries_options,
        default=default_country,
        key="ts_countries",
    )

if not selected_countries:
    st.info("Select one or more countries to see time series.")
else:
    ts_df = data[data["name"].isin(selected_countries)].copy()
    ts_df = ts_df.dropna(subset=[ts_metric, "year"]).sort_values(["name", "year"])
    if ts_df.empty:
        st.warning("No time series data available for the selected countries/metric.")
    else:
        ts_fig = px.line(
            ts_df,
            x="year",
            y=ts_metric,
            color="name",
            markers=True,
            labels={ts_metric: ts_metric_label, "year": "Year"},
        )
        ts_fig.update_layout(hovermode="x unified")
        st.plotly_chart(ts_fig, use_container_width=True)

# TODO: When I hover on one datapoint, I want to see the tooltip for all the datapoints of the selected countries!