# yt-transcribe

yt-dlpとfaster-whisperを使ったYouTube音声文字起こしツール

## 使い方

```bash
# 基本（モデル: base）
python transcribe.py https://www.youtube.com/watch?v=XXXX

# モデル指定
python transcribe.py https://www.youtube.com/watch?v=XXXX --model large-v3-turbo
```

## モデル一覧

| モデル | 速度 | 精度 |
|--------|------|------|
| tiny | 最速 | 低 |
| base | 速い | 普通（デフォルト） |
| small | 普通 | 良 |
| medium | 遅い | 高 |
| large-v3-turbo | 遅い | 最高 |

## セットアップ

```bash
pip install -r requirements.txt
```

## ⚠️ 注意
本ツールは個人学習・研究目的で作成しています。
著作権コンテンツのダウンロードはYouTube利用規約に違反する可能性があります。
権利クリアなコンテンツへの使用を推奨します。
