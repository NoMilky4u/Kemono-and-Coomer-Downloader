```markdown
# Attachment Downloader

A Python script that fetches data from specified APIs and downloads attachments and files associated with posts. This tool is designed to work with specific platforms and their respective APIs, allowing users to easily download content.

## Features

- Fetch data from specified API URLs.
- Download files and handle duplicate file names by appending a counter.
- Process both single posts and lists of posts (profiles).
- Log progress and errors for better debugging and tracking.

## Requirements

- Python 3.x
- `requests` library

You can install the required library using pip:


pip install requests
```

## Usage

1. Clone the repository or download the script.
2. Run the script using Python:

   ```bash
   python downloader.py
   ```

3. When prompted, enter the URL of the user profile or post you want to download attachments from. The script supports the following formats:

   - `https://kemono.su/patreon/user/{username}`
   - `https://kemono.su/patreon/user/{username}/post/{postid}`
   - `https://coomer.su/onlyfans/user/{username}`
   - `https://coomer.su/onlyfans/user/{username}/post/{postid}`
   - `https://coomer.su/fansly/user/{username}`
   - `https://coomer.su/fansly/user/{username}/post/{postid}`

4. The downloaded files will be saved in a directory named `downloaded_images`.
