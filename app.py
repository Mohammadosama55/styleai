from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
import uuid
from werkzeug.utils import secure_filename
from config import Config
from utils.recommender import FashionRecommender

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize recommender (fallback to demo mode if no API key)
try:
    recommender = FashionRecommender(app.config['GROQ_API_KEY'])
except Exception as e:
    print(f"Warning: Could not initialize Groq client: {e}")
    print("Running in demo mode without AI recommendations")
    recommender = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         genders=app.config['GENDERS'],
                         dress_codes=app.config['DRESS_CODES'])

@app.route('/quick-recommend', methods=['POST'])
def quick_recommend():
    """Get quick recommendations without image upload"""
    try:
        skin_tone = request.form.get('skin_tone')
        gender = request.form.get('gender')
        dress_code = request.form.get('dress_code')
        
        if recommender is None:
            # Demo mode response
            result = {
                "skin_analysis": {
                    "detected_tone": skin_tone,
                    "confidence": 0.85,
                    "color_palette": {
                        "primary": ["Navy Blue", "Burgundy", "Forest Green"],
                        "secondary": ["Soft Pink", "Lavender"],
                        "avoid": ["Neon Colors", "Bright Orange"]
                    }
                },
                "ai_recommendations": {
                    "outfit_recommendations": {
                        "tops": ["Classic white shirt", "Navy blue blouse"],
                        "bottoms": ["Dark jeans", "Black trousers"],
                        "shoes": ["Brown leather shoes", "Black heels"]
                    },
                    "fashion_tips": "Based on your skin tone, these colors will complement you beautifully."
                },
                "user_inputs": {
                    "gender": gender,
                    "dress_code": dress_code
                }
            }
            return render_template('results.html', result=result, quick_mode=True)
        
        # Validate inputs
        is_valid, message = recommender.validate_inputs(gender, dress_code)
        if not is_valid:
            flash(message, 'error')
            return redirect(url_for('index'))
        
        # Get recommendations
        result = recommender.get_quick_recommendations(skin_tone, gender, dress_code)
        
        return render_template('results.html', result=result, quick_mode=True)
        
    except Exception as e:
        flash(f"Error processing request: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
def analyze_image():
    """Analyze uploaded image and provide recommendations"""
    try:
        # Get form data
        gender = request.form.get('gender')
        dress_code = request.form.get('dress_code')
        preferences = request.form.get('preferences', '')
        
        # Check if image was uploaded
        if 'image' not in request.files:
            flash('No image selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['image']
        if file.filename == '':
            flash('No image selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            if recommender is None:
                # Demo mode response
                result = {
                    "skin_analysis": {
                        "detected_tone": "Medium",
                        "confidence": 0.82,
                        "color_palette": {
                            "primary": ["Royal Blue", "Crimson", "Forest Green"],
                            "secondary": ["Teal", "Coral"],
                            "avoid": ["Brown", "Muted Olive"]
                        }
                    },
                    "ai_recommendations": {
                        "outfit_recommendations": {
                            "tops": ["Classic white shirt", "Navy blue blouse", "Earth tone sweater"],
                            "bottoms": ["Dark jeans", "Beige trousers", "Black skirt"],
                            "shoes": ["Brown leather shoes", "Nude heels", "White sneakers"],
                            "dresses": ["A-line dress in complementary colors"],
                            "outerwear": ["Blazer in navy or black"]
                        },
                        "color_palette": {
                            "best_colors": ["Navy blue", "Burgundy", "Forest green", "Charcoal"],
                            "metal_tones": ["Gold accessories work well"],
                            "colors_to_avoid": ["Colors that clash with your undertone"]
                        }
                    },
                    "user_inputs": {
                        "gender": gender,
                        "dress_code": dress_code,
                        "preferences": preferences
                    },
                    "image_path": f"uploads/{filename}"
                }
                return render_template('results.html', result=result, quick_mode=False)
            
            try:
                # Validate inputs
                is_valid, message = recommender.validate_inputs(gender, dress_code)
                if not is_valid:
                    flash(message, 'error')
                    return redirect(url_for('index'))
                
                # Process image and get recommendations
                result = recommender.process_user_request(file_path, gender, dress_code, preferences)
                
                # Add image path for display
                result['image_path'] = f"uploads/{filename}"
                
                return render_template('results.html', result=result, quick_mode=False)
                
            except Exception as e:
                # Clean up uploaded file on error
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash(f"Error processing image: {str(e)}", 'error')
                return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f"Error processing request: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "StyleAI Fashion Recommender"
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    # Check if required environment variables are set
    if not app.config['GROQ_API_KEY']:
        print("WARNING: GROQ_API_KEY not set in environment variables!")
        print("Please set your Groq API key in the .env file")
    
    app.run(debug=True, host='0.0.0.0', port=5000)