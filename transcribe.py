import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def download_audio(url: str, output_path: str = "audio.mp3") -> str:
    print(f"[1/3] Downloading audio from: {url}")
    result = subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_path, url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    print("[1/3] Download complete.")
    return output_path


def transcribe(audio_path: str, model_size: str = "large-v3-turbo", language: str = "ja") -> list:
    print(f"[2/3] Loading model: {model_size}")
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"[2/3] Transcribing: {audio_path}")
    segments, info = model.transcribe(audio_path, language=language)
    texts = []
    for seg in segments:
        line = f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text.strip()}"
        print(line)
        texts.append(line)
    return texts


def save_output(texts: list, url: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"transcript_{timestamp}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write("-" * 60 + "\n\n")
        for line in texts:
            f.write(line + "\n")

    print(f"[3/3] Saved: {output_file}")
    return str(output_file)


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <YouTube URL>")
        print("Example: python transcribe.py https://www.youtube.com/watch?v=XXXX")
        sys.exit(1)

    url = sys.argv[1]
    audio_path = "audio.mp3"

    download_audio(url, audio_path)
    texts = transcribe(audio_path)
    save_output(texts, url)

    # 音声ファイル削除
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print("Cleaned up audio file.")


if __name__ == "__main__":
    main()
