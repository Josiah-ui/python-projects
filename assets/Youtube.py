import yt_dlp  

url = input("Enter the YouTube video URL: ")

yt_dlp_options = {"format": "bestvideo+bestaudio/best"}
with yt_dlp.YoutubeDL(yt_dlp_options) as downloader:
    downloader.download([url])