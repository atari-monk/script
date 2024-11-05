import os
import yt_dlp

from base.base_command import BaseCommand

class Mp3Command(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        if len(args) != 1:
            print("Error: One argument required - video_url.")
            return

        video_url = args[0]  # Use the first argument as the video URL

        try:
            if not self.is_valid_video_url(video_url):
                print("Invalid video URL format. URL must be a valid YouTube link.")
                return
        except ValueError as e:
            print(f"Error: {e}.")

        self.download_youtube_as_mp3(video_url)

    @property
    def description(self):
        return "Download video as mp3."

    def is_valid_video_url(self, video_url):
        # Implement a simple validation for YouTube URLs
        return isinstance(video_url, str) and ("youtube.com/watch?v=" in video_url or "youtu.be/" in video_url)

    def download_youtube_as_mp3(self, video_url, output_folder=r"C:/atari-monk/downloads/mp3"):
        try:
            # Create output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # yt-dlp options to download audio and convert to mp3
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            print("Download and conversion to MP3 completed.")
        
        except Exception as e:
            print(f"Error: {str(e)}")
