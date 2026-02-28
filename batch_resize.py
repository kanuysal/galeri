import os
from PIL import Image

content_dir = 'content'
target_width = 440
target_height = 600

def process_images():
    count = 0
    for filename in os.listdir(content_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(content_dir, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    
                    # Target aspect ratio is 440/600 (0.733)
                    # Current aspect ratio is likely 440/788 (0.558)
                    
                    if width == target_width and height == target_height:
                        # Already correct size, just convert to webp if needed
                        pass
                    
                    # Calculate central crop box
                    left = (width - target_width) / 2
                    top = (height - target_height) / 2
                    right = (width + target_width) / 2
                    bottom = (height + target_height) / 2
                    
                    # Avoid cropping outside the image if it's smaller than target
                    left = max(0, left)
                    top = max(0, top)
                    right = min(width, right)
                    bottom = min(height, bottom)

                    cropped_img = img.crop((left, top, right, bottom))
                    
                    # Ensure exact target size (resize if the original was smaller than target)
                    if cropped_img.size != (target_width, target_height):
                        cropped_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        
                    # Save as WebP
                    new_filename = os.path.splitext(filename)[0] + '.webp'
                    new_filepath = os.path.join(content_dir, new_filename)
                    
                    cropped_img.save(new_filepath, 'WEBP', quality=85)
                    count += 1
                    
                    # Optional: Remove original to clean up space
                    # os.remove(filepath)
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    print(f"Successfully processed and converted {count} images to .webp ({target_width}x{target_height}).")

if __name__ == '__main__':
    process_images()
