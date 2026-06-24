import streamlit as st
import plotly.express as px
import pandas as pd

from data_loader import load_data
from format import format_currency, format_population, format_year


st.title("Visualizations")

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

st.subheader(f"GDP per capita vs life expectancy")
st.markdown(
    """
    Each bubble represents a country. The horizontal axis shows GDP per capita,
    the vertical axis shows life expectancy, and bubble size represents population.
    """
)

c1, c2 = st.columns([1, 2], gap="medium")

with c1:
    bubble_year = st.selectbox(
        "Year", options=available_years, index=len(available_years) - 1, key="bubble_year"
    )

with c2:
    bubble_continents = st.multiselect(
        "Continents", options=available_continents, default=available_continents, key="bubble_continents"
    )

bubble_df = data[data["continent"].isin(bubble_continents)]
bubble_year_data = bubble_df[bubble_df["year"] == bubble_year].copy()

bubble_year_data = bubble_year_data.dropna(subset=["gdp_pcap", "lex", "pop", "continent", "name"])

if bubble_year_data.empty:
    st.warning("No data is available for the selected bubble filters.")
else:
    bubble_fig = px.scatter(
        bubble_year_data,
        x="gdp_pcap",
        y="lex",
        size="pop",
        color="continent",
        hover_name="name",
        hover_data={
            "continent": True,
            "gdp_pcap": ":,.0f",
            "lex": ":.1f",
            "pop": ":,.0f",
            "year": True,
        },
        log_x=True,
        size_max=70,
        labels={
            "gdp_pcap": "GDP per capita",
            "lex": "Life expectancy",
            "pop": "Population",
            "continent": "Continent",
            "year": "Year",
        },
    )

    bubble_fig.update_layout(
        xaxis_title="GDP per capita [log scale]",
        yaxis_title="Life expectancy",
        legend_title="Continent",
    )

    st.plotly_chart(bubble_fig, use_container_width=True)

st.divider()

st.subheader("Continent comparison")

# Layout: left column for compact controls (year, metric), right column for continent multi-select
c1, c2 = st.columns([1, 2], gap="medium")

with c1:
    cont_year = st.selectbox(
        "Year", options=available_years, index=len(available_years) - 1, key="cont_year"
    )

    continent_metric_options = {
        "Average GDP per capita": "avg_gdp_pcap",
        "Average life expectancy": "avg_life_expectancy",
        "Total population": "total_population",
        "Number of countries": "countries",
    }

    selected_continent_metric_label = st.selectbox(
        "Metric", options=list(continent_metric_options.keys()), key="cont_metric"
    )

    selected_continent_metric = continent_metric_options[selected_continent_metric_label]

with c2:
    cont_continents = st.multiselect(
        "Continents", options=available_continents, default=available_continents, key="cont_continents"
    )

# Compute filtered data after widgets are created
cont_df = data[data["continent"].isin(cont_continents)]
cont_year_data = cont_df[cont_df["year"] == cont_year].copy()
cont_year_data = cont_year_data.dropna(subset=["gdp_pcap", "lex", "pop", "continent", "name"])

if cont_year_data.empty:
    st.warning("No data is available for the selected continent-comparison filters.")
else:
    continent_summary = (
        cont_year_data.groupby("continent", as_index=False)
        .agg(
            countries=("name", "nunique"),
            total_population=("pop", "sum"),
            avg_gdp_pcap=("gdp_pcap", "mean"),
            avg_life_expectancy=("lex", "mean"),
        )
    )

    continent_summary = continent_summary.sort_values(selected_continent_metric, ascending=False)

    continent_fig = px.bar(
        continent_summary,
        x="continent",
        y=selected_continent_metric,
        hover_data={
            "countries": True,
            "total_population": ":,.0f",
            "avg_gdp_pcap": ":,.0f",
            "avg_life_expectancy": ":.1f",
        },
        labels={
            "continent": "Continent",
            "countries": "Countries",
            "total_population": "Total population",
            "avg_gdp_pcap": "Average GDP per capita",
            "avg_life_expectancy": "Average life expectancy",
        },
    )

    continent_fig.update_layout(xaxis_title="Continent", yaxis_title=selected_continent_metric_label, showlegend=False)

    st.plotly_chart(continent_fig, use_container_width=True)

st.divider()

st.subheader(f"Top countries by selected metric")

c1, c2 = st.columns([1, 2], gap="medium")

with c1:
    top_year = st.selectbox(
        "Year", options=available_years, index=len(available_years) - 1, key="top_year"
    )

    metric_options = {
        "GDP per capita": "gdp_pcap",
        "Life expectancy": "lex",
        "Population": "pop",
    }
    selected_metric_label = st.selectbox(
        "Metric",
        options=list(metric_options.keys()),
        key="top_metric",
    )
    selected_metric = metric_options[selected_metric_label]

with c2:
    top_continents = st.multiselect(
        "Continents", options=available_continents, default=available_continents, key="top_continents"
    )

    top_n = st.slider(
        "Number of countries to show",
        min_value=5,
        max_value=25,
        value=15,
        step=5,
        key="top_n",
    )

top_df = data[data["continent"].isin(top_continents)]
top_year_data = top_df[top_df["year"] == top_year].copy()
top_year_data = top_year_data.dropna(subset=["gdp_pcap", "lex", "pop", "continent", "name"])

if top_year_data.empty:
    st.warning("No data is available for the selected top-countries filters.")
else:
    top_countries = (
        top_year_data.sort_values(selected_metric, ascending=False)
        .head(top_n)
        .sort_values(selected_metric, ascending=True)
    )

    bar_fig = px.bar(
        top_countries,
        x=selected_metric,
        y="name",
        color="continent",
        orientation="h",
        hover_name="name",
        hover_data={
            "continent": True,
            "gdp_pcap": ":,.0f",
            "lex": ":.1f",
            "pop": ":,.0f",
        },
        labels={
            "name": "Country",
            "gdp_pcap": "GDP per capita",
            "lex": "Life expectancy",
            "pop": "Population",
            "continent": "Continent",
        },
    )

    bar_fig.update_layout(
        xaxis_title=selected_metric_label,
        yaxis_title="Country",
        legend_title="Continent",
    )

    st.plotly_chart(bar_fig, use_container_width=True)