#!/usr/bin/env python3
"""
Simple run script for the Artist Portfolio application
"""

import os
import sys
from app import app
from dotenv import load_dotenv
load_dotenv()
def main():
    """Main entry point for the application"""
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    ):
        print("⚠️  Warning: Virtual environment not detected!")
        print("It's recommended to run this in a virtual environment.")
        print("Run: python -m venv venv && source venv/bin/activate (or venv/Scripts/activate )")
        print()
    
    # Check if database is configured
    if 'postgresql' not in app.config['SQLALCHEMY_DATABASE_URI']:
        print("⚠️  Warning: Database not configured!")
        print("Please update your DATABASE_URL in the .env file")
        print()
    
    # Create uploads directory if it doesn't exist
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print(f"✅ Created uploads directory: {upload_dir}")
    
    print("🎨 Starting Artist Portfolio Application...")
    print("📍 Admin Panel: http://127.0.0.1:5000/admin")
    print("🔑 Default Login: admin / admin123")
    print("⚠️  Remember to change default password!")
    print()
    
    # Run the application
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )

if __name__ == '__main__':
    main()
