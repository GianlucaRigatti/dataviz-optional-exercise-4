import streamlit as st

st.set_page_config(page_title="Gapminder Dashboard", layout="wide")

pages = {
    "Gapminder Dashboard": [
        st.Page("pages/0_Overview.py", title="Overview"),
        st.Page("pages/1_Data_Explorer.py", title="Data Explorer"),
        st.Page("pages/2_Visualizations.py", title="Visualizations"),
        st.Page("pages/3_Trend_Analysis.py", title="Trend Analysis"),
        st.Page("pages/4_Download.py", title="Download"),
    ]
}

navigation = st.navigation(pages)
navigation.run()