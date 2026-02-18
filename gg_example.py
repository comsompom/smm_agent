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


def clean_content(content, current_year):
    """
    Clean content by removing SEO hashtag labels and correcting years
    
    Args:
        content: The content string to clean
        current_year: The current year to use for corrections
    
    Returns:
        Cleaned content string
    """
    # 1. Remove "**SEO Optimised Hashtags:**" string from content (all variations)
    content = re.sub(r'\*\*SEO\s+Optimised\s+Hashtags:\*\*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'SEO\s+Optimised\s+Hashtags:', '', content, flags=re.IGNORECASE)
    content = re.sub(r'SEO\s+Optimised\s+Hashtags', '', content, flags=re.IGNORECASE)
    # Clean up any double newlines that might result
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # 2. Correct years in the content (not in dates)
    # Process line by line to avoid dates in format **DD-MM-YYYY**
    lines = content.split('\n')
    processed_lines = []
    for line in lines:
        # Skip lines that are date headers (format: **DD-MM-YYYY**)
        if re.match(r'^\s*\*\*\d{2}-\d{2}-\d{4}\*\*\s*$', line.strip()):
            processed_lines.append(line)
        else:
            # Replace years in this line (2000-2099) that are not current year
            def replace_year(match):
                year = int(match.group(0))
                # Replace if it's not the current year (handles future years like 2070, 2075, etc.)
                if year != current_year:
                    return str(current_year)
                return match.group(0)
            
            # Replace years 2000-2099 that are not current year
            # Use word boundaries to avoid matching parts of URLs or other numbers
            line = re.sub(r'\b(20[0-9]{2})\b', replace_year, line)
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)


def cleanup_moon_post_file():
    """
    Utility function to clean up the existing moon_post.md file
    Applies all three rules:
    1. Removes "**SEO Optimised Hashtags:**" strings
    2. Corrects years in content (not in dates) to current year
    3. Ensures file ends with "#Invest #DeepTech #NewFrontier #MoonColony" with no extra spaces
    """
    try:
        current_year = datetime.now().year
        required_ending = "#Invest #DeepTech #NewFrontier #MoonColony"
        file_path = "db_utils/moon_post.md"
        
        # Read existing content
        with open(file_path, "r", encoding='utf-8') as news_file:
            content = news_file.read()
        
        # Clean the content
        content = clean_content(content, current_year)
        
        # Remove trailing spaces
        content = content.rstrip()
        
        # Ensure it ends with the required hashtags
        if not content.endswith(required_ending):
            content = content.rstrip()
            if content:
                content += '\n\n' + required_ending
            else:
                content = required_ending
        
        # Write cleaned content back
        with open(file_path, "w", encoding='utf-8') as updated_file:
            updated_file.write(content)
        
        print(f"✅ Cleaned up moon_post.md file")
        print(f"   - Removed SEO hashtag labels")
        print(f"   - Corrected years to {current_year}")
        print(f"   - Ensured proper ending with required hashtags")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up moon_post.md file: {e}")
        return False


def update_news_file(content):
    try:
        current_year = datetime.now().year
        required_ending = "#Invest #DeepTech #NewFrontier #MoonColony"
        
        # Clean the new content (remove SEO hashtag labels and correct years)
        content = clean_content(content, current_year)
        
        # Read existing content
        last_content = None
        with open("db_utils/moon_post.md", "r", encoding='utf-8') as news_file:
            last_content = news_file.read()
        
        # Clean up the existing content:
        # 1. Remove "**SEO Optimised Hashtags:**" if present
        last_content = clean_content(last_content, current_year)
        
        # 2. Remove trailing spaces and ensure proper ending
        last_content = last_content.rstrip()
        
        # 3. Ensure it ends with the required hashtags
        if not last_content.endswith(required_ending):
            last_content = last_content.rstrip()
            if last_content:
                last_content += '\n\n' + required_ending
            else:
                last_content = required_ending
        
        # Create new content
        new_content = (f'**{datetime.now().strftime("%d-%m-%Y")}**\n'
                       f'\n{content}\n\n{last_content}')
        
        # Remove any trailing whitespace
        new_content = new_content.rstrip()
        
        # Ensure it ends with the required hashtags (final check)
        if not new_content.endswith(required_ending):
            new_content = new_content.rstrip()
            if new_content:
                new_content += '\n\n' + required_ending
            else:
                new_content = required_ending
        
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
                  "persuasive conclusive document Generative AI Evolution "
                  "in the Moon Lunar Colony. It should contain the last AI "
                  "evolution changes of the last two weeks. The final document "
                  "should contain randomly from 130 to 190 words, should "
                  "be attractive and must include the mention https://moonhome.agency/, "
                  "Also must has hashtags, include the project web page "
                  "https://moonhome.agency/")
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
                model="gemini-3-flash-preview",
                contents=[prompt,],
            )
        except Exception as exc:
            last_err = exc

        if response:
            with open(helper_file, "w", encoding="utf-8") as file_to_save:
                file_to_save.write(response.text)

            print(response.text)
            
            # Create SQL file for database insertion
            # Temporary commented until future database releases
            # sql_file = create_sql_file(response.text)
            # if sql_file:
            #     print(f"🎉 Successfully created SQL file: {sql_file}")
            # else:
            #     print("⚠️  Failed to create SQL file")

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
