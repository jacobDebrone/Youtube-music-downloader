import os
import subprocess
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yt_dlp

# Set up the API key
api_key = 'your-api-key'  # Replace with your actual YouTube Data API key

# Create a YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

def download_media(video_id, is_audio=False):
    """Downloads a YouTube video or audio using yt-dlp.

    Args:
        video_id: The ID of the YouTube video to download.
        is_audio: True if downloading audio, False for video.
    """
    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'best',
        'outtmpl': f'%(title)s.{"mp3" if is_audio else "mp4"}',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

def search_videos(search_query):
    """Searches for YouTube videos using the YouTube Data API.

    Args:
        search_query: The search query to use.

    Returns:
        A list of dictionaries containing video titles and video IDs.
    """

    # Search for YouTube videos
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='snippet',
        maxResults=10  # You can adjust the number of results as needed
    ).execute()

    # Extract video titles and video IDs from the search response
    video_results = []
    for item in search_response['items']:
        video_results.append({
            'title': item['snippet']['title'],
            'videoId': item['id']['videoId']
        })

    return video_results

def main():
    # Get the user's search query
    search_query = input('Enter a search query: ')

    # Search for YouTube videos
    video_results = search_videos(search_query)

    # Display the search results with titles
    print('Search results:')
    for index, video_info in enumerate(video_results):
        print(f'{index}: {video_info["title"]}')

    # Get the user's choice of video
    video_index = int(input('Enter the index of the video you want to download: '))

    if 0 <= video_index < len(video_results):
        # Get the video ID of the selected video
        video_id = video_results[video_index]['videoId']

        # Ask the user if they want to download audio or video
        choice = input('Download as (v)ideo or (a)udio? ')

        if choice.lower() == 'v':
            # Download the video
            download_media(video_id)
            print(f'Downloaded the video: {video_results[video_index]["title"]}.mp4')
        elif choice.lower() == 'a':
            # Download the audio
            download_media(video_id, is_audio=True)
            print(f'Downloaded the audio: {video_results[video_index]["title"]}.mp3')
        else:
            print('Invalid choice. Exiting.')
    else:
        print('Invalid video index. Exiting.')

if __name__ == '__main__':
    main()
