FROM python:3.11-slim

# ffmpeg インストール
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存パッケージ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトコピー
COPY transcribe.py .

# 出力ディレクトリ
RUN mkdir -p /app/output
VOLUME ["/app/output"]

ENTRYPOINT ["python", "transcribe.py"]
