#!/usr/bin/env python3
"""
Script to update all txt files with new cloud URLs
"""

import os
from pathlib import Path

# Configuration
MODELS_DIR = "models"
IMAGES_DIR = "downloaded_imgs"
BASE_URL = "https://gemini-drive.hellaskraken.workers.dev/0:/SlideShow"

def update_txt_files():
    """Update all txt files with new cloud URLs"""
    
    models_path = Path(MODELS_DIR)
    images_path = Path(IMAGES_DIR)
    
    if not models_path.exists():
        print("❌ Models directory not found.")
        return
    
    if not images_path.exists():
        print("❌ Images directory not found.")
        return
    
    # Get all txt files
    txt_files = list(models_path.glob("*.txt"))
    print(f"Found {len(txt_files)} txt files to update")
    
    for txt_file in txt_files:
        model_name = txt_file.stem  # filename without extension
        model_images_dir = images_path / model_name
        
        if not model_images_dir.exists():
            print(f"⚠️ Skipping {model_name} - no image folder found")
            continue
        
        # Get all jpg files in the model's directory
        image_files = sorted([f for f in model_images_dir.iterdir() 
                            if f.is_file() and f.suffix.lower() == '.jpg'])
        
        if not image_files:
            print(f"⚠️ Skipping {model_name} - no images found")
            continue
        
        print(f"🔧 Updating {model_name}.txt with {len(image_files)} URLs")
        
        # Generate new URLs
        new_urls = []
        for image_file in image_files:
            # Create URL: BASE_URL/model_name/image_filename
            url = f"{BASE_URL}/{model_name}/{image_file.name}"
            new_urls.append(url)
        
        # Write new URLs to txt file
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                for url in new_urls:
                    f.write(url + '\n')
            
            print(f"✅ Updated {txt_file.name} with {len(new_urls)} URLs")
            
        except Exception as e:
            print(f"❌ Error updating {txt_file.name}: {e}")
    
    print("\n🎉 Finished updating all txt files!")

if __name__ == "__main__":
    update_txt_files()
