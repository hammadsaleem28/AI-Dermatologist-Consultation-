#!/usr/bin/env python3
"""
AI Dermatologist Application Launcher
"""

import os
import sys
from app import app
from config import Config

def check_requirements():
    """Check if all requirements are met"""
    
    # Check if templates directory exists
    if not os.path.exists('templates'):
        print("❌ Templates directory not found!")
        return False
    
    # Check if uploads directory exists
    if not os.path.exists('uploads'):
        print("📁 Creating uploads directory...")
        os.makedirs('uploads', exist_ok=True)
    
    # Check API key
    if Config.GEMINI_API_KEY == 'YOUR_GEMINI_API_KEY_HERE':
        print("⚠️  WARNING: Gemini API key not configured!")
        print("   Please update config.py with your actual API key")
        print("   Get your key from: https://aistudio.google.com/")
        return False
    
    return True

def main():
    """Main application launcher"""
    
    print("🏥 AI Dermatologist - Skin Disease Detection System")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Application cannot start. Please fix the issues above.")
        sys.exit(1)
    
    print("✅ All requirements met!")
    print("🚀 Starting Flask application...")
    print(f"🌐 Application will be available at: http://localhost:{Config.PORT}")
    print("=" * 60)
    print("\nFeatures available:")
    print("📸 Image Upload & Analysis")
    print("💬 AI Dermatologist Chat")
    print("💊 Pakistan Medicine Recommendations")
    print("🔍 Skin Disease Detection")
    print("\n" + "=" * 60)
    
    try:
        app.run(
            host=Config.HOST, 
            port=Config.PORT, 
            debug=Config.DEBUG
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 