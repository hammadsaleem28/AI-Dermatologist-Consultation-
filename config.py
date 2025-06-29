import os

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCZmExgSWzr02JEPNitfhkT2uVa0X_-yXM')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Application Settings
    HOST = '0.0.0.0'
    PORT = 5000

# Instructions for setting up Gemini API Key:
"""
To get your Gemini API Key:
1. Go to https://aistudio.google.com/
2. Click on "Get API Key"
3. Create a new project or select existing one
4. Generate an API key
5. Replace 'YOUR_GEMINI_API_KEY_HERE' in this file with your actual key

OR set as environment variable:
export GEMINI_API_KEY=your_actual_api_key_here
""" 