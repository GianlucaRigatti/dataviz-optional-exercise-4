# dataviz-optional-exercise-4

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0.3-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.8.0-3F4F75?logo=plotly&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-29.6.1-2496ED?logo=docker&logoColor=white)

Developed by Gianluca Rigatti and Giuseppe Screnci for the *Data Visualisation Lab* course.

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
  - GDP per Capita versus Life Expectancy, with Population represented by bubble size
  - Continent-level Comparisons
  - Rankings of the Top Countries by GDP per Capita, Life Expectancy, or Population
- **Trend Analysis** includes:
  - An animated Choropleth Map that visualizes GDP per Capita, Life Expectancy, or Population over time
  - Country Comparisons over time
- **Download** exports the currently filtered dataset as a CSV file.

Filters selected in the **Data Explorer** page are stored in a Streamlit session and applied to the *Visualization*, *Trend Analysis*, and *Download* pages.

---

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

---

## Project Structure

```text
.
├── data/       # Contains the source and aggregated datasets
│   ├── gdp_pcap.csv
│   ├── lex.csv
│   ├── pop.csv
│   └── gapminder_aggregated.csv
├── pages/          # Contains the Streamlit pages for the dashboard
│   ├── 0_Overview.py
│   ├── 1_Data_Explorer.py
│   ├── 2_Visualizations.py
│   ├── 3_Trend_Analysis.py
│   └── 4_Download.py
├── continent_map.py    # Used for mapping countries to continents
├── data_loader.py      # Used to load the aggregated dataset
├── format.py           # Contains formatting functions
├── main.py
├── preprocessing.ipynb     # Notebook for data preprocessing
├── requirements.txt
└── Dockerfile
```

---

## Run Locally

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

- On Windows:

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

---

## Run with Docker

Build the Docker image:

```bash
docker build -t gapminder-dashboard .
```

Run the container:

```bash
docker run -d -p 8501:8501 --name gapminder-app gapminder-dashboard
```
Note: The `-d` flag runs the container in the background. Remove it if you want to see the logs in your terminal.

Open the dashboard at:

```text
http://localhost:8501
```

Stop the container:
```bash
docker stop gapminder-app
```
