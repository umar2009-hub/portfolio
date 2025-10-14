import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    ADMIN_PIN = os.environ.get('ADMIN_PIN') or '1234'
    
    # Database URI: PostgreSQL for Render, SQLite for local
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render uses 'postgres://'; SQLAlchemy prefers 'postgresql://' for psycopg2
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
