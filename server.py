from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

import os

from groq import Groq

def chatbot_response(request):

    client = Groq(api_key = "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")
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request,
            }            ],
        model="llama-3.3-70b-versatile",
    )
    return (chat_completion.choices[0].message.content)
        

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    bot_response = chatbot_response(user_input)
    return jsonify({"reply": bot_response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
