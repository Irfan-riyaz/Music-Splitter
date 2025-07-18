import streamlit as st
from spleeter.separator import Separator
import os
import tempfile
import shutil

st.set_page_config(page_title="Music Splitter", layout="centered")
st.title("🎶 Music Splitter: Vocal & Instrumental Separator")

st.markdown("""
Upload an audio file (MP3 or WAV). This app will use [Spleeter](https://github.com/deezer/spleeter) to separate it into:
- 🎤 Vocals
- 🎸 Instrumental
""")

# Upload audio file
uploaded_file = st.file_uploader("📤 Upload Audio File", type=["mp3", "wav"])

if uploaded_file is not None:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        input_audio_path = tmp_file.name

    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Separator
    st.info("🔄 Separating audio... please wait")
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(input_audio_path, 'output')

    # Get output paths
    base_name = os.path.splitext(os.path.basename(input_audio_path))[0]
    output_dir = os.path.join("output", base_name)
    vocals_path = os.path.join(output_dir, "vocals.wav")
    instrumental_path = os.path.join(output_dir, "accompaniment.wav")

    st.success("✅ Separation Complete!")

    # Playback and download
    st.subheader("🎤 Vocals")
    st.audio(vocals_path)
    with open(vocals_path, "rb") as f:
        st.download_button("⬇ Download Vocals", f, file_name="vocals.wav")

    st.subheader("🎸 Instrumental")
    st.audio(instrumental_path)
    with open(instrumental_path, "rb") as f:
        st.download_button("⬇ Download Instrumental", f, file_name="instrumental.wav")
