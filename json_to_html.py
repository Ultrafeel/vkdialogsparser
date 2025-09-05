#!/usr/bin/env python3
"""
Script to convert saved VK posts JSON to HTML format.
Loads a JSON file with posts data and generates an HTML file using the same formatting as the main posts module.
"""

import json
import os
import sys
from modules.posts import save_posts_html


def main():
    """Main function to convert JSON to HTML."""
    # Get JSON file path from command line argument or user input
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
    else:
        json_file_path = input("Введите путь к JSON файлу с постами: ").strip()
    
    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"Ошибка: Файл {json_file_path} не найден!")
        return False
    
    # Load JSON data
    try:
        print(f"Загрузка данных из {json_file_path}...")
        with open(json_file_path, "r", encoding="utf-8") as f:
            posts_data = json.load(f)
        print(f"Загружено постов: {posts_data.get('posts_count', len(posts_data.get('posts', [])))}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return False
    
    # Validate JSON structure
    if not isinstance(posts_data, dict):
        print("Ошибка: JSON должен содержать объект с данными постов")
        return False
    
    if "community" not in posts_data or "posts" not in posts_data:
        print("Ошибка: JSON должен содержать поля 'community' и 'posts'")
        return False
    
    # Generate HTML file path
    json_dir = os.path.dirname(json_file_path)
    json_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    html_file_path = os.path.join(json_dir, f"{json_filename}.html")
    
    # Generate HTML
    try:
        print(f"Генерация HTML файла...")
        save_posts_html(posts_data, html_file_path)
        print(f"HTML сохранен: {html_file_path}")
        return True
    except Exception as e:
        print(f"Ошибка при генерации HTML: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\nГотово! HTML файл успешно создан.")
