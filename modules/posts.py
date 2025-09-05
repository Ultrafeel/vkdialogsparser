import json
import os
import vk_api
import html
from time import time
from datetime import datetime
from typing import Dict, List, Any, Optional


def save_posts_html(posts_data: Dict[str, Any], file_path: str):
    """Save posts in HTML format."""
    community = posts_data["community"]
    posts = posts_data["posts"]
    
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Посты: {community['name']}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f7f8fa; 
            line-height: 1.4;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ 
            background: linear-gradient(135deg, #4a76a8, #5a8bb8); 
            color: white; 
            padding: 30px; 
            border-radius: 12px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .header h1 {{ margin: 0 0 10px 0; font-size: 28px; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .post {{ 
            background: white; 
            margin: 20px 0; 
            padding: 25px; 
            border-radius: 12px; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e1e5eb;
        }}
        .post-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 15px; 
            padding-bottom: 15px; 
            border-bottom: 1px solid #f0f2f5;
        }}
        .post-id {{ font-weight: bold; color: #4a76a8; font-size: 16px; }}
        .post-date {{ color: #656d78; font-size: 14px; }}
        .post-date a {{ color: #4a76a8; text-decoration: none; }}
        .post-date a:hover {{ text-decoration: underline; }}
        .post-text {{ 
            margin: 15px 0; 
            font-size: 16px; 
            line-height: 1.5; 
            white-space: pre-wrap;
        }}
        .attachments {{ 
            margin: 15px 0; 
            padding: 15px; 
            background: #f8f9fa; 
            border-radius: 8px; 
            border-left: 4px solid #4a76a8;
        }}
        .attachment {{ 
            margin: 8px 0; 
            padding: 8px 12px; 
            background: white; 
            border-radius: 6px; 
            border: 1px solid #e1e5eb;
        }}
        .stats {{ 
            display: flex; 
            gap: 20px; 
            margin-top: 15px; 
            padding-top: 15px; 
            border-top: 1px solid #f0f2f5; 
            font-size: 14px; 
            color: #656d78;
        }}
        .stat {{ display: flex; align-items: center; gap: 5px; }}
        .comments {{ 
            margin-top: 20px; 
            padding: 15px; 
            background: #f8f9fa; 
            border-radius: 8px;
        }}
        .comment {{ 
            margin: 10px 0; 
            padding: 12px; 
            background: white; 
            border-radius: 6px; 
            border-left: 3px solid #4a76a8;
        }}
        .comment-header {{ 
            font-weight: bold; 
            color: #4a76a8; 
            margin-bottom: 5px; 
            font-size: 14px;
        }}
        .comment-header a {{ color: #4a76a8; text-decoration: none; }}
        .comment-header a:hover {{ text-decoration: underline; }}
        .copy-history {{ 
            margin: 15px 0; 
            padding: 15px; 
            background: #f0f8ff; 
            border-radius: 8px;
            border-left: 4px solid #4a76a8;
        }}
        .original-post {{ 
            margin: 10px 0; 
            padding: 12px; 
            background: white; 
            border-radius: 6px; 
            border: 1px solid #e1e5eb;
        }}
        .original-header {{ 
            font-weight: bold; 
            color: #4a76a8; 
            margin-bottom: 8px; 
            font-size: 14px;
        }}
        .original-header a {{ color: #4a76a8; text-decoration: none; }}
        .original-header a:hover {{ text-decoration: underline; }}
        .original-text {{ font-size: 14px; line-height: 1.4; }}
        .attachment a {{ color: #4a76a8; text-decoration: none; }}
        .attachment a:hover {{ text-decoration: underline; }}
        .comment-text {{ font-size: 14px; line-height: 1.4; }}
        .no-content {{ color: #656d78; font-style: italic; }}
        .search-box {{ 
            margin-bottom: 20px; 
            padding: 12px; 
            border: 2px solid #e1e5eb; 
            border-radius: 8px; 
            font-size: 16px; 
            width: 100%; 
            box-sizing: border-box;
        }}
    </style>
    <script>
        function searchPosts() {{
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const posts = document.querySelectorAll('.post');
            
            posts.forEach(post => {{
                const text = post.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    post.style.display = 'block';
                }} else {{
                    post.style.display = 'none';
                }}
            }});
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{community['name']}</h1>
            <p><strong>ID:</strong> {community['id']} | <strong>Тип:</strong> {community.get('type', 'group')}</p>
            <p><strong>Участников:</strong> {community.get('members_count', 'N/A')} | <strong>Постов:</strong> {len(posts)}</p>
            <p><strong>Дата экспорта:</strong> {posts_data['export_date'][:19].replace('T', ' ')}</p>
            {f'<p><strong>Описание:</strong> {community.get("description", "")[:200]}{"..." if len(community.get("description", "")) > 200 else ""}</p>' if community.get('description') else ''}
        </div>
        
        <input type="text" id="searchBox" class="search-box" placeholder="Поиск по постам..." onkeyup="searchPosts()">
        
        <div class="posts">
"""
    
    for post in posts:
        post_text = post.get('text', '').strip()
        if not post_text:
            post_text = '<span class="no-content">[Нет текста]</span>'
        else:
            post_text = html.escape(post_text).replace('\n', '<br>')
        
        html_content += f"""
        <div class="post">
            <div class="post-header">
                <div class="post-id">Пост #{post['id']}</div>
                <div class="post-date"><a href="{post['vk_link']}" target="_blank" title="Открыть оригинал в VK">{post['date_formatted']}</a></div>
            </div>
            <div class="post-text">{post_text}</div>
"""
        
        # Attachments
        if post.get('attachments'):
            html_content += '<div class="attachments"><strong>📎 Вложения:</strong>'
            for att in post['attachments']:
                att_type = att.get('type', 'unknown')
                att_info = ""
                att_link = ""
                
                if att_type == 'photo':
                    att_info = f" ({att.get('width', 0)}x{att.get('height', 0)})"
                    if att.get('url'):
                        att_link = f'<a href="{att["url"]}" target="_blank">🖼️ Фото{att_info}</a>'
                    else:
                        att_link = f'🖼️ Фото{att_info}'
                elif att_type == 'video':
                    att_info = f" - {att.get('title', 'Без названия')}"
                    if att.get('vk_link'):
                        att_link = f'<a href="{att["vk_link"]}" target="_blank">🎬 Видео{att_info}</a>'
                    else:
                        att_link = f'🎬 Видео{att_info}'
                elif att_type == 'doc':
                    att_info = f" - {att.get('title', 'Без названия')}"
                    if att.get('url'):
                        att_link = f'<a href="{att["url"]}" target="_blank">📄 Документ{att_info}</a>'
                    else:
                        att_link = f'📄 Документ{att_info}'
                elif att_type == 'audio':
                    artist = att.get('artist', '')
                    title = att.get('title', 'Аудио')
                    att_link = f'🎵 {artist} - {title}' if artist else f'🎵 {title}'
                elif att_type == 'link':
                    if att.get('url'):
                        att_link = f'<a href="{att["url"]}" target="_blank">🔗 {att.get("title", "Ссылка")}</a>'
                    else:
                        att_link = f'🔗 {att.get("title", "Ссылка")}'
                else:
                    att_link = f'📎 {att_type.upper()}'
                
                html_content += f'<div class="attachment">{att_link}</div>'
            html_content += '</div>'
        
        # Stats
        likes_count = post.get('likes', {}).get('count', 0)
        reposts_count = post.get('reposts', {}).get('count', 0)
        comments_count = len(post.get('comments', [])) if isinstance(post.get('comments'), list) else post.get('comments', {}).get('count', 0)
        views_count = post.get('views', {}).get('count', 0)
        
        html_content += f"""
            <div class="stats">
                <div class="stat">❤️ {likes_count}</div>
                <div class="stat">🔄 {reposts_count}</div>
                <div class="stat">💬 {comments_count}</div>
                <div class="stat">👁️ {views_count}</div>
            </div>
"""
        
        # Copy history (reposts)
        if post.get('copy_history'):
            html_content += '<div class="copy-history"><strong>🔄 Репост оригинала:</strong>'
            for original in post['copy_history']:
                original_text = original.get('text', '').strip()
                if not original_text:
                    original_text = '<span class="no-content">[Нет текста]</span>'
                else:
                    original_text = html.escape(original_text).replace('\n', '<br>')
                
                html_content += f'''
                <div class="original-post">
                    <div class="original-header">
                        <a href="{original['vk_link']}" target="_blank" title="Открыть оригинал в VK">Оригинал от {original['date_formatted']}</a>
                    </div>
                    <div class="original-text">{original_text}</div>
                </div>
                '''
            html_content += '</div>'
        
        # Comments
        if post.get('comments') and isinstance(post['comments'], list) and post['comments']:
            html_content += '<div class="comments"><strong>💬 Комментарии:</strong>'
            for comment in post['comments'][:10]:  # Show first 10 comments
                comment_text = comment.get('text', '').strip()
                if not comment_text:
                    comment_text = '<span class="no-content">[Нет текста]</span>'
                else:
                    comment_text = html.escape(comment_text).replace('\n', '<br>')
                
                html_content += f"""
                <div class="comment">
                    <div class="comment-header">
                        <a href="{comment['vk_link']}" target="_blank" title="Открыть комментарий в VK">Пользователь {comment.get('from_id', 'Unknown')} | {comment['date_formatted']}</a>
                    </div>
                    <div class="comment-text">{comment_text}</div>
                </div>
"""
            
            if len(post['comments']) > 10:
                html_content += f'<div class="no-content">... и ещё {len(post["comments"]) - 10} комментариев</div>'
            
            html_content += '</div>'
        
        html_content += '</div>'
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


class PostsManager:
    """Manages VK community posts dumping functionality."""
    
    def __init__(self, vk_session: vk_api.VkApi, config):
        self.vk = vk_session
        self.vk_tools = vk_api.tools.VkTools(self.vk)
        self.config = config
    
    def get_community_info(self, community_id: str) -> Optional[Dict[str, Any]]:
        """Get community information."""
        try:
            # Support both numeric IDs and domain names
            if community_id.lstrip('-').isdigit():
                # Numeric ID
                clean_id = str(community_id).lstrip('-')
                community_data = self.vk.method("groups.getById", {
                    "group_ids": clean_id,
                    "fields": "description,members_count,activity"
                })
            else:
                # Domain name
                community_data = self.vk.method("groups.getById", {
                    "group_ids": community_id,
                    "fields": "description,members_count,activity"
                })
            
            if community_data:
                info = community_data[0]
                return {
                    "id": -int(info.get("id")),  # VK uses negative IDs for communities
                    "name": info.get("name", ""),
                    "screen_name": info.get("screen_name", ""),
                    "description": info.get("description", ""),
                    "members_count": info.get("members_count", 0),
                    "activity": info.get("activity", ""),
                    "type": info.get("type", "group")
                }
            return None
            
        except Exception as e:
            print(f"Ошибка при получении информации о сообществе {community_id}: {e}")
            return None
    
    def get_community_posts(self, community_id: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get posts from community wall."""
        try:
            POSTS_PER_REQUEST = 100  # VK API limit
            all_posts = []
            offset = 0
            owner_id = None
            
            print(f"Запрашиваем {count} постов (по {POSTS_PER_REQUEST} за раз)...")
            
            while len(all_posts) < count:
                # Calculate how many posts to request in this iteration
                posts_to_request = min(POSTS_PER_REQUEST, count - len(all_posts))
                
                # Determine if community_id is numeric ID or domain name
                if community_id.lstrip('-').isdigit():
                    # Numeric ID - use owner_id parameter
                    clean_id = str(community_id).lstrip('-')
                    owner_id = -int(clean_id)
                    posts_data = self.vk.method("wall.get", {
                        "owner_id": owner_id,
                        "count": posts_to_request,
                        "offset": offset,
                        "extended": 1,
                        "filter": "all"
                    })
                else:
                    # Domain name - use domain parameter
                    posts_data = self.vk.method("wall.get", {
                        "domain": community_id,
                        "count": posts_to_request,
                        "offset": offset,
                        "extended": 1,
                        "filter": "all"
                    })
                    # Get owner_id from first post if not set yet
                    if not owner_id:
                        current_posts = posts_data.get('items', [])
                        if current_posts:
                            owner_id = current_posts[0].get('owner_id')
                        else:
                            raise Exception(f"Не удалось найти посты для сообщества: {community_id}")
                        if not owner_id and posts_data.get('groups'):
                            owner_id = -posts_data['groups'][0]['id'] 
                            print(f"Неизвестный метод : owner_id найден: {owner_id}")
                        if not owner_id:
                            raise Exception(f"Не удалось найти owner_id для сообщества: {community_id}")

                 
                # Check if we got any posts
                current_posts = posts_data.get('items', [])
                if not current_posts:
                    print(f"Получено {len(all_posts)} постов (больше постов нет)")
                    break
                
                print(f"Получено {len(current_posts)} постов (всего: {len(all_posts) + len(current_posts)})")
                
                # Process posts
                for post in current_posts:
                    formatted_post = self._format_post(post, owner_id)
                    
                    # Get comments if requested
                    if self.config.include_comments:
                        formatted_post['comments'] = self._get_post_comments(owner_id, post['id'])
                    
                    # Get likes/reactions if requested
                    if self.config.include_reactions:
                        formatted_post['likes'] = self._get_post_likes(owner_id, post['id'])
                    
                    all_posts.append(formatted_post)
                
                # If we got fewer posts than requested, we've reached the end
                if len(current_posts) < posts_to_request:
                    print(f"Достигнут конец списка постов (получено {len(all_posts)} постов)")
                    break
                
                offset += len(current_posts)
            
            return all_posts
            
        except Exception as e:
            print(f"Ошибка при получении постов сообщества {community_id}: {e}")
            return []
    
    def _format_post(self, post: Dict[str, Any], owner_id: int) -> Dict[str, Any]:
        """Format post data."""
        post_id = post.get("id")
        vk_link = self._generate_post_link(owner_id, post_id)
        
        formatted_post = {
            "id": post_id,
            "owner_id": owner_id,
            "from_id": post.get("from_id", owner_id),
            "date": post.get("date"),
            "date_formatted": datetime.fromtimestamp(post.get("date", 0)).strftime('%d.%m.%Y %H:%M:%S'),
            "vk_link": vk_link,
            "text": post.get("text", ""),
            "attachments": self._format_attachments(post.get("attachments", [])),
            "post_type": post.get("post_type", "post"),
            "copy_history": self._format_copy_history(post.get("copy_history", [])),
            "can_pin": post.get("can_pin", 0),
            "can_delete": post.get("can_delete", 0),
            "can_edit": post.get("can_edit", 0),
            "is_pinned": post.get("is_pinned", 0),
            "marked_as_ads": post.get("marked_as_ads", 0),
            "is_favorite": post.get("is_favorite", False),
            "views": post.get("views", {}),
            "reposts": post.get("reposts", {}),
            "likes": post.get("likes", {}),
            "comments": post.get("comments", {})
        }
        
        return formatted_post
    
    def _generate_post_link(self, owner_id: int, post_id: int) -> str:
        """Generate VK link to post."""
        return f"https://vk.com/wall{owner_id}_{post_id}"
    
    def _format_attachments(self, attachments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format attachments with links instead of downloading."""
        formatted_attachments = []
        
        for att in attachments:
            att_type = att.get('type', 'unknown')
            formatted_att = {
                'type': att_type,
                'original_data': att
            }
            
            if att_type == 'photo':
                photo = att.get('photo', {})
                # Get largest photo size
                sizes = photo.get('sizes', [])
                if sizes:
                    largest = max(sizes, key=lambda x: x.get('width', 0) * x.get('height', 0))
                    formatted_att['url'] = largest.get('url')
                formatted_att['width'] = photo.get('width')
                formatted_att['height'] = photo.get('height')
                
            elif att_type == 'video':
                video = att.get('video', {})
                formatted_att['title'] = video.get('title', 'Видео')
                formatted_att['duration'] = video.get('duration')
                formatted_att['player'] = video.get('player')
                formatted_att['vk_link'] = f"https://vk.com/video{video.get('owner_id', '')}_{video.get('id', '')}"
                
            elif att_type == 'doc':
                doc = att.get('doc', {})
                formatted_att['title'] = doc.get('title', 'Документ')
                formatted_att['size'] = doc.get('size')
                formatted_att['url'] = doc.get('url')
                
            elif att_type == 'audio':
                audio = att.get('audio', {})
                formatted_att['artist'] = audio.get('artist', '')
                formatted_att['title'] = audio.get('title', 'Аудио')
                formatted_att['duration'] = audio.get('duration')
                
            elif att_type == 'link':
                link = att.get('link', {})
                formatted_att['url'] = link.get('url')
                formatted_att['title'] = link.get('title', 'Ссылка')
                formatted_att['description'] = link.get('description')
            
            formatted_attachments.append(formatted_att)
        
        return formatted_attachments
    
    def _format_copy_history(self, copy_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format copy history (reposts) with original links."""
        formatted_history = []
        
        for item in copy_history:
            owner_id = item.get('owner_id')
            post_id = item.get('id')
            
            formatted_item = {
                'id': post_id,
                'owner_id': owner_id,
                'from_id': item.get('from_id', owner_id),
                'date': item.get('date'),
                'date_formatted': datetime.fromtimestamp(item.get('date', 0)).strftime('%d.%m.%Y %H:%M:%S'),
                'text': item.get('text', ''),
                'vk_link': self._generate_post_link(owner_id, post_id),
                'attachments': self._format_attachments(item.get('attachments', []))
            }
            
            formatted_history.append(formatted_item)
        
        return formatted_history
    
    def _get_post_comments(self, owner_id: int, post_id: int, count: int = 100) -> List[Dict[str, Any]]:
        """Get comments for a specific post."""
        try:
            comments_data = self.vk.method("wall.getComments", {
                "owner_id": owner_id,
                "post_id": post_id,
                "count": count,
                "sort": "asc",
                "extended": 1
            })
            
            comments = []
            for comment in comments_data.get('items', []):
                comment_id = comment.get("id")
                comments.append({
                    "id": comment_id,
                    "from_id": comment.get("from_id"),
                    "date": comment.get("date"),
                    "date_formatted": datetime.fromtimestamp(comment.get("date", 0)).strftime('%d.%m.%Y %H:%M:%S'),
                    "text": comment.get("text", ""),
                    "attachments": self._format_attachments(comment.get("attachments", [])),
                    "reply_to_user": comment.get("reply_to_user"),
                    "reply_to_comment": comment.get("reply_to_comment"),
                    "likes": comment.get("likes", {}),
                    "thread": comment.get("thread", {}),
                    "vk_link": f"https://vk.com/wall{owner_id}_{post_id}?reply={comment_id}"
                })
            
            return comments
            
        except Exception as e:
            print(f"Ошибка при получении комментариев для поста {post_id}: {e}")
            return []
    
    def _get_post_likes(self, owner_id: int, post_id: int) -> Dict[str, Any]:
        """Get likes/reactions for a specific post."""
        try:
            likes_data = self.vk.method("likes.getList", {
                "type": "post",
                "owner_id": owner_id,
                "item_id": post_id,
                "count": 1000,
                "extended": 1
            })
            
            return {
                "count": likes_data.get("count", 0),
                "user_likes": likes_data.get("user_likes", 0),
                "can_like": likes_data.get("can_like", 1),
                "can_publish": likes_data.get("can_publish", 1),
                "users": [user.get("id") for user in likes_data.get("items", [])]
            }
            
        except Exception as e:
            print(f"Ошибка при получении лайков для поста {post_id}: {e}")
            return {"count": 0, "user_likes": 0, "can_like": 1, "can_publish": 1, "users": []}
    
    def save_posts(self, community_info: Dict[str, Any], posts: List[Dict[str, Any]], directory: str):
        """Save posts to files."""
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Prepare data structure
        posts_data = {
            "type": "community_posts",
            "export_date": datetime.now().isoformat(),
            "community": community_info,
            "posts_count": len(posts),
            "posts": posts
        }
        
        # Clean filename
        community_name = self._clean_filename(community_info.get("name", "unknown"))
        
        # Save JSON
        if "json" in self.config.export_formats:
            json_path = os.path.join(directory, f"{community_name}_posts.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(posts_data, f, ensure_ascii=False, indent=2)
            print(f"JSON сохранен: {json_path}")
        
        # Save HTML
        if "html" in self.config.export_formats:
            html_path = os.path.join(directory, f"{community_name}_posts.html")
            save_posts_html(posts_data, html_path)
            print(f"HTML сохранен: {html_path}")
    
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename from invalid characters."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        return filename[:100]  # Limit length
    
    def dump_posts(self) -> bool:
        """Main function to dump community posts."""
        try:
            print("Получение информации о сообществе...")
            community_info = self.get_community_info(self.config.vk_community_id)
            
            if not community_info:
                print("Не удалось получить информацию о сообществе.")
                return False
            
            print(f"Сообщество: {community_info['name']} (ID: {community_info['id']})")
            print(f"Участников: {community_info.get('members_count', 'N/A')}")
            
            print(f"\nПолучение постов (максимум {self.config.posts_count})...")
            posts = self.get_community_posts(self.config.vk_community_id, self.config.posts_count)
            
            if not posts:
                print("Посты не найдены или произошла ошибка.")
                return False
            
            print(f"Найдено {len(posts)} постов")
            
            # Preview first few posts
            print("Первые несколько постов для выгрузки:")
            for post in posts[:min(3, len(posts))]:
                text = post.get('text', '[Нет текста]')[:100]
                print(f"- Пост #{post['id']}: {text}{'...' if len(post.get('text', '')) > 100 else ''}")
            
            # Confirm before proceeding
            confirm = input(f"\nПродолжить выгрузку {len(posts)} постов? (y/N): ").lower() == 'y'
            if not confirm:
                print("Операция отменена.")
                return False
            
            # Create output directory
            output_dir = self.config.full_posts_path
            os.makedirs(output_dir, exist_ok=True)
            
            # Save posts
            print("Сохранение постов...")
            self.save_posts(community_info, posts, output_dir)
            
            print(f"\n✅ Выгрузка постов завершена! Файлы сохранены в: {output_dir}")
            return True
            
        except Exception as e:
            print(f"Ошибка при выгрузке постов: {e}")
            return False
