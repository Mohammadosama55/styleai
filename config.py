import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Skin tone categories
    SKIN_TONES = ['Fair', 'Medium', 'Olive', 'Deep']
    
    # Gender options
    GENDERS = ['Female', 'Male', 'Non-Binary']
    
    # Dress codes
    DRESS_CODES = ['Formal', 'Business', 'Casual', 'Party', 'Traditional']