import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from gtts import gTTS
from shutil import copyfile

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["AUDIO_FOLDER"] = "static/audio"

# Make sure folders exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["AUDIO_FOLDER"], exist_ok=True)
os.makedirs("static/db_police", exist_ok=True)
os.makedirs("static/db_hospital", exist_ok=True)
os.makedirs("static/db_cctv", exist_ok=True)
os.makedirs("static/db_morgue", exist_ok=True)
os.makedirs("static/db_future", exist_ok=True)

# Stage order (name, folder)
DB_STAGES = [
    ("Stage 1 — Police Database", "static/db_police"),
    ("Stage 2 — Hospital Database", "static/db_hospital"),
    ("Stage 3 — CCTV Database", "static/db_cctv"),
    ("Stage 4 — Morgue Database", "static/db_morgue"),
]

def generate_voice(text):
    """Generate voice file for browser playback, returns web path"""
    try:
        audio_path = os.path.join(app.config["AUDIO_FOLDER"], "voice.mp3")
        tts = gTTS(text)
        tts.save(audio_path)
        return "/static/audio/voice.mp3"
    except Exception:
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Get form fields
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    last_seen = request.form.get("last_seen", "").strip()

    file = request.files.get("photo")
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    if filename == "":
        return "Invalid filename", 400

    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(upload_path)

    logs = []
    matched_stage = None
    matched_file = None
    match_info = None

    # Stage-by-stage simple filename matching
    for stage_name, stage_folder in DB_STAGES:
        logs.append(f"Checking {stage_name}...")
        # Check files in folder for exact filename match
        for f in os.listdir(stage_folder):
            if f == filename:
                matched_stage = stage_name
                matched_file = f
                logs.append(f"Result: Found ({f})")
                break
        if matched_stage:
            break
        else:
            logs.append("Result: Not found in this stage")

    if matched_stage:
        match_info = f"Found at {matched_stage} (file: {matched_file})"
    else:
        # Save to future DB (copy from uploads)
        try:
            future_path = os.path.join("static/db_future", filename)
            copyfile(upload_path, future_path)
            logs.append("Saved uploaded file to future database for later comparison.")
        except Exception as e:
            logs.append(f"Failed to save to future db: {e}")
        match_info = "No match found in any database. Saved for future comparison."

    # Create voice text and generate audio for browser playback
    voice_text = match_info
    if name:
        voice_text = f"{voice_text} Name: {name}. Age: {age or 'unknown'}."
    audio_web = generate_voice(voice_text)
    if audio_web:
        logs.append("Voice output generated.")
    else:
        logs.append("Voice generation failed or skipped.")

    return render_template(
        "result.html",
        name=name,
        age=age,
        last_seen=last_seen,
        uploaded_image=f"/static/uploads/{filename}",
        matched_stage=matched_stage,
        match_info=match_info,
        logs=logs,
        audio_web_path=audio_web
    )

if __name__ == "__main__":
    app.run(debug=True)