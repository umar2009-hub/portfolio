import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    ADMIN_PIN = os.environ.get('ADMIN_PIN') or '1234'

    DATABASE_URL = os.environ.get('DATABASE_URL', '').strip() or None

    if DATABASE_URL:
        # Normalize common forms to use psycopg3 driver
        # If Render gives "postgres://", convert to "postgresql+psycopg://"
        if DATABASE_URL.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
        elif DATABASE_URL.startswith('postgresql://'):
            SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)
        else:
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
