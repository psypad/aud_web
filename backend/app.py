from flask import Flask, jsonify, request, send_file, abort
from flask_cors import CORS
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

RECORDINGS_DIR = "recordings"
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

@app.route("/api/recordings", methods=["GET"])
def get_recordings():
    recordings = []
    for filename in os.listdir(RECORDINGS_DIR):
        if filename.endswith(".wav"):
            file_path = os.path.join(RECORDINGS_DIR, filename)
            recordings.append({
                "id": filename,
                "name": filename,
                "created_at": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
            })
    return jsonify(recordings)

@app.route("/api/recordings/<recording_id>", methods=["DELETE"])
def delete_recording(recording_id):
    file_path = os.path.join(RECORDINGS_DIR, recording_id)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "Recording deleted successfully"})
    abort(404)

@app.route("/api/recordings/<recording_id>", methods=["GET"])
def get_recording(recording_id):
    file_path = os.path.join(RECORDINGS_DIR, recording_id)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="audio/wav")
    abort(404)

@app.route("/api/record", methods=["POST"])
def start_recording():
    duration = request.json.get("duration", 5)  
    samplerate = 44100
    channels = 1
    
   
    filename = f"{uuid.uuid4()}.wav"
    file_path = os.path.join(RECORDINGS_DIR, filename)
    
 
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()  
    
    sf.write(file_path, recording, samplerate)
    
    return jsonify({
        "id": filename,
        "name": filename,
        "created_at": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)