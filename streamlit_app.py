import streamlit as st
from spleeter.separator import Separator
import os
import shutil
import uuid

st.set_page_config(page_title="Music Splitter", layout="centered")

st.title("🎵 Music Splitter using Spleeter")
st.write("Upload an audio file (MP3 or WAV), and this app will separate vocals and accompaniment using Spleeter.")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

if uploaded_file is not None:
    file_id = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", f"{file_id}_{uploaded_file.name}")
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Audio file uploaded successfully!")

    if st.button("🔀 Split Audio"):
        with st.spinner("⏳ Separating audio, please wait..."):
            output_dir = os.path.join("output", file_id)
            os.makedirs(output_dir, exist_ok=True)

            # Perform separation using Spleeter
            separator = Separator("spleeter:2stems")
            separator.separate_to_file(file_path, output_dir)

            # Locate result files
            split_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0])
            vocal_path = os.path.join(split_path, "vocals.wav")
            acc_path = os.path.join(split_path, "accompaniment.wav")

            if os.path.exists(vocal_path) and os.path.exists(acc_path):
                st.success("🎉 Audio split successfully!")

                st.subheader("🔊 Vocals")
                st.audio(vocal_path)

                st.subheader("🎶 Instrumental")
                st.audio(acc_path)
            else:
                st.error("❌ Error: Split files not found.")
