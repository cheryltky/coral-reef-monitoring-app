import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('NEON_HOST'),
    'database': os.getenv('NEON_DATABASE'),
    'user': os.getenv('NEON_USER'),
    'password': os.getenv('NEON_PASSWORD'),
    'port': os.getenv('NEON_PORT', 5432),
    'sslmode': 'require'
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("✅ Successfully connected to Neon!")
    print(f"PostgreSQL version: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
