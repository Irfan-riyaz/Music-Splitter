
import os
import shutil
import tempfile
import zipfile
import subprocess
from pathlib import Path
import gradio as gr

def run_demucs(audio_path, model_name="htdemucs"):
    # Create temp workspace
    workdir = Path(tempfile.mkdtemp(prefix="demucs_"))
    input_path = workdir / Path(audio_path).name
    shutil.copy(audio_path, input_path)

    # Output directory for demucs
    out_dir = workdir / "separated"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Run Demucs CLI
    # Note: --jobs 1 to reduce RAM on small instances
    cmd = [
        "python", "-m", "demucs",
        "-n", model_name,
        "--jobs", "1",
        str(input_path),
        "--out", str(out_dir)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Surface helpful error to UI
        raise RuntimeError(f"Demucs failed.\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}")

    # Demucs writes to: out_dir / model_name / <track_name_without_ext>
    # Find the inner directory that contains stems
    model_dir = next((p for p in (out_dir / model_name).glob("*") if p.is_dir()), None)
    if model_dir is None:
        raise RuntimeError("Could not find Demucs output folder.")

    stems = {
        "vocals": model_dir / "vocals.wav",
        "drums": model_dir / "drums.wav",
        "bass": model_dir / "bass.wav",
        "other": model_dir / "other.wav",
    }

    missing = [k for k, v in stems.items() if not v.exists()]
    if missing:
        raise RuntimeError(f"Missing stems: {', '.join(missing)}. Check logs.")

    # Zip all stems for easy download
    zip_path = workdir / "stems.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, p in stems.items():
            zf.write(p, arcname=f"{name}.wav")

    # Return filepaths; Gradio will serve them
    return str(stems["vocals"]), str(stems["drums"]), str(stems["bass"]), str(stems["other"]), str(zip_path)

with gr.Blocks() as demo:
    gr.Markdown("# 🎧 4‑Stem Audio Splitter (Demucs)\nUpload a track and split into vocals, drums, bass, and other.")

    with gr.Row():
        audio = gr.Audio(label="Upload audio (mp3/wav/m4a)", type="filepath")
        model = gr.Dropdown(
            ["htdemucs", "mdx", "htdemucs_ft"],
            value="htdemucs",
            label="Model"
        )

    run_btn = gr.Button("🔀 Split Audio")
    with gr.Row():
        out_vocals = gr.Audio(label="Vocals", type="filepath")
        out_drums = gr.Audio(label="Drums", type="filepath")
        out_bass = gr.Audio(label="Bass", type="filepath")
        out_other = gr.Audio(label="Other", type="filepath")
    zip_file = gr.File(label="Download all stems (.zip)")

    run_btn.click(run_demucs, inputs=[audio, model], outputs=[out_vocals, out_drums, out_bass, out_other, zip_file])

if __name__ == "__main__":
    demo.queue(max_size=5).launch()
