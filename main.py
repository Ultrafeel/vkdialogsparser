#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VK Dialogs and Posts Parser
Enhanced version with community posts support and modern configuration system.
"""

import vk_api
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from modules.dialogs import DialogsManager
from modules.posts import PostsManager


def init_vk_session(token: str) -> vk_api.VkApi:
    """Initialize VK API session."""
    try:
        vk_session = vk_api.VkApi(token=token)
        # Test the connection
        vk_session.method('users.get')
        return vk_session
    except Exception as e:
        print(f"Ошибка при инициализации VK сессии: {e}")
        return None


def main():
    """Main function with enhanced functionality."""
    print("=== VK Dialogs and Posts Parser ===")
    print("Версия 2.0 - с поддержкой постов сообществ\n")
    
    try:
        # Load configuration
        print("Загрузка конфигурации...")
        config = Config()
        config.print_config_summary()
        
        # Initialize VK session
        print("Инициализация VK сессии...")
        vk_session = init_vk_session(config.vk_token)
        if not vk_session:
            print("❌ Не удалось инициализировать VK сессию. Проверьте токен.")
            return False
        
        print("✅ VK сессия успешно инициализирована\n")
        
        success = True
        
        # Process dialogs if requested
        if config.should_dump_dialogs():
            print("📱 Начинаем выгрузку диалогов...")
            dialogs_manager = DialogsManager(vk_session, config)
            if not dialogs_manager.dump_dialogs():
                success = False
        
        # Process posts if requested
        if config.should_dump_posts():
            print("📝 Начинаем выгрузку постов сообщества...")
            posts_manager = PostsManager(vk_session, config)
            if not posts_manager.dump_posts():
                success = False
        
        if success:
            print("\n🎉 Все операции завершены успешно!")
            print(f"Результаты сохранены в директории: {config.output_directory}")
        else:
            print("\n⚠️ Некоторые операции завершились с ошибками.")
        
        return success
        
    except KeyboardInterrupt:
        print("\n❌ Операция прервана пользователем.")
        return False
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        return False


if __name__ == "__main__":
    main()