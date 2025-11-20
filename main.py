from flask import Flask, render_template ,request,jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI API KEY')

genai.configure(api_key=GEMINI_API_KEY)

model=genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/generate-haiku", methods=['POST'])
def generate_haiku():

    data = request.get_json()


    print("Received data:", data)
    theme = data.get('theme',None)
    print("Received theme:", theme)
    response = model.generate_content(f"Write a haiku about {theme}")
    return jsonify({"haiku": response.text})





if __name__== '__main__':
    app.run(debug=True)
