import json
import os
import vk_api
from time import time
from threading import Thread
from queue import Queue
from typing import Dict, List, Any, Optional


class DialogsManager:
    """Manages VK dialogs dumping functionality."""
    
    def __init__(self, vk_session: vk_api.VkApi, config):
        self.vk = vk_session
        self.vk_tools = vk_api.tools.VkTools(self.vk)
        self.config = config
    
    def handle_messages(self, q: Queue, directory: str = "users"):
        """Thread worker function to handle message processing."""
        while True:
            done = q.task_done
            dialog = q.get()

            messages = {
                "title": dialog["title"],
                "peer_id": dialog["peer_id"],
                "type": dialog.get("type", "unknown"),
                "messages": self.get_history(dialog["peer_id"])
            }

            self.save_dialog(messages, directory)
            done()
    
    def get_dialogs(self) -> List[Dict[str, Any]]:
        """Get list of all dialogs/conversations."""
        try:
            data = self.vk_tools.get_all(
                method="messages.getConversations",
                max_count=self.config.max_dialogs
            )['items']
            
            dialogs = []
            for peer in data:
                peer_id = peer["conversation"]["peer"]["id"]
                peer_type = peer["conversation"]["peer"]["type"]
                title = ""

                try:
                    if peer_type == "user":
                        user_data = self.vk.method("users.get", {"user_ids": peer_id})
                        title = f"{user_data[0]['first_name']}_{user_data[0]['last_name']}"
                    
                    elif peer_type == "group":
                        group_data = self.vk.method("groups.getById", {"group_ids": -peer_id})
                        title = group_data[0]["name"]
                    
                    elif peer_type == "chat":
                        chat_data = self.vk.method("messages.getConversationsById", {
                            "peer_ids": peer_id
                        })
                        title = chat_data['items'][0]['chat_settings']['title']
                    
                    dialogs.append({
                        "title": title,
                        "peer_id": peer_id,
                        "type": peer_type
                    })
                    
                except Exception as e:
                    print(f"Ошибка при получении информации о диалоге {peer_id}: {e}")
                    continue
            
            return dialogs
            
        except Exception as e:
            print(f"Ошибка при получении списка диалогов: {e}")
            return []

    def get_history(self, dialog_id: int) -> List[Dict[str, Any]]:
        """Get message history for a specific dialog."""
        try:
            history = self.vk_tools.get_all(
                method="messages.getHistory",
                max_count=200,
                values={"peer_id": dialog_id}
            )

            def format_message(message):
                return {
                    "message_id": message["id"],
                    "dialog_id": dialog_id,
                    "date": message.get("date"),
                    "from_id": message.get("from_id"),
                    "fwd_messages": message.get("fwd_messages", []),
                    "text": message.get("text", ""),
                    "attachments": message.get("attachments", []),
                    "reply_message": message.get("reply_message"),
                    "action": message.get("action")
                }

            start = time()
            messages = list(map(format_message, history['items']))
            end = time()
            print(f"Обработано {len(messages)} сообщений за {end-start:.2f} сек")
            return messages
            
        except Exception as e:
            print(f"Ошибка при получении истории диалога {dialog_id}: {e}")
            return []

    def save_dialog(self, dialog: Dict[str, Any], directory: str = "users"):
        """Save dialog to file."""
        directory = self._normalize_directory(directory)

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        print(f"Сохранение: {dialog['title']}")
        
        # Clean filename
        title = self._clean_filename(dialog["title"])
        
        # Save JSON
        if "json" in self.config.export_formats:
            json_path = os.path.join(directory, f"{title}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dialog, f, ensure_ascii=False, indent=2)
        
        # Save HTML if requested
        if "html" in self.config.export_formats:
            html_path = os.path.join(directory, f"{title}.html")
            self._save_dialog_html(dialog, html_path)

    def _save_dialog_html(self, dialog: Dict[str, Any], file_path: str):
        """Save dialog in HTML format."""
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Диалог: {dialog['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .dialog-header {{ background: #4a76a8; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .message {{ background: white; margin: 10px 0; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .message-header {{ font-weight: bold; color: #4a76a8; margin-bottom: 5px; }}
        .message-text {{ margin: 10px 0; }}
        .attachments {{ margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 4px; }}
        .attachment {{ margin: 5px 0; }}
        .forwarded {{ border-left: 3px solid #4a76a8; padding-left: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="dialog-header">
        <h1>{dialog['title']}</h1>
        <p>Тип: {dialog.get('type', 'unknown')} | ID: {dialog.get('peer_id')} | Сообщений: {len(dialog['messages'])}</p>
    </div>
    <div class="messages">
"""
        
        for msg in dialog['messages']:
            date_str = ""
            if msg.get('date'):
                import datetime
                date_str = datetime.datetime.fromtimestamp(msg['date']).strftime('%d.%m.%Y %H:%M:%S')
            
            html_content += f"""
        <div class="message">
            <div class="message-header">
                Сообщение #{msg['message_id']} от {msg.get('from_id', 'Unknown')} | {date_str}
            </div>
            <div class="message-text">{msg.get('text', '[Нет текста]')}</div>
"""
            
            if msg.get('attachments'):
                html_content += '<div class="attachments"><strong>Вложения:</strong><br>'
                for att in msg['attachments']:
                    att_type = att.get('type', 'unknown')
                    html_content += f'<div class="attachment">📎 {att_type}</div>'
                html_content += '</div>'
            
            if msg.get('fwd_messages'):
                html_content += '<div class="forwarded"><strong>Пересланные сообщения:</strong><br>'
                for fwd in msg['fwd_messages']:
                    html_content += f'<div>↳ {fwd.get("text", "[Нет текста]")}</div>'
                html_content += '</div>'
            
            html_content += '</div>'
        
        html_content += """
    </div>
</body>
</html>"""
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _normalize_directory(self, directory: str) -> str:
        """Normalize directory path."""
        if not directory:
            return ""
        return directory.strip("/\\")

    def _clean_filename(self, filename: str) -> str:
        """Clean filename from invalid characters."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename[:100]  # Limit length

    def dump_dialogs(self) -> bool:
        """Main function to dump all dialogs."""
        try:
            print("Получение списка диалогов...")
            dialogs = self.get_dialogs()
            
            if not dialogs:
                print("Диалоги не найдены или произошла ошибка.")
                return False
            
            print(f"Найдено {len(dialogs)} диалогов")
            
            # Preview first few dialogs
            print("Первые несколько диалогов для выгрузки:")
            for dialog in dialogs[:min(3, len(dialogs))]:
                print(f"- {dialog['title']} (ID: {dialog['peer_id']}, Тип: {dialog['type']})")
            
            # Confirm before proceeding
            confirm = input(f"\nПродолжить выгрузку {len(dialogs)} диалогов? (y/N): ").lower() == 'y'
            if not confirm:
                print("Операция отменена.")
                return False
            
            # Create output directory
            output_dir = self.config.full_dialogs_path
            os.makedirs(output_dir, exist_ok=True)
            
            # Setup threading
            queue = Queue()
            
            for _ in range(self.config.thread_count):
                t = Thread(target=self.handle_messages, args=(queue, output_dir))
                t.daemon = True
                t.start()
            
            # Add dialogs to queue
            for dialog in dialogs:
                queue.put(dialog)
            
            # Wait for completion
            queue.join()
            
            print(f"\n✅ Выгрузка диалогов завершена! Файлы сохранены в: {output_dir}")
            return True
            
        except Exception as e:
            print(f"Ошибка при выгрузке диалогов: {e}")
            return False
