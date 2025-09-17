
### **Disclaimer**
This process involves handling sensitive credentials. Never share your `client_secrets.json` file or your `token` file with anyone. Be mindful of YouTube's API usage policies and quotas to avoid getting your access suspended.

---

### **Part 1: Create Your YouTube Channel**

This is the foundational step. If you already have a channel, you can skip to Part 2.

1.  **Sign in to YouTube:** Go to [youtube.com](https://youtube.com) and sign in with your Google Account.
2.  **Go to Channel Creation:**
    *   Click on your profile picture in the top-right corner.
    *   Select **"Create a channel"**.
    *   You'll be prompted to enter a name and handle for your channel.

3.  **(Recommended) Create a Brand Account Channel:** A Brand Account is more flexible than a personal one, especially for automated projects. It can have multiple managers and a different name from your Google Account.
    *   Go to your [Channel Switcher page](https://www.youtube.com/channel_switcher).
    *   Click **"Create a channel"**.
    *   Give it a name (e.g., "My Python Bot Channel") and follow the on-screen instructions.

4.  **Customize Your Channel:** Once created, you can go to YouTube Studio to add a profile picture, banner, description, etc. This is good practice but not required for the bot to work.

---

### **Part 2: Set Up Your Developer Environment (Google Cloud & API Keys)**

This is the most crucial part. We need to tell Google that our Python script is a legitimate application that has permission to act on your behalf.

**Step 1: Create a Google Cloud Project**
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Click the project dropdown at the top of the page (it might say "My First Project").
3.  In the dialog that appears, click **"NEW PROJECT"**.
4.  Give your project a name (e.g., "YouTube Uploader Bot") and click **"CREATE"**.

**Step 2: Enable the YouTube Data API v3**
1.  Make sure your new project is selected in the top dropdown.
2.  In the navigation menu (hamburger icon ☰), go to **APIs & Services > Library**.
3.  In the search bar, type `YouTube Data API v3` and select it from the results.
4.  Click the **"ENABLE"** button.

**Step 3: Configure the OAuth Consent Screen**
This screen is what you will see when you first run the bot, asking you to grant permission.
1.  In the left menu, go to **APIs & Services > OAuth consent screen**.
2.  Choose the User Type: Select **"External"** and click **"CREATE"**.
3.  Fill in the required information:
    *   **App name:** "Python YouTube Uploader" (or whatever you like).
    *   **User support email:** Select your email address.
    *   **Developer contact information:** Enter your email address again.
4.  Click **"SAVE AND CONTINUE"**. On the "Scopes" and "Test Users" pages, you can just click **"SAVE AND CONTINUE"** for now. You don't need to add anything there for this project.
5.  On the Summary page, click **"BACK TO DASHBOARD"**.
6.  You'll see the Publishing status is "Testing". This is perfectly fine. It means only you (as a test user added to the project) can authorize the app.

**Step 4: Create Your Credentials**
This will generate the secret file our Python script needs to identify itself.
1.  In the left menu, go to **APIs & Services > Credentials**.
2.  Click **"+ CREATE CREDENTIALS"** at the top and select **"OAuth client ID"**.
3.  For **Application type**, select **"Desktop app"**.
4.  Give it a name (e.g., "Desktop Client 1") and click **"CREATE"**.
5.  A window will pop up with your Client ID and Client Secret. **You don't need to copy these.** Instead, click the **"DOWNLOAD JSON"** button on the right.
6.  Save this file in your Python project directory. **Rename the downloaded file to `client_secrets.json`**. This exact name is important for the script.

You have now completed the Google Cloud setup!

---

### **Part 3: The Python Bot - Code & Explanation**

Now we write the Python code that will perform the upload.

**Step 1: Install Necessary Libraries**
Open your terminal or command prompt and install the required Google API client libraries for Python:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Code Explanation:**
*   **`get_authenticated_service()`**: This function handles the OAuth 2.0 flow. The very first time you run it, it will open your web browser, ask you to log in to your Google Account, and request permission to manage your YouTube videos. After you grant permission, it saves your credentials in a file named `token.pickle`. On all subsequent runs, it will reuse these saved credentials so you don't have to log in again.
*   **`upload_video()`**: This function constructs the request to the YouTube API. It builds a `body` with all the metadata (title, description, etc.) and uses `MediaFileUpload` to handle the actual video file. The `resumable=True` flag is highly recommended as it allows the upload to resume if your internet connection drops.
*   **`if __name__ == '__main__':`**: This is the main block where you configure the details of your video. **You must change `VIDEO_FILE_PATH`** to the actual path of the video file you want to upload.

---

### **Part 4: Running the Bot & Automation**

**Step 1: Your First Run (The Authentication Step)**
1.  Make sure your project directory contains:
    *   `upload_bot.py`
    *   `client_secrets.json`
    *   The video file you want to upload (e.g., `my_video.mp4`).
2.  Update the `VIDEO_FILE_PATH` variable in the script to point to your video file.
3.  Open your terminal/command prompt, navigate to your project directory, and run the script:
    ```bash
    python upload_bot.py
    ```
4.  Your web browser will automatically open.
5.  Choose the Google Account associated with your YouTube channel.
6.  You might see a "Google hasn’t verified this app" warning. This is normal because your app is in "Testing" mode. Click **"Advanced"** and then **"Go to [Your App Name] (unsafe)"**.
7.  Click **"Allow"** to grant your script permission to manage your YouTube account.
8.  The browser tab will say "The authentication flow has completed." You can close it.
9.  Go back to your terminal. The script will now start uploading the video and will print its progress!

**Step 2: Subsequent Runs**
After the first run, a `token.pickle` file will be created in your directory. Now, whenever you run `python upload_bot.py`, it will use this token and immediately start the upload without needing you to log in via the browser.

**Step 3: True Automation (Scheduling)**
To make the bot truly automatic, you need to schedule it to run at certain times.

*   **For Linux/macOS (using Cron jobs):**
    Open your terminal and type `crontab -e`. Add a line like this to run the script every day at 2 PM:
    ```cron
    0 14 * * * /usr/bin/python3 /path/to/your/project/upload_bot.py
    ```
    *(Make sure the paths to python and your script are correct.)*

*   **For Windows (using Task Scheduler):**
    1.  Open Task Scheduler.
    2.  Click "Create Basic Task...".
    3.  Give it a name and description.
    4.  Set the "Trigger" (e.g., Daily, and choose a time).
    5.  For the "Action", select "Start a program".
    6.  In "Program/script", browse to your Python executable (e.g., `C:\Python39\python.exe`).
    7.  In "Add arguments (optional)", put the name of your script: `upload_bot.py`.
    8.  In "Start in (optional)", put the full path to your project directory (this is important so the script can find `client_secrets.json` and the video file).
    9.  Finish the wizard.

---

### **Part 5: Important Considerations & Best Practices**

*   **YouTube API Quotas:** The YouTube API is not free to use indefinitely. It has a daily quota of 10,000 "units". A single video upload costs **1600 units**. This means you can upload about **6 videos per day** by default with a new project. If you need more, you must apply for a quota extension from the Google Cloud Console.
*   **Dynamic Video Details:** Don't hardcode the video details in the script. A better approach is to read them from a text file, a CSV, or a simple database. Your script could then pick the next video in the queue, upload it, and mark it as complete.
*   **Error Handling:** The provided script is basic. A production-ready script should have `try...except` blocks to gracefully handle network errors, API errors, or cases where a video file is missing.
*   **Security:** Your `client_secrets.json` and `token.pickle` files are highly sensitive. Add them to your `.gitignore` file if you are using Git, and never commit them to a public repository.

