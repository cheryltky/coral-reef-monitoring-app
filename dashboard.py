import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    return psycopg2.connect(
        host=os.getenv('NEON_HOST'),
        database=os.getenv('NEON_DATABASE'),
        user=os.getenv('NEON_USER'),
        password=os.getenv('NEON_PASSWORD'),
        port=os.getenv('NEON_PORT', 5432),
        sslmode='require'
    )

def main():
    st.set_page_config(
        page_title="Coral Reef Monitor",
        page_icon="��",
        layout="wide"
    )
    
    st.title("🌊 Coral Reef Health Monitor")
    st.markdown("*Powered by free cloud tools: Neon + Streamlit*")
    
    try:
        conn = get_database_connection()
        df = pd.read_sql("SELECT * FROM reef_data ORDER BY date DESC", conn)
        conn.close()
        
        st.success(f"✅ Connected to Neon database - {len(df)} records loaded")
        
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    selected_reef = st.sidebar.selectbox(
        "Select Reef",
        options=['All'] + list(df['reef_id'].unique()),
        format_func=lambda x: x if x == 'All' else f"{x} - {df[df['reef_id'] == x]['reef_name'].iloc[0]}"
    )
    
    # Filter data
    filtered_df = df.copy()
    if selected_reef != 'All':
        filtered_df = filtered_df[filtered_df['reef_id'] == selected_reef]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_sst = filtered_df['sst_celsius'].mean()
        st.metric("Average SST", f"{avg_sst:.1f}°C")
    
    with col2:
        max_dhw = filtered_df['dhw_value'].max()
        st.metric("Max DHW", f"{max_dhw:.1f}")
    
    with col3:
        high_risk_days = len(filtered_df[filtered_df['bleaching_risk'] == 'High Risk'])
        st.metric("High Risk Days", high_risk_days)
    
    with col4:
        total_reefs = filtered_df['reef_id'].nunique()
        st.metric("Reefs Monitored", total_reefs)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Temperature Trends")
        time_data = filtered_df.groupby('date')['sst_celsius'].mean().reset_index()
        fig = px.line(time_data, x='date', y='sst_celsius', title='SST Over Time')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Bleaching Risk Distribution")
        risk_counts = filtered_df['bleaching_risk'].value_counts()
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, title='Risk Level Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Map
    st.subheader("Global Reef Locations")
    reef_locations = filtered_df[['reef_id', 'reef_name', 'latitude', 'longitude', 'country']].drop_duplicates()
    
    fig = px.scatter_mapbox(
        reef_locations,
        lat='latitude',
        lon='longitude',
        hover_data=['reef_name', 'country'],
        zoom=1,
        mapbox_style="carto-positron"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(filtered_df.tail(100))

if __name__ == "__main__":
    main()
