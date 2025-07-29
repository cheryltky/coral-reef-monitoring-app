import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from datetime import datetime, timedelta
import time
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class CoralReefPipeline:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('NEON_HOST'),
            'database': os.getenv('NEON_DATABASE'),
            'user': os.getenv('NEON_USER'),
            'password': os.getenv('NEON_PASSWORD'),
            'port': os.getenv('NEON_PORT', 5432),
            'sslmode': 'require'
        }
        
    def create_tables(self):
        """Create tables in Neon database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        # Drop table if it exists to ensure clean schema
        cursor.execute("DROP TABLE IF EXISTS reef_data")
        
        cursor.execute("""
            CREATE TABLE reef_data (
                id SERIAL PRIMARY KEY,
                reef_id VARCHAR(50),
                reef_name VARCHAR(255),
                latitude DECIMAL(10, 6),
                longitude DECIMAL(10, 6),
                country VARCHAR(100),
                date DATE,
                sst_celsius DECIMAL(5, 2),
                dhw_value DECIMAL(5, 2),
                bleaching_risk VARCHAR(50),
                data_source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(reef_id, date)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tables created in Neon database")
    
    def generate_reef_data(self):
        """Generate realistic coral reef data"""
        reefs = [
            {'id': 'GBR001', 'name': 'Great Barrier Reef - Northern', 'lat': -14.5, 'lon': 145.0, 'country': 'Australia'},
            {'id': 'GBR002', 'name': 'Great Barrier Reef - Central', 'lat': -18.0, 'lon': 147.0, 'country': 'Australia'},
            {'id': 'HAW001', 'name': 'Hawaiian Islands', 'lat': 21.5, 'lon': -158.0, 'country': 'USA'},
            {'id': 'FIJ001', 'name': 'Fiji Reefs', 'lat': -18.0, 'lon': 178.0, 'country': 'Fiji'},
            {'id': 'MEX001', 'name': 'Mesoamerican Reef', 'lat': 18.0, 'lon': -87.5, 'country': 'Mexico'}
        ]
        
        data = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        for reef in reefs:
            for date in pd.date_range(start_date, end_date):
                base_temp = 26.0
                seasonal_variation = 2.0 * np.sin(2 * np.pi * date.dayofyear / 365)
                random_variation = np.random.normal(0, 0.5)
                
                sst = base_temp + seasonal_variation + random_variation
                
                bleaching_threshold = 27.0
                if sst > bleaching_threshold:
                    dhw = (sst - bleaching_threshold) * 7
                else:
                    dhw = 0
                
                if dhw >= 8:
                    risk = 'High Risk'
                elif dhw >= 4:
                    risk = 'Moderate Risk'
                elif dhw >= 1:
                    risk = 'Low Risk'
                else:
                    risk = 'No Risk'
                
                data.append({
                    'reef_id': reef['id'],
                    'reef_name': reef['name'],
                    'latitude': reef['lat'],
                    'longitude': reef['lon'],
                    'country': reef['country'],
                    'date': date,
                    'sst_celsius': round(sst, 2),
                    'dhw_value': round(dhw, 2),
                    'bleaching_risk': risk,
                    'data_source': 'Simulated',
                    'created_at': datetime.now()
                })
        
        return pd.DataFrame(data)
    
    def store_data(self, data_df):
        """Store data in Neon database"""
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        data_to_insert = []
        for _, row in data_df.iterrows():
            data_to_insert.append((
                row['reef_id'],
                row['reef_name'],
                row['latitude'],
                row['longitude'],
                row['country'],
                row['date'],
                row['sst_celsius'],
                row['dhw_value'],
                row['bleaching_risk'],
                row['data_source'],
                row['created_at']
            ))
        
        execute_values(
            cursor,
            """
            INSERT INTO reef_data (
                reef_id, reef_name, latitude, longitude, country, date,
                sst_celsius, dhw_value, bleaching_risk, data_source, created_at
            ) VALUES %s
            ON CONFLICT (reef_id, date) DO UPDATE SET
                sst_celsius = EXCLUDED.sst_celsius,
                dhw_value = EXCLUDED.dhw_value,
                bleaching_risk = EXCLUDED.bleaching_risk
            """,
            data_to_insert
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Stored {len(data_df)} records in Neon database")
    
    def run_pipeline(self):
        """Run the complete pipeline"""
        print("🚀 Starting coral reef data pipeline...")
        
        # Create tables
        self.create_tables()
        
        # Generate data
        print("📊 Generating reef data...")
        data_df = self.generate_reef_data()
        
        # Store data
        print("💾 Storing data in cloud database...")
        self.store_data(data_df)
        
        print("✅ Pipeline completed successfully!")
        return data_df

if __name__ == "__main__":
    pipeline = CoralReefPipeline()
    data = pipeline.run_pipeline()
