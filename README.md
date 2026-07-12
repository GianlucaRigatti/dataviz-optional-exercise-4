# dataviz-optional-exercise-4

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker&logoColor=white)

## Assignment

Build a *Streamlit* dashboard using the Gapminder dataset. The app should have these pages:
- **Overview** to introduce the dataset and show basic metrics
- **Data Explorer** to filter by continent, country, and year range
- **Visualizations** to show interactive charts such as GDP per capita vs life expectancy with population as bubble size
- **Trend Analysis** to compare countries over time
- **Download** to export the filtered data

Put the project in a Git repository with a clean `README.md`, and a working Dockerfile. Send the repo to snoei@fbk.eu before the exam.

---

## Datasets Used

Based on free material from [GAPMINDER.ORG](https://www.gapminder.org/data/), CC-BY LICENSE. The relevant files downloaded in the `data/` directory are:
- `gdp_pcap` : Gross Domestic Product per person adjusted for differences in purchasing power (in international dollars, fixed 2021 prices, PPP based on 2021 ICP).
- `lex` : The number of years a newborn infant would live if the current mortality rates at different ages were to stay the same throughout its life.
- `pop` : Total population counts the number of inhabitants in the territory.

---

## Dashboard Features

The application is organized into five Streamlit pages:

- **Overview** provides an introduction to the dataset, summary statistics, global indicators, and a complete data table.
- **Data Explorer** allows filtering by continent, country, and year range.
- **Visualizations** includes:
  - GDP per capita versus life expectancy, with population represented by bubble size
  - Continent-level comparisons
  - Rankings of the top countries by GDP per capita, life expectancy, or population
- **Trend Analysis** includes an animated world map and country comparisons over time.
- **Download** exports the currently filtered dataset as a CSV file.

Filters selected in the Data Explorer are stored in the Streamlit session and applied to the visualization, trend-analysis, and download pages.

## Data Preparation

The source Gapminder datasets are converted from wide to long format and merged into a single file containing:

- `geo`: country code
- `name`: country name
- `year`: observation year
- `gdp_pcap`: GDP per capita
- `lex`: life expectancy
- `pop`: population
- `continent`: continent classification

The preprocessing workflow is available in `preprocessing.ipynb`. The generated dataset used by the dashboard is stored at:

```text
data/gapminder_aggregated.csv
```

## Project Structure

```text
.
├── data/
│   └── gapminder_aggregated.csv
├── pages/
│   ├── 0_Overview.py
│   ├── 1_Data_Explorer.py
│   ├── 2_Visualizations.py
│   ├── 3_Trend_Analysis.py
│   └── 4_Download.py
├── continent_map.py
├── data_loader.py
├── format.py
├── main.py
├── preprocessing.ipynb
├── requirements.txt
└── Dockerfile
```

## Run Locally

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run main.py
```

The application will be available at:

```text
http://localhost:8501
```

## Run with Docker

Build the Docker image:

```bash
docker build -t gapminder-dashboard .
```

Run the container:

```bash
docker run -p 8501:8501 gapminder-dashboard
```

Open the dashboard at:

```text
http://localhost:8501
```

## Technologies

- Python 3.11
- Streamlit
- Pandas
- Plotly
- Docker