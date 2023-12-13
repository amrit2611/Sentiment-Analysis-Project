import random
import codecs
import io
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CHANNEL_IDS = ["UCucot-Zp428OwkyRm2I7v2Q", "UCkvK_5omS-42Ovgah8KRKtg", "UC4qk9TtGhBKCkoWz5qGJcGg", "UCNGkAYEhcVdlwJITJSnB73A", "UCnQC_G5Xsjhp9fEJKuIcrSw", "UCGp6FxRC5mcRvoPz71NMpHg", "UC7bYyWCCCLHDU0ZuNzGNTtg", "UCEy0HWmgp2PUTBICGqKfB_A", "UCVWTuLqDlnJZYeIt-tUBdvw"]

def get_youtube():
    DEVELOPER_KEY = 'AIzaSyBag1Gj-Dsvw47-PvRNtjefVRgFIMxgC3A'
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
    
    all_comments = []
    for channel_id in CHANNEL_IDS:
        request = youtube.search().list(
            part="snippet",
            type="video",
            channelId=channel_id,
            maxResults=50  # Fetch more comments
        )
        response = request.execute()

        for item in response.get("items", []):
            videoId = item['id']['videoId']

            try:
                request_comments = youtube.commentThreads().list(
                    part="snippet",
                    videoId=videoId,
                    maxResults=100
                )
                response_comments = request_comments.execute()
                
                keywords = ["fat", "ugly", "skinny", "obese", "lumpy", "disgusting", "chubby", "gross", "plus", "size", "sized", "overeat", "lose weight", "weight", "bony", "skeletal", "scrawny", "bulky", "thick", "toothpick", "too thin", "underweight", "overweight", "anorexic", "bullmic", "twig", "reed", "stick figure", "morbid", "morbidly obese", "fatso", "chunky", "plump", "lard", "butterball", "blob", "hideous", "baggy", "revealing", "waddling", "slumping", "jiggling"]
                # ["fat", "ugly", "skinny", "obese"]
                comments = extract_comments(response_comments.get("items", []), keywords)

                all_comments.extend(comments)

            except HttpError as e:
                # Check if the error is due to comments being disabled
                if "commentsDisabled" in str(e):
                    print(f"Comments disabled for video: {videoId}")
                else:
                    print(f"Error processing video {videoId}: {e}")


    # Remove duplicates and shuffle
    unique_comments = list(set(all_comments))
    random.shuffle(unique_comments)

    # Limit to a specific number of comments we want to write to the file in one go
    comments_to_write = unique_comments[:50]  

    with io.open("comments.txt", "a", encoding="utf-8") as f:
        for comment in comments_to_write:
            f.write(comment + "\n")

if __name__ == "__main__":
    main()
