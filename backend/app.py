from flask import Flask, request, jsonify  
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please ask a question!"})
    return jsonify({"answer": f"Dummy response to: {question}"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)