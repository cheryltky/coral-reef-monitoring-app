# Setup

Requires Python 3.11. The project uses a free Neon PostgreSQL database and
Streamlit. Dependencies are listed in [requirements.txt](../requirements.txt).

## 1. Set up your environment

Copy the template file and add your own Neon database credentials. The
template contains placeholders only; the real `.env` file must never be
committed.

```bash
cp env_template.txt .env
```

Then edit `.env`. The variable names are:

```env
NEON_HOST=your-neon-host.neon.tech
NEON_DATABASE=your-database-name
NEON_USER=your-username
NEON_PASSWORD=your-password
NEON_PORT=5432
```

To get a database, sign up at [neon.tech](https://neon.tech) for free
PostgreSQL and copy its connection details into `.env`. All three scripts
read these variables with `python-dotenv` and connect with SSL required.

## 2. Activate a virtual environment

```bash
source coral-reef-venv/bin/activate
```

The environment is not part of the repository; create one with
`python -m venv coral-reef-venv` and `pip install -r requirements.txt` if it
does not exist.

## 3. Test the database connection

```bash
python test_connection.py
```

## 4. Run the data pipeline

Creates the `reef_data` table (dropping any existing copy), generates the
simulated readings and stores them:

```bash
python coral_reef_pipeline.py
```

## 5. Launch the dashboard

```bash
streamlit run dashboard.py
```

## Project structure

```
coral-reef-data/
├── docs/                     setup and methodology
├── coral_reef_pipeline.py    data pipeline
├── dashboard.py              Streamlit dashboard
├── test_connection.py        database connection test
├── requirements.txt          Python dependencies
├── env_template.txt          environment template
└── coral-reef-venv/          virtual environment (not committed)
```
