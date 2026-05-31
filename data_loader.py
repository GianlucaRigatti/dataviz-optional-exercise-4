from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(data_dir: str | Path = "data") -> pd.DataFrame:
    data_path = Path(data_dir)
    data = pd.read_csv(data_path / "gapminder_aggregated.csv")
    return data