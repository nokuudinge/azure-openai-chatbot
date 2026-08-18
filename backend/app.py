import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI

load_dotenv()

missing = [name for name in ("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT") if not os.getenv(name)]
if missing:
    print(f"Missing settings in backend/.env: {', '.join(missing)} — see the README for setup.")
    raise SystemExit(1)

AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-06-01",
)

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please ask a question!"})

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception:
        app.logger.exception("Azure OpenAI request failed")
        return jsonify({"answer": "Sorry, something went wrong. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
