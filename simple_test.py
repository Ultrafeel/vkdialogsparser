import os
import tempfile
from modules.posts import download_image, get_cached_image_path

# Test basic functionality
print("Testing image caching functions...")

# Test with a simple image URL
test_url = "https://httpbin.org/image/jpeg"

with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Temp dir: {temp_dir}")
    
    # Test download_image function
    result = download_image(test_url, temp_dir)
    print(f"Download result: {result}")
    
    # Test get_cached_image_path function
    cached_path, original_url = get_cached_image_path(test_url, temp_dir)
    print(f"Cached path: {cached_path}")
    print(f"Original URL: {original_url}")
    
    # List files in cache directory
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        print(f"Files in cache: {files}")

print("Test completed!")
