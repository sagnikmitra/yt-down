import streamlit as st
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

def download_video(url, output_path):
    yt = YouTube(url)
    video_stream = yt.streams.get_highest_resolution()
    video_path = video_stream.download(output_path)
    return video_path, yt.length

def trim_video(video_path, start_time, end_time):
    video_clip = VideoFileClip(video_path).subclip(start_time, end_time)
    trimmed_video_path = video_path.replace(".mp4", "_trimmed.mp4")
    video_clip.write_videofile(trimmed_video_path, codec="libx264", audio_codec="aac", temp_audiofile="temp_audio.m4a", remove_temp=True)
    return trimmed_video_path, video_clip.duration

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds)}"

def main():
    st.title("YouTube Video Trimmer and Downloader")

    youtube_url = st.text_input("Enter YouTube Video URL:")
    output_folder = "./output"
    full_video_path = None

    if youtube_url:
        st.subheader("YouTube Video Preview:")
        st.video(youtube_url)
        try:
            yt = YouTube(youtube_url)
            video_duration = yt.length
            st.info(f"Video Duration: {format_time(video_duration)} seconds")
        except:
            st.warning("Unable to fetch video duration. Please check the URL.")

        st.subheader("Trimming Section:")
        start_time = st.slider("Start Time (seconds)", 0, video_duration, 0, key="trim_start_slider")
        st.text(f"Selected Start Time: {format_time(start_time)}")
        end_time = st.slider("End Time (seconds)", 0, video_duration, video_duration, key="trim_end_slider")
        st.text(f"Selected End Time: {format_time(end_time)}")
        if start_time >= end_time:
            st.warning("Start time must be before end time.")
        total_length = end_time - start_time
        st.info(f"Total Length of Trimmed Video: {format_time(total_length)} seconds")
        if st.button("Trim and Download"):
            if youtube_url and full_video_path is None:
                output_path = output_folder
                full_video_path, _ = download_video(youtube_url, output_path)

            trimmed_video_path, trimmed_video_duration = trim_video(full_video_path, start_time, end_time)
            st.success("Your Trimmed Video is here, click on three dots to download or else find it at: {}".format(trimmed_video_path))
            st.video(trimmed_video_path)
            
            
    
    st.text("Made with ❤️ by Sagnik")

if __name__ == "__main__":
    main()
    
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
st.title("YouTube Video/MP3/Thumbnail Downloader")

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

