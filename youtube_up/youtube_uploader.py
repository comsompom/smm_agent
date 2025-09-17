import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


CLIENT_SECRETS_FILE = "client_secret.json"
API_NAME = 'youtube'
API_VERSION = 'v3'
# This scope allows for full access to the user's YouTube account,
# including uploading videos.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def get_authenticated_service():
    """
    Authenticates the user and returns a YouTube API service object.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            # This will open a browser window for authentication
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return build(API_NAME, API_VERSION, credentials=creds)


def upload_video(youtube, video_path, title, description, category_id, tags, privacy_status):
    """
    Uploads a video to YouTube.
    
    Args:
        youtube: The authenticated YouTube API service object.
        video_path (str): The path to the video file.
        title (str): The title of the video.
        description (str): The description of the video.
        category_id (str): The category ID for the video.
                           (e.g., '22' for People & Blogs, '28' for Science & Technology)
        tags (list): A list of tags for the video.
        privacy_status (str): The privacy status ('public', 'private', 'unlisted').
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    # The resumable=True is important for large files and unreliable connections.
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    print(f"Uploading video: {title}...")
    
    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )

    # This loop shows the upload progress.
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload successful! Video ID: {response['id']}")
    print(f"Watch your video at: https://www.youtube.com/watch?v={response['id']}")


if __name__ == '__main__':
    # --- Details for the video you want to upload ---
    VIDEO_MAIN_TAGS = ("#MoonColony #LunarCitizenship #FutureInvestment "
                       "#SpaceSettlement #SpaceInvestment #FutureIsNow")
    VIDEO_FILE_PATH = "videos/scene_full.mp4" # IMPORTANT: Change this to your video's path
    VIDEO_TITLE = "Moon History. Full Lunar Movie."
    VIDEO_DESCRIPTION = f"Find the solutions to the new future! The combined movie {VIDEO_MAIN_TAGS}"
    VIDEO_TAGS = ["Python", "YouTube API", "Automation", "Bot"]
    
    # YouTube video categories: https://developers.google.com/youtube/v3/docs/videoCategories/list
    # Common ones: 22 (People & Blogs), 24 (Entertainment), 27 (Education), 28 (Science & Technology)
    VIDEO_CATEGORY_ID = "28" 
    
    # 'public', 'private', or 'unlisted'
    PRIVACY_STATUS = "public"

    # 1. Authenticate
    youtube_service = get_authenticated_service()
    
    # 2. Upload the video
    upload_video(
        youtube=youtube_service,
        video_path=VIDEO_FILE_PATH,
        title=VIDEO_TITLE,
        description=VIDEO_DESCRIPTION,
        category_id=VIDEO_CATEGORY_ID,
        tags=VIDEO_TAGS,
        privacy_status=PRIVACY_STATUS
    )
