import streamlit as st
from pytube import YouTube
import os

# Create the 'downloads' folder if it doesn't exist
os.makedirs("downloads", exist_ok=True)

# Function to download YouTube video as audio
def download_youtube_audio(url, output_folder):
    try:
        # Get YouTube video
        yt = YouTube(url)

        # Download audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download audio file
        audio_stream.download(output_folder)

        # Get the downloaded audio file
        audio_file = os.path.join(output_folder, audio_stream.default_filename)

        # Rename the audio file with a .mp3 extension
        mp3_file = os.path.splitext(audio_file)[0] + ".mp3"
        os.rename(audio_file, mp3_file)

        return mp3_file

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit UI
st.title("YouTube Video to MP3 Downloader")

# Radio button for choosing between one or multiple videos
choice = st.radio("Choose:", ["Single", "Multiple"])

if choice == "Single":
    # Input URL for a single video
    url = st.text_input("Enter YouTube video URL:")

    if st.button("Download as MP3"):
        # Specify the output folder
        output_folder = "downloads"

        # Download and convert to MP3
        mp3_file = download_youtube_audio(url, output_folder)

        if mp3_file:
            # Provide download link
            st.success(f"Download successful! [Download MP3]({mp3_file})")
            st.audio(mp3_file, format='audio/mp3')

elif choice == "Multiple":
    # Input number of videos
    num_videos = st.number_input("Enter the number of YouTube videos:", 1, step=1)

    # Input URLs for multiple videos
    url_list = st.text_area("Enter YouTube video URLs (one URL per line):", height=200)

    if st.button("Download as MP3"):
        if url_list:
            # Convert input text area content to a list of URLs
            urls = url_list.split('\n')[:num_videos]

            # Specify the output folder
            output_folder = "downloads"

            # Process each URL
            for url in urls:
                url = url.strip()
                if url:
                    st.write(f"Processing: {url}")
                    mp3_file = download_youtube_audio(url, output_folder)
                    if mp3_file:
                        st.success(f"Download successful! [Download MP3]({mp3_file})")
                        st.audio(mp3_file, format='audio/mp3')
