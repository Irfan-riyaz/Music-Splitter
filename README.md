
# 🎧 4‑Stem Audio Splitter (Demucs) — Hugging Face Space

This Space uses **Demucs** to split audio into **vocals, drums, bass, other** via a simple **Gradio** UI.

## Files
- `app.py` — Gradio app entry (Space SDK: **Gradio**)
- `requirements.txt` — Python deps (includes torch, demucs)
- `apt.txt` — System deps (installs `ffmpeg` in the Space)
- `README.md` — This file

##
Working link - https://huggingface.co/spaces/irfanriyas/Music-Splitter

## Notes
- Hardware: **CPU Basic** works but is slower; upgrade hardware for speed.
- Large files may take time; keep inputs short (≤ 20–30s) on free CPU for responsiveness.
