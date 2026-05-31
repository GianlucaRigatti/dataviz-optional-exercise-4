import streamlit as st
from datetime import date

from data_loader import load_data
from format import format_currency, format_population, format_year

st.title("Overview")
st.markdown(
"""
This dashboard explores global development indicators from the Gapminder dataset.

It focuses on three key variables:

- **GDP per capita** – economic output per person (PPP-adjusted).
- **Life expectancy** – average expected lifespan at birth.
- **Population** – total number of inhabitants.

The dataset spans multiple countries and years, allowing analysis of global inequality and development trends over time.
"""
)

data = load_data()

current_year = date.today().year
available_years = sorted(data["year"].unique())
selected_year = current_year if current_year in available_years else available_years[-1]

latest_df = data[data["year"] == selected_year]
previous_year = data[data["year"] < selected_year]["year"].max()
previous_df = data[data["year"] == previous_year]

countries_count = data["geo"].nunique()
min_year = int(data["year"].min())
max_year = int(data["year"].max())

world_pop = latest_df["pop"].sum()
world_pop_prev = previous_df["pop"].sum()
world_pop_delta = world_pop - world_pop_prev
avg_gdp = latest_df["gdp_pcap"].mean()
avg_gdp_prev = previous_df["gdp_pcap"].mean()
avg_gdp_delta = avg_gdp - avg_gdp_prev
avg_lex = latest_df["lex"].mean()
avg_lex_prev = previous_df["lex"].mean()
avg_lex_delta = avg_lex - avg_lex_prev

avg_gdp_display = format_currency(float(avg_gdp))
avg_gdp_delta_display = format_currency(float(avg_gdp_delta))
avg_lex_display = format_year(float(avg_lex))
avg_lex_delta_display = format_year(float(avg_lex_delta))

st.subheader("Dataset summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Countries", countries_count)
c2.metric("Years covered", f"{min_year}–{max_year}")
c3.metric("Rows", f"{len(data):,}")
c4.metric("Columns", len(data.columns))

st.subheader(f"Global snapshot ({selected_year})")

c1, c2, c3 = st.columns(3)

c1.metric(
    f"World population (vs. {previous_year})",
    f"{world_pop:,.0f}",
    delta=f"{world_pop_delta:,.0f} ({world_pop_delta / world_pop_prev:.1%})",
    border=True,
)

c2.metric(
    f"Avg GDP per capita (vs. {previous_year})",
	avg_gdp_display,
    delta=f"{avg_gdp_delta_display} ({avg_gdp_delta / avg_gdp_prev:.1%})",
    border=True,
)

c3.metric(
    f"Avg life expectancy (vs. {previous_year})",
	avg_lex_display,
    delta=f"{avg_lex_delta_display} ({avg_lex_delta / avg_lex_prev:.1%})",
    border=True,
)

st.subheader("Dataset")

st.dataframe(
    data.sort_values(["year", "name"]),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Data source")

st.markdown(
"""
The dataset is sourced from [Gapminder](https://www.gapminder.org/data/).  
All indicators have been preprocessed and merged into a single long format dataset for analysis.
"""
)

# TODO: provide details about how missing values were handled?