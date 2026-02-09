import os
from groq import Groq
import json

class GroqStylist:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        # Using vision-capable model for image analysis
        self.vision_model = "llama-3.2-90b-vision-preview"
        self.text_model = "llama-3.3-70b-versatile"
    
    def analyze_image_and_recommend(self, image_base64, skin_tone, gender, dress_code, user_preferences=""):
        """
        Comprehensive fashion analysis using Groq's vision model
        """
        system_prompt = """You are an expert fashion stylist with deep knowledge of color theory, 
        body types, cultural fashion, and current trends. Provide detailed, actionable fashion advice."""
        
        user_prompt = f"""Analyze this person's photo and provide comprehensive fashion recommendations.
        
        Detected Skin Tone: {skin_tone}
        Gender Preference: {gender}
        Dress Code: {dress_code}
        Additional Preferences: {user_preferences}
        
        Provide a JSON response with the following structure:
        {{
            "skin_tone_analysis": {{
                "detected_tone": "{skin_tone}",
                "undertone": "warm/cool/neutral",
                "color_harmony_explanation": "detailed explanation"
            }},
            "outfit_recommendations": {{
                "tops": ["specific recommendations with colors and styles"],
                "bottoms": ["specific recommendations"],
                "shoes": ["specific recommendations"],
                "dresses": ["if applicable"],
                "outerwear": ["jackets/coats suggestions"]
            }},
            "color_palette": {{
                "best_colors": ["list of 5-7 colors"],
                "metal_tones": ["gold/silver/rose gold"],
                "colors_to_avoid": ["list"]
            }},
            "accessories": {{
                "jewelry": ["necklaces, earrings, etc."],
                "bags": ["style and color recommendations"],
                "watches": ["if applicable"],
                "other": ["scarves, belts, etc."]
            }},
            "hairstyle_suggestions": {{
                "recommended_styles": ["based on face shape"],
                "maintenance_tips": ["care instructions"],
                "color_recommendations": ["hair colors if applicable"]
            }},
            "makeup_tips": {{
                "foundation": ["undertone matching"],
                "lipstick": ["best shades"],
                "eyeshadow": ["complementary colors"]
            }},
            "shopping_links": {{
                "amazon_in": ["specific search terms for Amazon India"],
                "myntra": ["specific search terms for Myntra"],
                "ajio": ["specific search terms for Ajio"]
            }},
            "styling_tips": ["3-5 practical styling tips"],
            "confidence_boosters": ["how these choices enhance appearance"]
        }}
        
        Be specific, practical, and culturally relevant for Indian fashion context."""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                model=self.vision_model,
                temperature=0.7,
                max_tokens=2048
            )
            
            response_content = chat_completion.choices[0].message.content
            
            # Try to parse as JSON, if fails return raw response
            try:
                return json.loads(response_content)
            except json.JSONDecodeError:
                # If not valid JSON, create a structured response
                return {
                    "raw_response": response_content,
                    "skin_tone_analysis": {
                        "detected_tone": skin_tone,
                        "undertone": "neutral",
                        "color_harmony_explanation": "Based on detected skin tone"
                    },
                    "outfit_recommendations": {
                        "tops": ["Recommended tops based on analysis"],
                        "bottoms": ["Recommended bottoms based on analysis"],
                        "shoes": ["Footwear suggestions"],
                        "dresses": ["Dress recommendations if applicable"],
                        "outerwear": ["Jacket/coat suggestions"]
                    },
                    "color_palette": {
                        "best_colors": ["Colors that complement your skin tone"],
                        "metal_tones": ["Gold/Silver recommendations"],
                        "colors_to_avoid": ["Colors to avoid"]
                    }
                }
                
        except Exception as e:
            # Fallback response if API fails
            return {
                "error": str(e),
                "skin_tone_analysis": {
                    "detected_tone": skin_tone,
                    "undertone": "neutral",
                    "color_harmony_explanation": f"Based on {skin_tone} skin tone analysis"
                },
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
            }
    
    def get_fashion_tips(self, skin_tone, gender, dress_code):
        """
        Get fashion tips without image analysis (text-only model)
        """
        prompt = f"""Provide fashion recommendations for:
        Skin Tone: {skin_tone}
        Gender: {gender}
        Dress Code: {dress_code}
        
        Include color recommendations, outfit ideas, and styling tips."""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional fashion stylist."},
                    {"role": "user", "content": prompt}
                ],
                model=self.text_model,
                temperature=0.7,
                max_tokens=1024
            )
            
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Could not fetch fashion tips: {str(e)}"