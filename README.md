YouTube Media Downloader with Lyrics (Python)

YouTube Media Downloader
Table of Contents

    Introduction
    Features
    Prerequisites
    Installation
    Usage
    Configuration
    Contributing
    License

Introduction

The music/music video downloader is a Python program that allows you to search for YouTube videos, download them as video or audio files, and even download lyrics for your favorite songs. It provides an interactive command-line interface for a seamless user experience.

This project is built using various Python libraries, including yt-dlp for downloading YouTube media, the Google API for searching YouTube videos, and lyricsgenius for retrieving song lyrics from Genius.
Features

    Search and download YouTube videos in video or audio format.
    Download lyrics for your favorite songs.
    User-friendly command-line interface with clear instructions.
    Error handling for a smooth user experience.
    Modular and well-structured code for easy maintenance and customization.

Prerequisites

Before using this program, ensure you have the following prerequisites installed:

    Python 3.x: You can download it from the official website.

Installation

    Clone the repository to your local machine:

    bash





Navigate to the project directory:

bash

cd your-repo-name

Install the required Python packages:

bash

    pip install -r requirements.txt

Usage

    Run the program:

    bash

    python main.py

    You will be presented with the following options:
        Download (v)ideo
        Download (a)udio
        Download (l)yrics
        (exit) to quit

    Choose the option corresponding to what you want to download:
        For video or audio, you'll be prompted to enter a search query and then choose a video to download.
        For lyrics, you'll be prompted to enter the song title and artist name.

    Follow the on-screen instructions to complete the download.

Configuration

Before using the program, you need to configure your API keys for YouTube Data and Lyrics Genius. Follow these steps:

    Get a YouTube Data API Key:
        Visit the Google Developers Console.
        Create a new project or select an existing one.
        Enable the YouTube Data API v3 for your project.
        Create an API key.
        Replace YOUR_YOUTUBE_API_KEY in main.py with your API key.

    Get a Lyrics Genius API Token:
        Visit the Genius API page.
        Sign in or create an account.
        Create a new API client.
        Copy the access token.
        Replace YOUR_GENIUS_API_TOKEN in main.py with your access token.

Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Make your changes.
    Submit a pull request to the main branch of the original repository.
