#!/usr/bin/env python3
import os
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import threading
from tqdm import tqdm
import lyricsgenius

# Define constants
VIDEO_EXTENSION = '.mp4'
AUDIO_EXTENSION = '.mp3'

# Set up the API keys (Replace with your actual YouTube Data API key and Lyrics Genius API token)
api_key = 'YOUTUBE-API'
genius_token = 'GENIUS-TOKEN'

# Create clients for YouTube Data API and Lyrics Genius API
youtube = build('youtube', 'v3', developerKey=api_key)
genius = lyricsgenius.Genius(genius_token)


def download_media(video_id, is_audio=False):
    """Downloads a YouTube video or audio using yt-dlp."""
    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'best',
        'outtmpl': f'%(title)s.{AUDIO_EXTENSION if is_audio else VIDEO_EXTENSION}',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]
            print(f'Downloaded: {info_dict["title"]}{AUDIO_EXTENSION if is_audio else VIDEO_EXTENSION}')
    except yt_dlp.DownloadError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_video(video_info):
    """Downloads a video in a separate thread with a progress bar."""
    video_id = video_info['videoId']
    with tqdm(unit='B', unit_scale=True, leave=False, miniters=1, desc=f'Downloading Video: {video_info["title"]}  ',
              ncols=100) as progress_bar:
        def hook(data):
            progress_bar.update(data['downloaded_bytes'])

        ydl_opts = {
            'format': 'best',
            'progress_hooks': [hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])


def download_audio(video_info):
    """Downloads audio in a separate thread with a progress bar."""
    video_id = video_info['videoId']
    with tqdm(unit='B', unit_scale=True, leave=False, miniters=1, desc=f'Downloading Audio: {video_info["title"]}  ',
              ncols=100) as progress_bar:
        def hook(data):
            progress_bar.update(data['downloaded_bytes'])

        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])


def search_videos(search_query):
    """Searches for YouTube videos using the YouTube Data API."""
    try:
        search_response = youtube.search().list(
            q=search_query,
            type='video',
            part='snippet',
            maxResults=15
        ).execute()
        video_results = []
        for item in search_response['items']:
            video_results.append({
                'title': item['snippet']['title'],
                'videoId': item['id']['videoId']
            })
        return video_results
    except HttpError as e:
        print(f"HTTP Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_lyrics(song_title, artist_name):
    """Downloads song lyrics using the Lyrics Genius API."""
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            lyrics_file = f"{song_title} - {artist_name}.txt"
            with open(lyrics_file, 'w', encoding='utf-8') as f:
                f.write(song.lyrics)
            print(f"Lyrics downloaded: {lyrics_file}")
        else:
            print("Lyrics not found. Please try a different search query.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    print("Program made by Jacob Debrone")
    while True:
        # Ask the user for their choice
        choice = input('What would you like to download? (v)ideo, (a)udio, or (l)yrics? (type "exit" to quit): ')
        if choice.lower() == 'exit':
            break
        elif choice.lower() == 'v':
            # Get the user's search query
            search_query = input('Enter a search query: ')
            # Search for YouTube videos
            video_results = search_videos(search_query)
            if not video_results:
                print('No videos found. Please try a different search query.')
                continue
            # Display the search results with titles
            print('Search results:')
            for index, video_info in enumerate(video_results):
                print(f'{index}: {video_info["title"]}')
            # Get the user's choice of video
            while True:
                try:
                    video_index = int(input('Enter the index of the video you want to download (type -1 to go back): '))
                    if video_index == -1:
                        break
                    if 0 <= video_index < len(video_results):
                        # Get the video info of the selected video
                        selected_video = video_results[video_index]
                        # Download the video
                        download_video(selected_video)
                        break
                    else:
                        print('Invalid video index. Please enter a valid index.')
                except ValueError:
                    print('Invalid input. Please enter a valid index.')
        elif choice.lower() == 'a':
            # Get the user's search query
            search_query = input('Enter a search query: ')
            # Search for YouTube videos
            video_results = search_videos(search_query)
            if not video_results:
                print('No videos found. Please try a different search query.')
                continue
            # Display the search results with titles
            print('Search results:')
            for index, video_info in enumerate(video_results):
                print(f'{index}: {video_info["title"]}')
            # Get the user's choice of video
            while True:
                try:
                    video_index = int(input('Enter the index of the video you want to download (type -1 to go back): '))
                    if video_index == -1:
                        break
                    if 0 <= video_index < len(video_results):
                        # Get the video info of the selected video
                        selected_video = video_results[video_index]
                        # Download the audio
                        download_audio(selected_video)
                        break
                    else:
                        print('Invalid video index. Please enter a valid index.')
                except ValueError:
                    print('Invalid input. Please enter a valid index.')
        elif choice.lower() == 'l':
            # Get the song title and artist name
            song_title = input('Enter the song title: ')
            artist_name = input('Enter the artist name: ')
            # Download song lyrics
            try:
                download_lyrics(song_title, artist_name)
            except UnicodeEncodeError:
                print("An error occurred while downloading lyrics. Please try a different search query.")
                continue
        else:
            print('Invalid choice. Please enter "v", "a", or "l".')


if __name__ == '__main__':
    main()
