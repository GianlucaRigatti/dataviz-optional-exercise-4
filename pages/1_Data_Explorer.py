import streamlit as st

from data_loader import load_data
from format import format_currency, format_population, format_year
from continent_map import add_continent_column, get_continents, COUNTRY_TO_CONTINENT


st.title("Data Explorer")
st.info(
"""
Selected filters will be applied to all other pages in the dashboard.
"""
)

data = load_data().copy()

st.subheader("Filters")

# Initialize session state once
if "filters" not in st.session_state:
    st.session_state["filters"] = {
        "continents": sorted(data["continent"].unique()),
        "countries": sorted(data["name"].unique()),
        "year_range": (int(data["year"].min()), int(data["year"].max())),
    }

filters = st.session_state["filters"]

# Continent filter
continents = sorted(data["continent"].unique())
selected_continents = st.multiselect(
    "Continent",
    options=continents,
    default=filters["continents"],
    key="continents_select",
)
st.session_state["filters"]["continents"] = selected_continents
continent_filtered = data[data["continent"].isin(selected_continents)]

# Country filter within selected continents
countries = sorted(continent_filtered["name"].unique())
selected_countries = st.multiselect(
    "Country",
    options=countries,
    default=[c for c in filters["countries"] if c in countries],
    key="countries_select",
)
st.session_state["filters"]["countries"] = selected_countries

# Year range filter
min_year = int(data["year"].min())
max_year = int(data["year"].max())
selected_year_range = st.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=filters["year_range"],
    step=1,
    key="year_slider",
)
st.session_state["filters"]["year_range"] = selected_year_range

# Apply filters
filtered_data = continent_filtered[
    (continent_filtered["name"].isin(selected_countries))
    & (continent_filtered["year"] >= selected_year_range[0])
    & (continent_filtered["year"] <= selected_year_range[1])
].copy()
filtered_data = filtered_data.sort_values(["year", "continent", "name"])
st.session_state["filtered_data"] = filtered_data

st.subheader("Filtered Dataset Summary")

if filtered_data.empty:
    st.warning("No records match the selected filters.")
else:
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Countries", filtered_data["name"].nunique())
    c2.metric("Continents", filtered_data["continent"].nunique())
    c3.metric(
        "Years Covered",
        f"{int(filtered_data['year'].min())}–{int(filtered_data['year'].max())}",
    )
    c4.metric("Rows", f"{len(filtered_data):,}")
    c5.metric("Columns", f"{len(filtered_data.columns)}")

    st.subheader("Filtered Dataset")

    st.dataframe(
        filtered_data.sort_values(["year", "continent", "name"]),
        use_container_width=True,
        hide_index=True
    )