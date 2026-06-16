import streamlit as st

from data_loader import load_data
from format import format_currency, format_population, format_year
from continent_map import add_continent_column, get_continents, COUNTRY_TO_CONTINENT


st.title("Data Explorer")
st.caption("Filter the Gapminder dataset by continent, country, and year range.")

data = load_data().copy()

data["continent"] = data["name"].map(COUNTRY_TO_CONTINENT)
data["continent"] = data["continent"].fillna("Unclassified")

st.subheader("Filters")

continents = sorted(data["continent"].unique())

selected_continents = st.multiselect(
    "Continent",
    options=continents,
    default=continents,
)

continent_filtered = data[data["continent"].isin(selected_continents)]

countries = sorted(continent_filtered["name"].unique())

selected_countries = st.multiselect(
    "Country",
    options=countries,
    default=countries,
)

min_year = int(data["year"].min())
max_year = int(data["year"].max())

selected_year_range = st.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1,
)

filtered_data = continent_filtered[
    (continent_filtered["name"].isin(selected_countries))
    & (continent_filtered["year"] >= selected_year_range[0])
    & (continent_filtered["year"] <= selected_year_range[1])
].copy()

filtered_data = filtered_data.sort_values(["year", "continent", "name"])

st.session_state["filtered_data"] = filtered_data

st.subheader("Filtered summary")

if filtered_data.empty:
    st.warning("No records match the selected filters.")
else:
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{len(filtered_data):,}")
    c2.metric("Countries", filtered_data["name"].nunique())
    c3.metric("Continents", filtered_data["continent"].nunique())
    c4.metric(
        "Years covered",
        f"{int(filtered_data['year'].min())}–{int(filtered_data['year'].max())}",
    )

    latest_year = int(filtered_data["year"].max())
    latest_data = filtered_data[filtered_data["year"] == latest_year]

    st.subheader(f"Snapshot for latest selected year ({latest_year})")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Population",
        format_population(float(latest_data["pop"].sum())),
        border=True,
    )

    c2.metric(
        "Average GDP per capita",
        format_currency(float(latest_data["gdp_pcap"].mean())),
        border=True,
    )

    c3.metric(
        "Average life expectancy",
        format_year(float(latest_data["lex"].mean())),
        border=True,
    )

    st.subheader("Filtered dataset")

    display_data = filtered_data[
        ["continent", "geo", "name", "year", "gdp_pcap", "lex", "pop"]
    ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )