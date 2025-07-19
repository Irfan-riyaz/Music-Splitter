import os
import streamlit as st
from spleeter.separator import Separator
import tempfile

st.set_page_config(page_title="🎵 Music Splitter", layout="centered")
st.title("🎵 Music Splitter")
st.markdown("Upload an audio file (MP3/WAV) and split it into vocals and accompaniment using Spleeter.")

# Create temp directory for output
output_dir = tempfile.mkdtemp()

uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input.flush()

        if st.button("🔊 Split Audio"):
            with st.spinner("Processing... this may take a minute ⏳"):
                separator = Separator('spleeter:2stems')
                separator.separate_to_file(tmp_input.name, output_dir)

                # Extract base name
                base_name = os.path.splitext(os.path.basename(tmp_input.name))[0]
                result_path = os.path.join(output_dir, base_name)

                vocals_path = os.path.join(result_path, "vocals.wav")
                accompaniment_path = os.path.join(result_path, "accompaniment.wav")

                st.success("Audio successfully split! 🎉")

                st.audio(vocals_path, format='audio/wav', start_time=0)
                st.markdown("⬆️ Vocals")

                st.audio(accompaniment_path, format='audio/wav', start_time=0)
                st.markdown("⬆️ Accompaniment")

                st.markdown("🎧 Enjoy your separated tracks!")
