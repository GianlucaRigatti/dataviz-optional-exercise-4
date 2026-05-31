import streamlit as st

st.title("Overview")
st.caption("High-level summary of the Gapminder dataset and key indicators.")

st.markdown(
	"""
This dashboard explores GDP per capita, life expectancy, and population trends
across countries and time. Use the sidebar to navigate the full analysis.
"""
)

st.subheader("At-a-glance")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Years covered", "1952–2021")
col2.metric("Countries", "142")
col3.metric("Latest population", "7.9B")
col4.metric("GDP per capita range", "$300–$120k")
col5.metric("Life expectancy range", "30–85")

st.subheader("Dataset snapshot")
snapshot_data = [
	{"country": "Italy", "year": 2021, "gdp_pcap": 42000, "lex": 82.9, "pop": 59000000},
	{"country": "India", "year": 2021, "gdp_pcap": 7800, "lex": 69.7, "pop": 1390000000},
	{"country": "Brazil", "year": 2021, "gdp_pcap": 15500, "lex": 75.5, "pop": 213000000},
]
st.dataframe(snapshot_data, use_container_width=True)

st.subheader("Key insights (placeholder)")
st.markdown(
	"""
- Add 2–3 bullet points summarizing key takeaways.
- Highlight notable regional patterns or outliers.
- Link to the most relevant visualization page.
"""
)

with st.expander("Data sources and definitions"):
	st.markdown(
		"""
- **Source**: [Gapminder](https://www.gapminder.org/data/)
- **GDP per capita**: International dollars, PPP (2021 prices).
- **Life expectancy**: Expected years of life at birth.
- **Population**: Total number of inhabitants.
"""
	)
