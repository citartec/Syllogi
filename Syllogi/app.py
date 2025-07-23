from flask import Flask, render_template, request, redirect, url_for, abort
import subprocess
from pathlib import Path
import shutil
import logging

# Configuration
app = Flask(__name__)
DOWNLOAD_FOLDER = Path(__file__).parent / "static" / "downloads"
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            try:
                logging.info(f"Starting download: {url}")
                subprocess.run([
                    "yt-dlp",
                    "-f", "bv*+ba/b",
                    "--merge-output-format", "mp4",
                    "-o", "%(title)s.%(ext)s",
                    url
                ], cwd=DOWNLOAD_FOLDER, check=True)
                logging.info("Download completed.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Download failed: {e}")
        return redirect(url_for("index"))

    # Get downloaded video files sorted by newest first
    video_files = sorted(
        [f for f in DOWNLOAD_FOLDER.glob("*") if f.is_file()],
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    return render_template("index.html", videos=video_files)

@app.route("/reveal/<path:filename>")
def reveal_in_folder(filename):
    try:
        # Normalize and secure the path
        safe_path = (DOWNLOAD_FOLDER / filename).resolve()

        if not str(safe_path).startswith(str(DOWNLOAD_FOLDER)):
            logging.warning("Attempted directory traversal")
            abort(403)

        if not safe_path.exists():
            logging.warning(f"File not found: {safe_path}")
            abort(404)

        logging.info(f"Revealing file in folder: {safe_path}")

        # Try common Linux file managers
        if shutil.which("nautilus"):
            subprocess.run(["nautilus", "--select", str(safe_path)])
        elif shutil.which("dolphin"):
            subprocess.run(["dolphin", "--select", str(safe_path)])
        elif shutil.which("thunar"):
            subprocess.run(["thunar", str(safe_path.parent)])
        else:
            subprocess.run(["xdg-open", str(safe_path.parent)])

    except Exception as e:
        logging.error(f"Error opening folder: {e}")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

