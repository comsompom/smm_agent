import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple


class NASAAPOD:
    """Handles NASA Astronomy Picture of the Day API requests"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov/planetary/apod"
    
    def get_apod_data(self) -> Optional[Dict]:
        """Fetch APOD data from NASA API"""
        try:
            params = {
                'api_key': self.api_key,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching APOD data: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing APOD JSON: {str(e)}")
            return None
    
    def download_image(self, image_url: str, filename: str = None) -> Optional[str]:
        """Download image from URL and save locally"""
        try:
            if not filename:
                # Extract filename from URL
                filename = image_url.split('/')[-1]
                if '?' in filename:
                    filename = filename.split('?')[0]
            
            # Create images directory if it doesn't exist
            os.makedirs('images', exist_ok=True)
            filepath = os.path.join('images', filename)
            
            # Download image
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Image downloaded: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error downloading image: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error saving image: {str(e)}")
            return None
    
    def format_apod_message(self, apod_data: Dict) -> str:
        """Format APOD data into a readable message"""
        title = apod_data.get('title', 'Unknown')
        explanation = apod_data.get('explanation', 'No explanation available')
        date = apod_data.get('date', 'Unknown date')
        copyright_info = apod_data.get('copyright', 'NASA')
        
        # Truncate explanation if too long
        max_explanation_length = 500
        if len(explanation) > max_explanation_length:
            explanation = explanation[:max_explanation_length] + "..."
        
        message = f"""🌌 NASA Astronomy Picture of the Day - {date}

📸 {title}

📝 {explanation}

📸 Credit: {copyright_info}

#NASA #APOD #Astronomy #Space #Science #Cosmos #Astrophotography #SpaceExploration"""
        
        return message
    
    def get_apod_content(self) -> Tuple[Optional[str], Optional[str]]:
        """Get APOD message and image filepath"""
        print("🔭 Fetching NASA APOD data...")
        
        apod_data = self.get_apod_data()
        if not apod_data:
            return None, None
        
        # Format message
        message = self.format_apod_message(apod_data)
        
        # Download image if available
        image_filepath = None
        if apod_data.get('media_type') == 'image':
            image_url = apod_data.get('hdurl') or apod_data.get('url')
            if image_url:
                image_filepath = self.download_image(image_url)
        
        return message, image_filepath
