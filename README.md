# dataviz-optional-exercise-4

## Assignment

Build a *Streamlit* dashboard using the Gapminder dataset. The app should have these pages:
- **Overview** to introduce the dataset and show basic metrics
- **Data Explorer** to filter by continent, country, and year range
- **Visualizations** to show interactive charts such as GDP per capita vs life expectancy with population as bubble size
- **Trend Analysis** to compare countries over time
- **Download** to export the filtered data

Put the project in a Git repository with a clean `README.md`, and a working Dockerfile. Send the repo to snoei@fbk.eu before the exam.

## Datasets used

Based on free material from [GAPMINDER.ORG](https://www.gapminder.org/data/), CC-BY LICENSE. The relevant files downloaded in the `data/` directory are:
- `gdp_pcap` : Gross Domestic Product per person adjusted for differences in purchasing power (in international dollars, fixed 2021 prices, PPP based on 2021 ICP).
- `lex` : The number of years a newborn infant would live if the current mortality rates at different ages were to stay the same throughout its life.
- `pop` : Total population counts the number of inhabitants in the territory.

# How to run the app

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run main.py`