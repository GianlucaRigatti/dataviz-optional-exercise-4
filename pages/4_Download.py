import pandas as pd
import streamlit as st

from data_loader import load_data


st.title("Download")
st.markdown(
	"""
	Export the data currently selected in **Data Explorer**.
	If no filters are active, the full dataset is downloaded.
	"""
)

if (
    "filtered_data" in st.session_state
    and isinstance(st.session_state.get("filtered_data"), pd.DataFrame)
):
	data = st.session_state.get("filtered_data").copy()
	st.success(f"Ready to download {len(data):,} filtered rows.")
else:
	data = load_data()
	st.info(f"No filtered data found. Downloading the full dataset with {len(data):,} rows.")
	
csv_data = data.to_csv(index=False).encode("utf-8")
st.download_button(
	label="Download CSV",
	data=csv_data,
	file_name="gapminder_filtered.csv",
	mime="text/csv",
)

st.subheader("Preview data")

with st.expander("Selected Filters", expanded=False):
    filters = st.session_state.get("filters")
    if filters:
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            st.write("**Continents**")
            st.write(", ".join(filters.get("continents", [])) or "None")
        with c2:
            st.write("**Countries**")
            st.write(", ".join(filters.get("countries", [])) or "None")
        with c3:
            year_range = filters.get("year_range")
            st.write("**Year range**")
            st.write(f"{year_range[0]} – {year_range[1]}" if year_range else "All")

st.dataframe(data.head(200), use_container_width=True, hide_index=True)
