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


def transcribe(audio_path: str, model_size: str = "small", language: str = "ja") -> list:
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
    import argparse
    parser = argparse.ArgumentParser(description="YouTube音声文字起こしツール")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--model", default="base",
                        help="Whisperモデルサイズ (default: base) "
                             "例: tiny, base, small, medium, large-v3-turbo")
    args = parser.parse_args()

    audio_path = "audio.mp3"

    download_audio(args.url, audio_path)
    texts = transcribe(audio_path, model_size=args.model)
    save_output(texts, args.url)

    # 音声ファイル削除
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print("Cleaned up audio file.")


if __name__ == "__main__":
    main()
