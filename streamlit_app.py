# Install dependencies (if using in Colab, uncomment these lines)
# !apt-get install -y ffmpeg
# !pip install spleeter

from google.colab import files
from spleeter.separator import Separator
import os
from IPython.display import Audio

# Upload an audio file
print("Please upload an audio file (MP3 or WAV)")
uploaded = files.upload()

filename = list(uploaded.keys())[0]
print(f"File uploaded: {filename}")

# Separate vocals and accompaniment
separator = Separator('spleeter:2stems')
separator.separate_to_file(filename, 'output')
print("Separation Complete!")

# Prepare download links
base_name = os.path.splitext(filename)[0]
vocals_path = f'output/{base_name}/vocals.wav'
accompaniment_path = f'output/{base_name}/accompaniment.wav'

print("⬇ Preparing downloads...")
files.download(vocals_path)
files.download(accompaniment_path)

# Play back results
print("🎧 Vocals:")
display(Audio(vocals_path))

print("🎸 Instrumental:")
display(Audio(accompaniment_path))
