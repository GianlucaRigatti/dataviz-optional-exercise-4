import streamlit as st
import plotly.express as px

from data_loader import load_data
from continent_map import add_continent_column, get_continents
from format import format_currency, format_population, format_year


st.title("Visualizations")

st.markdown(
    """
    This page explores relationships between GDP per capita, life expectancy,
    population, and geography using interactive charts.
    """
)

data = load_data()
data = add_continent_column(data)

st.subheader("Filters")

available_years = sorted(data["year"].dropna().unique())
selected_year = st.selectbox(
    "Year",
    options=available_years,
    index=len(available_years) - 1,
)

continents = get_continents(data)
selected_continents = st.multiselect(
    "Continents",
    options=continents,
    default=continents,
)

continent_filtered = data[data["continent"].isin(selected_continents)]

available_countries = sorted(continent_filtered["name"].dropna().unique())

selected_countries = st.multiselect(
    "Countries",
    options=available_countries,
    placeholder="Leave empty to include all countries in the selected continents",
)

if selected_countries:
    filtered_data = continent_filtered[
        continent_filtered["name"].isin(selected_countries)
    ]
else:
    filtered_data = continent_filtered

year_data = filtered_data[filtered_data["year"] == selected_year].copy()

year_data = year_data.dropna(
    subset=["gdp_pcap", "lex", "pop", "continent", "name"]
)

if year_data.empty:
    st.warning("No data is available for the selected filters.")
    st.stop()


st.subheader(f"GDP per capita vs life expectancy ({selected_year})")

st.markdown(
    """
    Each bubble represents a country. The horizontal axis shows GDP per capita,
    the vertical axis shows life expectancy, and bubble size represents population.
    """
)

bubble_fig = px.scatter(
    year_data,
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
    xaxis_title="GDP per capita, log scale",
    yaxis_title="Life expectancy",
    legend_title="Continent",
)

st.plotly_chart(
    bubble_fig,
    use_container_width=True,
)


st.divider()

st.subheader(f"Top countries by selected metric ({selected_year})")

metric_options = {
    "GDP per capita": "gdp_pcap",
    "Life expectancy": "lex",
    "Population": "pop",
}

selected_metric_label = st.selectbox(
    "Metric",
    options=list(metric_options.keys()),
)

selected_metric = metric_options[selected_metric_label]

top_n = st.slider(
    "Number of countries to show",
    min_value=5,
    max_value=25,
    value=15,
    step=5,
)

top_countries = (
    year_data.sort_values(selected_metric, ascending=False)
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

st.plotly_chart(
    bar_fig,
    use_container_width=True,
)


st.divider()

st.subheader(f"Continent comparison ({selected_year})")

continent_summary = (
    year_data.groupby("continent", as_index=False)
    .agg(
        countries=("name", "nunique"),
        total_population=("pop", "sum"),
        avg_gdp_pcap=("gdp_pcap", "mean"),
        avg_life_expectancy=("lex", "mean"),
    )
)

continent_metric_options = {
    "Average GDP per capita": "avg_gdp_pcap",
    "Average life expectancy": "avg_life_expectancy",
    "Total population": "total_population",
    "Number of countries": "countries",
}

selected_continent_metric_label = st.selectbox(
    "Continent metric",
    options=list(continent_metric_options.keys()),
)

selected_continent_metric = continent_metric_options[
    selected_continent_metric_label
]

continent_summary = continent_summary.sort_values(
    selected_continent_metric,
    ascending=False,
)

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

continent_fig.update_layout(
    xaxis_title="Continent",
    yaxis_title=selected_continent_metric_label,
    showlegend=False,
)

st.plotly_chart(
    continent_fig,
    use_container_width=True,
)


st.divider()

st.subheader("Selected data summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Countries", year_data["name"].nunique())
c2.metric("Continents", year_data["continent"].nunique())
c3.metric("Population", format_population(float(year_data["pop"].sum())))
c4.metric("Year", int(selected_year))

c1, c2 = st.columns(2)

c1.metric(
    "Average GDP per capita",
    format_currency(float(year_data["gdp_pcap"].mean())),
)

c2.metric(
    "Average life expectancy",
    format_year(float(year_data["lex"].mean())),
)

with st.expander("Show chart data"):
    st.dataframe(
        year_data[
            ["continent", "geo", "name", "year", "gdp_pcap", "lex", "pop"]
        ].sort_values(["continent", "name"]),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Continent labels are manually assigned because the source data does not include a continent column."
)