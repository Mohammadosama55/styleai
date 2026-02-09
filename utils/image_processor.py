from PIL import Image
import io
import base64
import random

class ImageProcessor:
    def __init__(self):
        # Simple initialization without OpenCV dependencies
        pass
    
    def detect_face(self, image_path):
        """Simple face detection simulation (returns full image)"""
        try:
            img = Image.open(image_path)
            return img, img
        except Exception:
            raise ValueError("Could not load image")
    
    def analyze_skin_tone(self, image_path):
        """
        Simulated skin tone detection (random for demo purposes)
        Returns: skin_tone_category, confidence, color_palette
        """
        # For demo purposes, return random skin tone
        skin_tones = ["Fair", "Medium", "Olive", "Deep"]
        skin_tone = random.choice(skin_tones)
        confidence = round(random.uniform(0.7, 0.95), 2)
        palette = self._get_palette(skin_tone)
        
        return skin_tone, confidence, palette
    
    # Removed OpenCV-dependent methods for compatibility
    
    def _get_palette(self, skin_tone):
        """Get recommended color palette for skin tone"""
        palettes = {
            "Fair": {
                "primary": ["Navy Blue", "Emerald Green", "Burgundy", "Charcoal"],
                "secondary": ["Soft Pink", "Lavender", "Mint Green", "Peach"],
                "accent": ["Gold", "Coral", "Turquoise"],
                "avoid": ["Neon Yellow", "Orange", "Beige (too close to skin)"]
            },
            "Medium": {
                "primary": ["Royal Blue", "Crimson", "Forest Green", "Plum"],
                "secondary": ["Teal", "Coral", "Lemon Yellow", "Magenta"],
                "accent": ["Silver", "Bronze", "Fuchsia"],
                "avoid": ["Brown (too close to skin)", "Muted Olive"]
            },
            "Olive": {
                "primary": ["Cream", "Rust", "Deep Purple", "Terracotta"],
                "secondary": ["Peach", "Soft White", "Dusty Rose", "Khaki"],
                "accent": ["Gold", "Copper", "Mint"],
                "avoid": ["Green (too similar to undertone)", "Yellow-green"]
            },
            "Deep": {
                "primary": ["Pure White", "Bright Orange", "Hot Pink", "Electric Blue"],
                "secondary": ["Lime Green", "Red", "Yellow", "Cobalt"],
                "accent": ["Gold", "Bronze", "Neon shades"],
                "avoid": ["Brown", "Navy (too dark)", "Muted tones"]
            }
        }
        return palettes.get(skin_tone, palettes["Medium"])
    
    def get_image_base64(self, image_path):
        """Convert image to base64 for API transmission"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')