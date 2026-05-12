import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    
    # Webhook settings
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    
    # Data storage
    DATA_DIR = 'data'
    REMINDERS_FILE = os.path.join(DATA_DIR, 'reminders.json')
    
    # Scheduler
    SCHEDULER_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'

config = Config()
