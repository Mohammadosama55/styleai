from utils.image_processor import ImageProcessor
from utils.groq_client import GroqStylist
import os

class FashionRecommender:
    def __init__(self, groq_api_key):
        self.image_processor = ImageProcessor()
        self.groq_stylist = GroqStylist(groq_api_key)
    
    def process_user_request(self, image_path, gender, dress_code, preferences=""):
        """
        Main processing function that combines image analysis with AI recommendations
        """
        try:
            # Step 1: Analyze skin tone from image
            skin_tone, confidence, color_palette = self.image_processor.analyze_skin_tone(image_path)
            
            # Step 2: Convert image to base64 for API
            image_base64 = self.image_processor.get_image_base64(image_path)
            
            # Step 3: Get AI recommendations
            ai_recommendations = self.groq_stylist.analyze_image_and_recommend(
                image_base64, skin_tone, gender, dress_code, preferences
            )
            
            # Step 4: Combine all results
            result = {
                "skin_analysis": {
                    "detected_tone": skin_tone,
                    "confidence": confidence,
                    "color_palette": color_palette
                },
                "ai_recommendations": ai_recommendations,
                "user_inputs": {
                    "gender": gender,
                    "dress_code": dress_code,
                    "preferences": preferences
                }
            }
            
            return result
            
        except Exception as e:
            # Fallback processing without image analysis
            return self._fallback_processing(gender, dress_code, preferences)
    
    def _fallback_processing(self, gender, dress_code, preferences):
        """
        Fallback processing when image analysis fails
        """
        # Default skin tone analysis
        default_tone = "Medium"
        default_palette = self.image_processor._get_palette(default_tone)
        
        # Get basic recommendations from Groq
        basic_tips = self.groq_stylist.get_fashion_tips(default_tone, gender, dress_code)
        
        return {
            "skin_analysis": {
                "detected_tone": default_tone,
                "confidence": 0.7,
                "color_palette": default_palette,
                "note": "Using default analysis due to processing error"
            },
            "ai_recommendations": {
                "basic_tips": basic_tips,
                "outfit_recommendations": {
                    "tops": ["Classic white shirt", "Navy blue blouse"],
                    "bottoms": ["Dark jeans", "Black trousers"],
                    "shoes": ["Brown leather shoes", "Black heels"]
                }
            },
            "user_inputs": {
                "gender": gender,
                "dress_code": dress_code,
                "preferences": preferences
            },
            "error": "Image processing failed, using fallback recommendations"
        }
    
    def get_quick_recommendations(self, skin_tone, gender, dress_code):
        """
        Quick recommendations without image upload
        """
        try:
            tips = self.groq_stylist.get_fashion_tips(skin_tone, gender, dress_code)
            palette = self.image_processor._get_palette(skin_tone)
            
            return {
                "skin_tone": skin_tone,
                "color_palette": palette,
                "fashion_tips": tips,
                "quick_recommendations": {
                    "tops": ["Essential pieces for your skin tone"],
                    "bottoms": ["Versatile options"],
                    "accessories": ["Complementary accessories"]
                }
            }
        except Exception as e:
            return {
                "error": str(e),
                "skin_tone": skin_tone,
                "color_palette": self.image_processor._get_palette(skin_tone)
            }
    
    def validate_inputs(self, gender, dress_code):
        """
        Validate user inputs
        """
        from config import Config
        
        if gender not in Config.GENDERS:
            return False, f"Invalid gender. Choose from: {', '.join(Config.GENDERS)}"
        
        if dress_code not in Config.DRESS_CODES:
            return False, f"Invalid dress code. Choose from: {', '.join(Config.DRESS_CODES)}"
        
        return True, "Valid inputs"