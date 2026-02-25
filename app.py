from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    chat_history = data.get("history", [])

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history
        )

        ai_reply = completion.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        ai_reply = str(e)

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run()