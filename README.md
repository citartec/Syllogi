# 🎥 Flask YouTube Downloader (Linux Optimized)

A local web app built with Flask that lets you:

- Paste YouTube or video URLs
- Download high-quality videos using `yt-dlp`
- Display downloaded videos in-browser
- 🔍 Reveal the downloaded file in your Linux file manager (Nautilus, Dolphin, etc.)

---

## 🚀 Features

- Format: `bv*+ba/b` (best video + best audio, fallback to best available)
- Auto-merges video/audio to `.mp4`
- Responsive HTML UI with dark mode
- Works entirely offline/local (no internet needed except for downloading videos)
- Button to show file in folder

---

## 📦 Requirements

- Python 3.7+
- Linux OS (Ubuntu, Arch, Fedora, etc.)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ffmpeg (for merging video/audio)
- Flask

### 🧰 Install Dependencies

```bash
sudo apt update
sudo apt install ffmpeg
pip install flask yt-dlp


http://127.0.0.1:5000
