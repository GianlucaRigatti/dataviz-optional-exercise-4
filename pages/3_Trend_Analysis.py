import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data
from format import format_currency, format_population, format_year


st.title("Trend Analysis")

if (
    "filtered_data" in st.session_state
    and isinstance(st.session_state.get("filtered_data"), pd.DataFrame)
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
    metric_map = {"GDP per Capita": "gdp_pcap", "Life Expectancy": "lex", "Population": "pop"}
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
        custom_data=[
            "continent",
            "year",
            choropleth_metric,
        ],
        animation_frame="year",
        color_continuous_scale="Viridis",
        projection="natural earth",
    )
    hover_templates = {
        "gdp_pcap": (
            "<b>%{hovertext}</b><br>"
            "Continent: %{customdata[0]}<br>"
            "Year: %{customdata[1]}<br>"
            "GDP per Capita: $%{customdata[2]:,.0f}"
            "<extra></extra>"
        ),
        "lex": (
            "<b>%{hovertext}</b><br>"
            "Continent: %{customdata[0]}<br>"
            "Year: %{customdata[1]}<br>"
            "Life Expectancy: %{customdata[2]:.1f} years"
            "<extra></extra>"
        ),
        "pop": (
            "<b>%{hovertext}</b><br>"
            "Continent: %{customdata[0]}<br>"
            "Year: %{customdata[1]}<br>"
            "Population: %{customdata[2]:,.0f}"
            "<extra></extra>"
        ),
    }

    # Apply hover template to initial trace
    for trace in fig.data:
        trace.hovertemplate = hover_templates[choropleth_metric]

    # Apply hover template to animation frames
    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_templates[choropleth_metric]
    
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
            custom_data=["name"],
            labels={
                ts_metric: ts_metric_label,
                "year": "Year",
                "name": "Country",
            },
        )
        ts_fig.update_layout(hovermode="x unified")
        hover_templates = {
            "gdp_pcap": (
                "<b>%{customdata[0]}</b><br>"
                "GDP per Capita: $%{y:,.0f}"
                "<extra></extra>"
            ),
            "lex": (
                "<b>%{customdata[0]}</b><br>"
                "Life Expectancy: %{y:.1f} years"
                "<extra></extra>"
            ),
            "pop": (
                "<b>%{customdata[0]}</b><br>"
                "Population: %{y:,.0f}"
                "<extra></extra>"
            ),
        }
        ts_fig.update_traces(
            hovertemplate=hover_templates[ts_metric]
        )

        st.plotly_chart(ts_fig, use_container_width=True)