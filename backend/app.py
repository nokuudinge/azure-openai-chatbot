import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = None
if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY and AZURE_OPENAI_DEPLOYMENT:
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-06-01",
    )

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please ask a question!"})

    if client is None:
        return jsonify({"answer": f"Dummy response to: {question} (Azure OpenAI is not configured — check backend/.env)"})

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": f"Error talking to Azure OpenAI: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
