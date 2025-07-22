from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # NEW IMPORT
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API Key not found. Make sure it's in your .env file.")

genai.configure(api_key=api_key)

system_instruction = """
You are a Data Structure and Algorithm Instructor. You will only reply to problems related to
Data Structures and Algorithms. If users ask you irrelevant questions to data science and algorithms then reply rudely and more rudely.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

app = Flask(__name__)
CORS(app)  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    try:
        response = model.generate_content([user_input])
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"response": "An error occurred while processing your request."})

if __name__ == "__main__":
    app.run(debug=True)
