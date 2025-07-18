import streamlit as st
from spleeter.separator import Separator
import os
import tempfile

st.title("🎵 Music Splitter (Vocals & Instrumental)")

uploaded_file = st.file_uploader("Upload an audio file (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.success(f"Uploaded: {uploaded_file.name}")

    # Run Spleeter
    with st.spinner("Separating audio into vocals and accompaniment..."):
        separator = Separator('spleeter:2stems')
        separator.separate_to_file(tmp_path, 'output')

    # Get base name
    base_name = os.path.splitext(os.path.basename(tmp_path))[0]
    vocals_path = f'output/{base_name}/vocals.wav'
    accompaniment_path = f'output/{base_name}/accompaniment.wav'

    # Offer playback and download
    st.subheader("🎧 Vocals")
    st.audio(vocals_path)
    with open(vocals_path, "rb") as f:
        st.download_button("Download Vocals", f, file_name="vocals.wav")

    st.subheader("🎸 Instrumental")
    st.audio(accompaniment_path)
    with open(accompaniment_path, "rb") as f:
        st.download_button("Download Instrumental", f, file_name="accompaniment.wav")
