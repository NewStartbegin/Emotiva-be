from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST (before anything else)
load_dotenv()

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    """
    Run Flask development server
    
    Untuk menjalankan:
    python run.py
    
    Server akan berjalan di http://localhost:5000
    """
    print("="*60)
    print("🚀 EMOTIVA-MATH Backend Server Starting...")
    print("="*60)
    print(f"📍 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔗 Server URL: http://localhost:5000")
    print(f"🏥 Health Check: http://localhost:5000/api/health")
    print(f"ℹ️  System Info: http://localhost:5000/api/info")
    print("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
