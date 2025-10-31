"""
WSGI entry point for production deployment with Gunicorn
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create application instance
app = create_app('production')

if __name__ == '__main__':
    app.run()
