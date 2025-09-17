import time
import os
import re
from datetime import datetime
from google import genai
from utils import get_api_key


def parse_content_and_tags(content):
    """Parse content and extract hashtags"""
    # Split content into lines
    lines = content.strip().split('\n')
    
    # Find the last line that starts with # (tags)
    content_lines = []
    tags_line = ""
    
    for line in lines:
        if line.strip().startswith('#'):
            tags_line = line.strip()
        else:
            content_lines.append(line)
    
    # Join content lines
    main_content = '\n'.join(content_lines).strip()
    
    # If no tags found, try to extract hashtags from content
    if not tags_line:
        hashtags = re.findall(r'#\w+', main_content)
        if hashtags:
            tags_line = ' '.join(hashtags)
            # Remove hashtags from content
            main_content = re.sub(r'#\w+', '', main_content).strip()
    
    # Clean up content (remove extra whitespace)
    main_content = re.sub(r'\s+', ' ', main_content).strip()
    
    return main_content, tags_line


def create_sql_file(content):
    """Create SQL file with current content and timestamp"""
    try:
        # Parse content and extract tags
        main_content, tags = parse_content_and_tags(content)
        
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_filename = f"db_utils/news_{timestamp}.sql"
        
        # Ensure db_utils directory exists
        os.makedirs("db_utils", exist_ok=True)
        
        # Create SQL content
        sql_content = f"""-- SQL file created on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
-- Auto-generated from AI response

INSERT INTO news (date, item, tags) VALUES (
    '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
    '{main_content.replace("'", "''")}',
    '{tags.replace("'", "''")}'
);

-- Verify the insertion
SELECT COUNT(*) as total_records FROM news;
SELECT id, date, LEFT(item, 100) as item_preview, tags FROM news ORDER BY date DESC LIMIT 1;
"""
        
        # Write SQL file
        with open(sql_filename, 'w', encoding='utf-8') as sql_file:
            sql_file.write(sql_content)
        
        print(f"✅ SQL file created: {sql_filename}")
        print(f"📝 Content: {main_content[:100]}{'...' if len(main_content) > 100 else ''}")
        print(f"🏷️  Tags: {tags}")
        
        return sql_filename
        
    except Exception as e:
        print(f"❌ Error creating SQL file: {e}")
        return None


def update_news_file(content):
    try:
        last_content = None
        # Read with UTF-8 encoding
        with open("db_utils/moon_post.md", "r", encoding='utf-8') as news_file:
            last_content = news_file.read()
        
        new_content = (f'**{datetime.now().strftime("%d-%m-%Y")}**\n'
                       f'\n{content}\n\n{last_content}\n')
        
        # Write with UTF-8 encoding
        with open("db_utils/moon_post.md", "w", encoding='utf-8') as updated_file:
            updated_file.write(new_content)

        print(f"✅ News file Updated: db_utils/moon_post.md")
        print(f"📝 Content: {new_content[:100]}{'...' if len(new_content) > 100 else ''}")

        return "db_utils/moon_post.md"
        
    except Exception as e:
        print(f"❌ Error updating news file: {e}")
        return None


def create_new_message(msg_type):
    client = genai.Client(api_key=get_api_key())

    if msg_type == 1:
        prompt = ("create well psychologically attractive and very "
                  "persuasive conclusive document about investment to the "
                  "Moon Lunar like the  one of the best "
                  "investment in to the future. The document should "
                  "contain randomly from 120 to 170 words, should "
                  "be SEO optimised, must has hashtags, include the "
                  "project web page https://moonhome.agency/")
    elif msg_type == 2:
        prompt = ("can you create a simple history of the Moon Lunar "
                  "colony day. The history should contain the genetic "
                  "investigation, gathering resources, looking for the "
                  "space around, constructing the new buildings. In the "
                  "history should be described some persons pioneers with "
                  "their name and the jobs that they are doing, The all "
                  "history should not be more than 200 words. At the end "
                  "of the history should be provided some useful SEO "
                  "optimised hashtags.")

    helper_file = "smm_message.md"

    response = None
    while not response:
        last_err = None
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt,],
            )
        except Exception as exc:
            last_err = exc

        if response:
            with open(helper_file, "w", encoding="utf-8") as file_to_save:
                file_to_save.write(response.text)

            print(response.text)
            
            # Create SQL file for database insertion
            sql_file = create_sql_file(response.text)
            if sql_file:
                print(f"🎉 Successfully created SQL file: {sql_file}")
            else:
                print("⚠️  Failed to create SQL file")

            updated_file = update_news_file(response.text)
            if updated_file:
                print(f"🎉 Successfully Updated News file: {updated_file}")
            else:
                print("⚠️  Failed to Update News file")
        else:
            print(f'{last_err.code} Error')
            if last_err.code == 429:
                print(last_err.message)
                break
            else:
                print("waiting 30 sec...")
                time.sleep(30)
