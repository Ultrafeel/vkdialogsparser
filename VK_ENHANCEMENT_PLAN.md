# VK Dialogs Parser Enhancement Plan

## Overview
Enhance the existing VK dialogs parser to support community posts dumping with both JSON and HTML export formats, following modern configuration practices from tele-copy project.

## Current State Analysis

### Existing Features
- ✅ Dialog/conversation dumping to JSON
- ✅ Multi-threaded processing
- ✅ Support for users, groups, and chats
- ✅ Message history extraction with attachments

### Current Issues
- ❌ Hardcoded input prompts (no .env support)
- ❌ No community posts support
- ❌ Only JSON export format
- ❌ Monolithic code structure
- ❌ No configuration validation
- ❌ Limited error handling

## Enhancement Goals

### Primary Features
1. **Community Posts Dumping**
   - Extract posts from VK public groups/communities
   - Support for post content, comments, reactions
   - Handle all attachment types (photos, videos, documents, etc.)

2. **Multi-format Export**
   - JSON format (existing + enhanced)
   - HTML format with proper styling and media embedding
   - Configurable export formats

3. **Modern Configuration System**
   - `.env` file support following tele-copy pattern
   - Input fallback for missing parameters
   - Configuration validation

4. **Code Refactoring**
   - Modular architecture with separate files
   - Clean separation of concerns
   - Better error handling and logging

## Implementation Architecture

### File Structure
```
vkdialogsparser/
├── main.py                 # Entry point and orchestration
├── .env.example            # Environment variables template
├── .env                    # User configuration (gitignored)
├── requirements.txt        # Dependencies
├── config/
│   └── settings.py         # Configuration management
├── modules/
│   ├── __init__.py
│   ├── dialogs.py          # Dialog dumping functionality
│   ├── posts.py            # Community posts dumping
│   └── exporters.py        # JSON/HTML export handlers
└── templates/
    └── post_template.html  # HTML template for posts
```

### Configuration System (.env approach)
```env
# VK API Configuration
VK_TOKEN=your_vk_token_here
VK_APP_ID=your_app_id

# Operation Mode
DUMP_MODE=dialogs  # dialogs, posts, both
EXPORT_FORMAT=json,html  # json, html, or both

# Threading
THREAD_COUNT=4

# Output Configuration
OUTPUT_DIRECTORY=output
DIALOGS_DIRECTORY=dialogs
POSTS_DIRECTORY=posts

# Community Posts Configuration (when DUMP_MODE=posts or both)
VK_COMMUNITY_ID=your_community_id
POSTS_COUNT=100
INCLUDE_COMMENTS=true
INCLUDE_REACTIONS=true

# Dialog Configuration (when DUMP_MODE=dialogs or both)
MAX_DIALOGS=200
```

## Implementation Phases

### Phase 1: Configuration System
- [ ] Create `.env` support with python-dotenv
- [ ] Implement `config/settings.py` with validation
- [ ] Add input fallback for missing parameters
- [ ] Create `.env.example` template

### Phase 2: Code Refactoring
- [ ] Extract dialog functionality to `modules/dialogs.py`
- [ ] Create base exporter classes in `modules/exporters.py`
- [ ] Implement proper error handling and logging
- [ ] Update main.py to use modular approach

### Phase 3: Community Posts Feature
- [ ] Implement `modules/posts.py` for community posts dumping
- [ ] Add VK API methods for posts extraction
- [ ] Support for post content, comments, reactions
- [ ] Handle all attachment types

### Phase 4: HTML Export
- [ ] Create HTML templates for posts and dialogs
- [ ] Implement HTML exporter with proper styling
- [ ] Add media embedding and responsive design
- [ ] Generate index pages for navigation

### Phase 5: Testing & Polish
- [ ] Add error handling and retry logic
- [ ] Implement progress indicators
- [ ] Add configuration validation
- [ ] Create comprehensive documentation

## Technical Details

### VK API Methods for Posts
- `wall.get` - Get community posts
- `wall.getComments` - Get post comments
- `likes.getList` - Get post reactions
- `photos.get`, `video.get`, etc. - Get media attachments

### Export Formats

#### JSON Structure (Enhanced)
```json
{
  "type": "community_posts",
  "community": {
    "id": -12345,
    "name": "Community Name",
    "screen_name": "community_url"
  },
  "posts": [
    {
      "id": 123,
      "date": "2024-01-01T12:00:00Z",
      "text": "Post content",
      "attachments": [...],
      "comments": [...],
      "likes": {...},
      "reposts": {...}
    }
  ]
}
```

#### HTML Structure
- Responsive design with CSS Grid/Flexbox
- Embedded media (images, videos)
- Collapsible comments sections
- Search and filter functionality
- Export date and metadata

## Dependencies to Add
```txt
python-dotenv>=1.0.0
jinja2>=3.1.0  # For HTML templating
requests>=2.31.0  # For media downloading
```

## Usage Examples

### Environment Configuration
```bash
# Copy template
cp .env.example .env

# Edit configuration
nano .env
```

### Command Line Usage
```bash
# Dump dialogs only (current functionality)
python main.py

# Dump community posts only
VK_COMMUNITY_ID=12345 DUMP_MODE=posts python main.py

# Dump both with HTML export
DUMP_MODE=both EXPORT_FORMAT=json,html python main.py
```

## Preview Implementation

Similar to tele-copy's preview approach:
```python
# Preview first few posts before full dump
print("First few posts to be dumped:")
for post in posts[:min(3, len(posts))]:
    text = post.get('text', '[No text]')[:100]
    print(f"- Post {post['id']}: {text}{'...' if len(post.get('text', '')) > 100 else ''}")

confirm = input(f"\nProceed with dumping {len(posts)} posts? (y/N): ").lower() == 'y'
```

## Security Considerations
- Store VK tokens in .env (gitignored)
- Validate community IDs and permissions
- Rate limiting for API calls
- Secure media file downloads

## Future Enhancements - low priority
- Incremental updates
- Database storage option
- Real-time monitoring mode
- Web interface for configuration
- Telegram bot integration
