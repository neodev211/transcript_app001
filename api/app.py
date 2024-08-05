from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

app = Flask(__name__)

def get_video_id(url):
    # Extraer el ID del video de la URL de YouTube
    video_id = re.findall(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id[0] if video_id else None

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No se proporcionó URL"}), 400

    video_id = get_video_id(url)
    if not video_id:
        return jsonify({"error": "URL de YouTube inválida"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return jsonify({"transcription": full_transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)