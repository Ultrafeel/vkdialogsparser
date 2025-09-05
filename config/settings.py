import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional, List


class Config:
    """Configuration management class following tele-copy pattern."""
    
    def __init__(self):
        # Load environment variables
        load_dotenv(find_dotenv())
        
        # VK API Configuration
        self.vk_token = self._get_env_or_input("VK_TOKEN", "Введите VK токен: ", required=True)
        
        # Operation Mode
        self.dump_mode = self._get_env_or_input("DUMP_MODE", "Режим работы (dialogs/posts/both) [dialogs]: ", default="dialogs")
        self.export_format = self._get_env_or_input("EXPORT_FORMAT", "Формат экспорта (json/html/json,html) [json]: ", default="json")
        
        # Threading
        self.thread_count = int(self._get_env_or_input("THREAD_COUNT", "Количество потоков [4]: ", default="4"))
        
        # Output Configuration
        self.output_directory = self._get_env_or_input("OUTPUT_DIRECTORY", "Директория вывода [output]: ", default="output")
        self.dialogs_directory = self._get_env_or_input("DIALOGS_DIRECTORY", "Поддиректория для диалогов [dialogs]: ", default="dialogs")
        self.posts_directory = self._get_env_or_input("POSTS_DIRECTORY", "Поддиректория для постов [posts]: ", default="posts")
        
        # Community Posts Configuration
        if self.dump_mode in ["posts", "both"]:
            self.vk_community_id = self._get_env_or_input("VK_COMMUNITY_ID", "ID сообщества для выгрузки постов: ", required=True)
            self.posts_count = int(self._get_env_or_input("POSTS_COUNT", "Количество постов для выгрузки [100]: ", default="100"))
            self.include_comments = self._get_env_or_input("INCLUDE_COMMENTS", "Включить комментарии (true/false) [true]: ", default="true").lower() == "true"
            self.include_reactions = self._get_env_or_input("INCLUDE_REACTIONS", "Включить реакции (true/false) [true]: ", default="true").lower() == "true"
        else:
            self.vk_community_id = None
            self.posts_count = 100
            self.include_comments = True
            self.include_reactions = True
        
        # Dialog Configuration
        if self.dump_mode in ["dialogs", "both"]:
            self.max_dialogs = int(self._get_env_or_input("MAX_DIALOGS", "Максимальное количество диалогов [200]: ", default="200"))
        else:
            self.max_dialogs = 200
        
        # Validate configuration
        self._validate_config()
    
    def _get_env_or_input(self, env_var: str, prompt: str, default: Optional[str] = None, required: bool = False) -> str:
        """Get value from environment variable or prompt user input."""
        value = os.getenv(env_var)
        
        if value:
            return value
        
        if required and not default:
            while True:
                value = input(prompt).strip()
                if value:
                    return value
                print("Это поле обязательно для заполнения!")
        else:
            value = input(prompt).strip()
            return value if value else (default or "")
    
    def _validate_config(self):
        """Validate configuration values."""
        # Validate dump mode
        if self.dump_mode not in ["dialogs", "posts", "both"]:
            raise ValueError(f"Неверный режим работы: {self.dump_mode}. Допустимые значения: dialogs, posts, both")
        
        # Validate export format
        valid_formats = {"json", "html"}
        formats = [f.strip() for f in self.export_format.split(",")]
        for fmt in formats:
            if fmt not in valid_formats:
                raise ValueError(f"Неверный формат экспорта: {fmt}. Допустимые значения: json, html")
        
        # Validate thread count
        if self.thread_count < 1 or self.thread_count > 20:
            raise ValueError("Количество потоков должно быть от 1 до 20")
        
        # Validate community ID format if needed
        if self.vk_community_id:
            community_id = str(self.vk_community_id).strip()
            # Check if it's a valid numeric ID or domain name
            if not (community_id.lstrip('-').isdigit() or 
                   (community_id.replace('_', '').replace('.', '').isalnum() and len(community_id) > 0)):
                raise ValueError(f"Неверный формат ID сообщества: {self.vk_community_id}. Используйте числовой ID или доменное имя.")
    
    @property
    def export_formats(self) -> List[str]:
        """Get list of export formats."""
        return [f.strip() for f in self.export_format.split(",")]
    
    @property
    def full_dialogs_path(self) -> str:
        """Get full path for dialogs output."""
        return os.path.join(self.output_directory, self.dialogs_directory)
    
    @property
    def full_posts_path(self) -> str:
        """Get full path for posts output."""
        return os.path.join(self.output_directory, self.posts_directory)
    
    def should_dump_dialogs(self) -> bool:
        """Check if dialogs should be dumped."""
        return self.dump_mode in ["dialogs", "both"]
    
    def should_dump_posts(self) -> bool:
        """Check if posts should be dumped."""
        return self.dump_mode in ["posts", "both"]
    
    def print_config_summary(self):
        """Print configuration summary."""
        print("=== Конфигурация ===")
        print(f"Режим работы: {self.dump_mode}")
        print(f"Форматы экспорта: {self.export_format}")
        print(f"Количество потоков: {self.thread_count}")
        print(f"Директория вывода: {self.output_directory}")
        
        if self.should_dump_dialogs():
            print(f"Максимум диалогов: {self.max_dialogs}")
        
        if self.should_dump_posts():
            print(f"ID сообщества: {self.vk_community_id}")
            print(f"Количество постов: {self.posts_count}")
            print(f"Включить комментарии: {self.include_comments}")
            print(f"Включить реакции: {self.include_reactions}")
        
        print("==================\n")
