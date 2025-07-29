# 🌊 Coral Reef Health Monitor

A real-time coral reef monitoring system using free cloud tools: **Neon PostgreSQL** + **Streamlit**.

## 🚀 Quick Start

### 1. Set up your environment

First, rename the template file and add your Neon database credentials:

```bash
cp env_template.txt .env
```

Then edit `.env` with your actual Neon database credentials:

```env
NEON_HOST=your-neon-host.neon.tech
NEON_DATABASE=your-database-name
NEON_USER=your-username
NEON_PASSWORD=your-password
NEON_PORT=5432
```

### 2. Activate virtual environment

```bash
source coral-reef-venv/bin/activate
```

### 3. Test database connection

```bash
python test_connection.py
```

### 4. Run the data pipeline

```bash
python coral_reef_pipeline.py
```

### 5. Launch the dashboard

```bash
streamlit run dashboard.py
```

## 📊 Features

- **Real-time monitoring** of coral reef health metrics
- **Temperature tracking** with Sea Surface Temperature (SST) data
- **Bleaching risk assessment** using Degree Heating Weeks (DHW)
- **Interactive maps** showing global reef locations
- **Filtering capabilities** by reef and time period
- **Beautiful visualizations** with Plotly charts

## 🛠️ Tech Stack

- **Database**: Neon PostgreSQL (free tier)
- **Dashboard**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Environment**: Python 3.11

## 📈 Data Sources

The system currently uses simulated data for demonstration, including:
- Great Barrier Reef (Australia)
- Hawaiian Islands (USA)
- Fiji Reefs (Fiji)
- Mesoamerican Reef (Mexico)

## 🔧 Project Structure

```
coral-reef-data/
├── coral_reef_pipeline.py    # Data pipeline
├── dashboard.py              # Streamlit dashboard
├── test_connection.py        # Database connection test
├── requirements.txt          # Python dependencies
├── env_template.txt          # Environment template
└── coral-reef-venv/         # Virtual environment
```

## 🎯 Next Steps

1. **Get Neon Database**: Sign up at [neon.tech](https://neon.tech) for free PostgreSQL
2. **Update credentials**: Add your database details to `.env`
3. **Run the pipeline**: Generate and store reef data
4. **Launch dashboard**: View your coral reef monitoring system!

## 🌟 Free Tools Used

- **Neon**: Serverless PostgreSQL with generous free tier
- **Streamlit**: Free hosting for data apps
- **GitHub**: Version control and collaboration
- **Python**: Open-source data science ecosystem 
