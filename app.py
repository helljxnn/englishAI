from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.gemini_client import GeminiClient

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize Gemini client
gemini_client = GeminiClient()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not gemini_client.is_configured():
        return jsonify({"error": "API Key not configured. Please check your .env file."}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response_text = gemini_client.generate_response(user_message)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error with Gemini model: {e}")
        return jsonify({"error": f"Model failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
