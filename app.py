from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

 Configure your Gemini API key securely via environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("⚠️ GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

 Create Gemini model
model = genai.GenerativeModel("gemini-pro")

@app.route('/')
def index():
    return render_template("latest_email.html")

@app.route('/generate_reply', methods=['POST'])
def generate_reply():
    data = request.get_json()
    email_snippet = data.get("email_snippet", "")

    try:
        response = model.generate_content(f"Write a professional reply to this email:\n\n{email_snippet}")
        ai_reply = response.text
        return jsonify({"reply": ai_reply})
    except Exception as e:
        print("❌ Error generating reply:", e)
        return jsonify({"error": "AI generation failed."}), 500

if __name__ == "__main__":
    app.run(port=5001)
