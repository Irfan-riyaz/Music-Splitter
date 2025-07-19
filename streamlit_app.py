# streamlit_app.py
import subprocess
import os
import streamlit as st
from spleeter.separator import Separator

# Install FFmpeg and Spleeter (only required in environments that allow runtime install, e.g. Colab)
def install_dependencies():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True)
    except FileNotFoundError:
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"])
    try:
        import spleeter
    except ImportError:
        subprocess.run(["pip", "install", "spleeter"])

# Comment out in Hugging Face/production: used only for Colab
# install_dependencies()

st.title("🎵 Music Splitter")
st.write("Upload an MP3 or WAV file to extract vocals and instrumental parts using Spleeter")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded: {uploaded_file.name}")

    with st.spinner("Separating audio..."):
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(uploaded_file.name, 'output')

    base_name = os.path.splitext(uploaded_file.name)[0]
    vocals_path = f'output/{base_name}/vocals.wav'
    acc_path = f'output/{base_name}/accompaniment.wav'

    st.subheader("Download Results")
    with open(vocals_path, "rb") as f:
        st.download_button(label="⬇ Download Vocals", data=f, file_name="vocals.wav")

    with open(acc_path, "rb") as f:
        st.download_button(label="⬇ Download Instrumental", data=f, file_name="accompaniment.wav")

    st.audio(vocals_path, format="audio/wav", start_time=0)
    st.audio(acc_path, format="audio/wav", start_time=0)
