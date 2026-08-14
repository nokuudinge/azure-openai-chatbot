from flask import Flask, jsonify  # pyright: ignore[reportMissingImports]

app = Flask(__name__)

@app.route('/query', methods=['GET'])
def query():
    response = {"response": "Hello from Azure OpenAI Chatbot backend"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8080)