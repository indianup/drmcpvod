from flask import Flask, request, jsonify
import os
from services.drm_service import generate_drm_keys

app = Flask(__name__)

# Load the token from environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'default_token_if_not_set')

@app.route('/api', methods=['GET'])
def api():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL parameter is required"}), 400

    result = generate_drm_keys(video_url, ACCESS_TOKEN)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
