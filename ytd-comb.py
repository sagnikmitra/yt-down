import streamlit as st
from pytube import YouTube
import os
import requests
from PIL import Image
from io import BytesIO

# Specify the full path for the 'downloads' folder
downloads_folder = os.path.join(os.getcwd(), "downloads")
os.makedirs(downloads_folder, exist_ok=True)

def download_youtube_audio(url, output_folder):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_folder)

        mp3_file = os.path.splitext(audio_file)[0] + ".mp3"

        if os.path.exists(mp3_file):
            base, ext = os.path.splitext(mp3_file)
            counter = 1
            while os.path.exists(f"{base}_{counter}{ext}"):
                counter += 1
            mp3_file = f"{base}_{counter}{ext}"

        os.rename(audio_file, mp3_file)

        return mp3_file
    except Exception as e:
        st.error(f"Error downloading audio: {str(e)}")
        return None

def download_youtube_thumbnail(url, output_folder):
    try:
        yt = YouTube(url)
        thumbnail_url = yt.thumbnail_url
        thumbnail_data = requests.get(thumbnail_url).content
        thumbnail_path = os.path.join(output_folder, f"{yt.title}_thumbnail.jpg")

        with open(thumbnail_path, "wb") as thumbnail_file:
            thumbnail_file.write(thumbnail_data)

        return thumbnail_path
    except Exception as e:
        st.error(f"Error downloading thumbnail: {str(e)}")
        return None

# Streamlit UI
st.title("YouTube Downloader")

url = st.text_input("Enter YouTube video URL:")
download_type = st.radio("Choose Download Type:", ["Full Video", "MP3", "Thumbnail"])

if st.button("Download"):
    if download_type == "Full Video":
        try:
            yt = YouTube(url)
            video_stream = yt.streams.get_highest_resolution()
            video_path = video_stream.download(downloads_folder)
            st.success(f"Download successful! [Download Video]({video_path})")
            st.video(video_path)
        except Exception as e:
            st.error(f"Error downloading full video: {str(e)}")
    elif download_type == "MP3":
        mp3_file = download_youtube_audio(url, downloads_folder)
        if mp3_file:
            st.success(f"Download successful! [Download MP3]({mp3_file})")
            st.audio(mp3_file, format='audio/mp3')
    elif download_type == "Thumbnail":
        thumbnail_path = download_youtube_thumbnail(url, downloads_folder)
        if thumbnail_path:
            thumbnail_image = Image.open(thumbnail_path)
            st.success("Download successful! Thumbnail:")
            st.image(thumbnail_image)

