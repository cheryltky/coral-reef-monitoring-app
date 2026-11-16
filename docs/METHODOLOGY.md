# Methodology

How the simulated data is generated, how risk is classified and how the
pieces fit together.

## Tech stack

- **Database:** Neon PostgreSQL (free tier)
- **Dashboard:** Streamlit
- **Visualisation:** Plotly
- **Data processing:** Pandas, NumPy
- **Environment:** Python 3.11

Free tools used: Neon (serverless PostgreSQL with a generous free tier),
Streamlit (free hosting for data apps), GitHub (version control and
collaboration) and Python (open-source data science ecosystem).

## Data source

The system currently uses simulated data for demonstration. Every row is
tagged `Simulated` in the `data_source` column. The five simulated reef
sites are:

| Reef ID | Name | Country |
|---|---|---|
| GBR001 | Great Barrier Reef - Northern | Australia |
| GBR002 | Great Barrier Reef - Central | Australia |
| HAW001 | Hawaiian Islands | USA |
| FIJ001 | Fiji Reefs | Fiji |
| MEX001 | Mesoamerican Reef | Mexico |

The original README listed four locations (Great Barrier Reef, Hawaiian
Islands, Fiji Reefs, Mesoamerican Reef); the Great Barrier Reef is
simulated as a northern and a central site.

Each site gets one reading per day for the 30 days up to the run date, as
generated in [`coral_reef_pipeline.py`](../coral_reef_pipeline.py):

- Sea surface temperature (SST) is a 26.0 degree Celsius base, plus a
  seasonal sine term with an amplitude of 2.0 degrees driven by day of year,
  plus random noise with a standard deviation of 0.5.
- Degree Heating Weeks (DHW) is 0 when SST is at or below the 27.0 degree
  bleaching threshold, and otherwise (SST minus 27.0) multiplied by 7. The
  value is computed per day and is not accumulated over a rolling window.
- The seasonal term depends only on the date, not on a site's latitude, so
  only the random noise differs between sites.

## Bleaching risk classification

| DHW | Risk label |
|---|---|
| 8 or more | High Risk |
| 4 to under 8 | Moderate Risk |
| 1 to under 4 | Low Risk |
| under 1 | No Risk |

## Storage

The pipeline writes to a single table, `reef_data`, with columns `id`,
`reef_id`, `reef_name`, `latitude`, `longitude`, `country`, `date`,
`sst_celsius`, `dhw_value`, `bleaching_risk`, `data_source` and
`created_at`. `(reef_id, date)` is unique, and re-inserting an existing pair
updates the SST, DHW and risk values. `create_tables` drops and recreates
the table on every run to guarantee a clean schema, so a pipeline run
replaces all stored data.

## Dashboard

[`dashboard.py`](../dashboard.py) reads the whole table and offers:

- Real-time monitoring of reef health metrics: the app queries the database
  on each load, although the underlying readings are simulated
- A reef selector in the sidebar (the original README also listed a
  time-period filter; the current code filters by reef only)
- Four headline metrics: average SST, maximum DHW, count of High Risk days
  and number of reefs monitored
- A line chart of mean SST over time and a pie chart of risk levels
- An interactive map of reef locations
- A raw data table showing the last 100 rows

If the database connection fails the app shows the error message and stops.
