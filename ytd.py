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
    return trimmed_video_path

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

        if st.button("Trim and Download"):
            if youtube_url and full_video_path is None:
                output_path = output_folder
                full_video_path, _ = download_video(youtube_url, output_path)

            trimmed_video_path = trim_video(full_video_path, start_time, end_time)
            st.success("Your Trimmed Video is here, click on three dots to download or else find it at: {}".format(trimmed_video_path))
            st.video(trimmed_video_path)
    st.text("Made with ❤️ by Sagnik")

if __name__ == "__main__":
    main()
