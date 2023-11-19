import random
import codecs
import io
from googleapiclient.discovery import build

CHANNEL_ID = "UCucot-Zp428OwkyRm2I7v2Q"

def get_youtube():
    DEVELOPER_KEY = 'AIzaSyBDMskOiFNVdaJsddWV4tKiNtVxn5tTjhg'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    return youtube

def extract_comments(comment_threads, keywords):
    comments = []
    for comment_thread in comment_threads:
        comment = comment_thread["snippet"]["topLevelComment"]
        comment_text = comment["snippet"]["textDisplay"]

        if any(keyword in comment_text.lower() for keyword in keywords):
            comments.append(comment_text)
    return comments

def main():
    youtube = get_youtube()

    request = youtube.search().list(
        part="snippet",
        type="video",
        channelId=CHANNEL_ID,
        maxResults=50  # Fetch more comments
    )
    response = request.execute()

    all_comments = []
    for item in response.get("items", []):
        videoId = item['id']['videoId']

        request_comments = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
        )
        response_comments = request_comments.execute()

        keywords = ["fat", "ugly", "skinny", "obese", "lumpy", "disgusting", "chubby", "gross"]
        comments = extract_comments(response_comments.get("items", []), keywords)

        all_comments.extend(comments)

    # Remove duplicates and shuffle
    unique_comments = list(set(all_comments))
    random.shuffle(unique_comments)

    # Limit to a specific number of comments you want to write to the file
    comments_to_write = unique_comments[:20]  # Adjust the number as needed

    with io.open("comments.txt", "a", encoding="utf-8") as f:
        for comment in comments_to_write:
            f.write(comment + "\n")

if __name__ == "__main__":
    main()
