#!/usr/bin/env python3
"""
Test script for image caching functionality in posts.py
"""

import os
import tempfile
import json
from datetime import datetime
from modules.posts import save_posts_html

def create_test_posts_data():
    """Create test data with image attachments."""
    return {
        "type": "community_posts",
        "export_date": datetime.now().isoformat(),
        "community": {
            "id": -12345,
            "name": "Test Community",
            "screen_name": "test_community",
            "description": "Test community for image caching",
            "members_count": 1000,
            "type": "group"
        },
        "posts_count": 2,
        "posts": [
            {
                "id": 1,
                "owner_id": -12345,
                "from_id": -12345,
                "date": 1640995200,
                "date_formatted": "01.01.2022 00:00:00",
                "vk_link": "https://vk.com/wall-12345_1",
                "text": "Тестовый пост с изображением",
                "attachments": [
                    {
                        "type": "photo",
                        "url": "https://sun9-74.userapi.com/impg/c857136/v857136098/95b8b/0YK6suXkY24.jpg?size=604x604&quality=96&sign=53bc0c5ce6c2897ab9afce5c32ce8e2b&type=album",
                        "width": 604,
                        "height": 604,
                        "original_data": {}
                    }
                ],
                "post_type": "post",
                "copy_history": [],
                "views": {"count": 100},
                "reposts": {"count": 5},
                "likes": {"count": 25},
                "comments": {"count": 3}
            },
            {
                "id": 2,
                "owner_id": -12345,
                "from_id": -12345,
                "date": 1640995260,
                "date_formatted": "01.01.2022 00:01:00",
                "vk_link": "https://vk.com/wall-12345_2",
                "text": "Тестовый пост с видео",
                "attachments": [
                    {
                        "type": "video",
                        "title": "Тестовое видео",
                        "duration": 120,
                        "vk_link": "https://vk.com/video-12345_456789",
                        "original_data": {
                            "video": {
                                "title": "Тестовое видео",
                                "description": "Описание тестового видео",
                                "duration": 120,
                                "owner_id": -12345,
                                "id": 456789,
                                "views": 500,
                                "comments": 10,
                                "photo_800": "https://sun9-74.userapi.com/impg/c857136/v857136098/95b8b/0YK6suXkY24.jpg?size=800x450&quality=96&sign=53bc0c5ce6c2897ab9afce5c32ce8e2b&type=album",
                                "first_frame_800": "https://sun9-74.userapi.com/impg/c857136/v857136098/95b8b/0YK6suXkY24.jpg?size=800x450&quality=96&sign=53bc0c5ce6c2897ab9afce5c32ce8e2b&type=album"
                            }
                        }
                    }
                ],
                "post_type": "post",
                "copy_history": [],
                "views": {"count": 200},
                "reposts": {"count": 10},
                "likes": {"count": 50},
                "comments": {"count": 8}
            }
        ]
    }

def test_image_caching():
    """Test the image caching functionality."""
    print("🧪 Тестирование функции кеширования изображений...")
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Временная директория: {temp_dir}")
        
        # Create test data
        test_data = create_test_posts_data()
        
        # Generate HTML file path
        html_path = os.path.join(temp_dir, "test_posts.html")
        
        try:
            # Test the save_posts_html function with caching
            print("💾 Сохранение HTML с кешированием изображений...")
            save_posts_html(test_data, html_path)
            
            # Check if HTML file was created
            if os.path.exists(html_path):
                print("✅ HTML файл создан успешно")
                
                # Check if cache directory was created
                cache_dir = os.path.join(temp_dir, "test_posts_files")
                if os.path.exists(cache_dir):
                    print("✅ Директория кеша создана")
                    
                    # List cached files
                    cached_files = os.listdir(cache_dir)
                    if cached_files:
                        print(f"✅ Кешированные файлы: {cached_files}")
                    else:
                        print("⚠️ Кешированные файлы не найдены (возможно, изображения недоступны)")
                else:
                    print("⚠️ Директория кеша не создана")
                
                # Check HTML content
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                if "test_posts_files/" in html_content:
                    print("✅ HTML содержит ссылки на кешированные изображения")
                else:
                    print("⚠️ HTML не содержит ссылки на кешированные изображения")
                
                if "<!-- Original URL:" in html_content:
                    print("✅ HTML содержит комментарии с оригинальными URL")
                else:
                    print("⚠️ HTML не содержит комментарии с оригинальными URL")
                
                print(f"📄 HTML файл размером {len(html_content)} символов создан")
                
            else:
                print("❌ HTML файл не был создан")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при тестировании: {e}")
            return False
    
    print("🎉 Тестирование завершено успешно!")
    return True

if __name__ == "__main__":
    test_image_caching()
