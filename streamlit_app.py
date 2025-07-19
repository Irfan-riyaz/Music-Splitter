
import streamlit as st
from spleeter.separator import Separator
import os
import tempfile
import shutil

st.set_page_config(page_title="🎵 Music Splitter", layout="centered")
st.title("🎵 Music Splitter")
st.write("Upload an audio file (MP3 or WAV) to split it into vocals and accompaniment using Spleeter.")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("Processing audio file... This may take a minute.")

        separator = Separator("spleeter:2stems")
        separator.separate_to_file(input_path, tmpdir)

        stem_dir = os.path.join(tmpdir, os.path.splitext(uploaded_file.name)[0])
        vocals_path = os.path.join(stem_dir, "vocals.wav")
        accompaniment_path = os.path.join(stem_dir, "accompaniment.wav")

        if os.path.exists(vocals_path) and os.path.exists(accompaniment_path):
            st.success("Audio split successfully!")
            st.audio(vocals_path, format="audio/wav", start_time=0)
            st.audio(accompaniment_path, format="audio/wav", start_time=0)
        else:
            st.error("Failed to process audio file.")
