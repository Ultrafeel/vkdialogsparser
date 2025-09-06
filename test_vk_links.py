#!/usr/bin/env python3
"""
Test script for VK link parsing functionality.
Tests the parse_vk_links function with various VK-style link formats.
"""

import sys
import os

# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from posts import parse_vk_links

def test_vk_link_parsing():
    """Test VK link parsing with various formats."""
    
    test_cases = [
        {
            'input': 'Проверьте эту статью: [#alias|www.example.com/russian/ve...|https://www.example.com/russian/vert-cap-40793289]',
            'expected_contains': '<a href="https://www.example.com/russian/vert-cap-40793289" target="_blank">www.example.com/russian/ve...</a>'
        },
        {
            'input': 'Несколько ссылок: [#alias|Первая ссылка|https://example1.com] и [#alias|Вторая ссылка|https://example2.com]',
            'expected_contains': ['<a href="https://example1.com" target="_blank">Первая ссылка</a>', 
                                '<a href="https://example2.com" target="_blank">Вторая ссылка</a>']
        },
        {
            'input': 'Текст без ссылок',
            'expected': 'Текст без ссылок'
        },
        {
            'input': 'Ссылка с HTML символами: [#alias|<script>alert("test")</script>|https://safe-link.com]',
            'expected_contains': '<a href="https://safe-link.com" target="_blank">&lt;script&gt;alert(&quot;test&quot;)&lt;/script&gt;</a>'
        },
        {
            'input': 'Неправильный формат: [#wrong|текст|url] не должен обрабатываться',
            'expected': 'Неправильный формат: [#wrong|текст|url] не должен обрабатываться'
        },
        {
            'input': '',
            'expected': ''
        },
        {
            'input': None,
            'expected': None
        }
    ]
    
    print("🔗 Тестирование парсинга VK ссылок\n")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Тест {i}:")
        print(f"  Входной текст: {repr(test_case['input'])}")
        
        try:
            result = parse_vk_links(test_case['input'])
            print(f"  Результат: {repr(result)}")
            
            # Check expected result
            if 'expected' in test_case:
                if result == test_case['expected']:
                    print("  ✅ ПРОЙДЕН")
                else:
                    print(f"  ❌ ПРОВАЛЕН - ожидалось: {repr(test_case['expected'])}")
                    all_passed = False
            elif 'expected_contains' in test_case:
                expected_items = test_case['expected_contains']
                if isinstance(expected_items, str):
                    expected_items = [expected_items]
                
                success = True
                for expected_item in expected_items:
                    if expected_item not in result:
                        print(f"  ❌ ПРОВАЛЕН - не найдено: {repr(expected_item)}")
                        success = False
                        all_passed = False
                
                if success:
                    print("  ✅ ПРОЙДЕН")
            
        except Exception as e:
            print(f"  ❌ ОШИБКА: {e}")
            all_passed = False
        
        print()
    
    if all_passed:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("⚠️ Некоторые тесты провалены.")
    
    return all_passed

def test_html_generation():
    """Test HTML generation with VK links."""
    
    print("🌐 Тестирование генерации HTML с VK ссылками\n")
    
    # Sample post data with VK links
    sample_post = {
        'id': 12345,
        'text': 'Интересная статья: [#alias|example Russian|https://www.example.com/russian/vert-cap-40793289]\n\nА также: [#alias|Технологии|https://example.com/tech]',
        'date': 1640995200,  # 2022-01-01 00:00:00
        'date_formatted': '01.01.2022 00:00:00',
        'vk_link': 'https://vk.com/wall-123_12345',
        'attachments': [],
        'likes': {'count': 10},
        'reposts': {'count': 5},
        'comments': [],
        'views': {'count': 100}
    }
    
    # Test the text processing logic
    from posts import html
    
    post_text = sample_post.get('text', '').strip()
    if post_text:
        # Apply the same processing as in save_posts_html
        processed_text = html.escape(post_text)
        processed_text = parse_vk_links(processed_text)
        processed_text = processed_text.replace('\n', '<br>')
        
        print("Исходный текст:")
        print(f"  {repr(sample_post['text'])}")
        print()
        print("Обработанный HTML:")
        print(f"  {processed_text}")
        print()
        
        # Check if links are properly converted
        if '<a href="https://www.example.com/russian/vert-cap-40793289" target="_blank">example Russian</a>' in processed_text:
            print("✅ Первая ссылка обработана корректно")
        else:
            print("❌ Первая ссылка обработана некорректно")
        
        if '<a href="https://example.com/tech" target="_blank">Технологии</a>' in processed_text:
            print("✅ Вторая ссылка обработана корректно")
        else:
            print("❌ Вторая ссылка обработана некорректно")
        
        if '<br>' in processed_text:
            print("✅ Переносы строк обработаны корректно")
        else:
            print("❌ Переносы строк обработаны некорректно")

if __name__ == '__main__':
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ФУНКЦИОНАЛЬНОСТИ ПАРСИНГА VK ССЫЛОК")
    print("=" * 60)
    print()
    
    # Test the parsing function
    parsing_success = test_vk_link_parsing()
    
    print("-" * 60)
    
    # Test HTML generation
    test_html_generation()
    
    print()
    print("=" * 60)
    if parsing_success:
        print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО")
    else:
        print("⚠️ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО С ОШИБКАМИ")
    print("=" * 60)
