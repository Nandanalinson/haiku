
from flask import Flask, render_template ,request,jsonify
import sqlite3
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

@app.route('/haikus')
def haikus():
    connect = sqlite3.connect('haikus.db')
    cur=connect.cursor()
    cur.execute("SELECT theme,haiku FROM haikus ")
    hai=cur.fetchall()
    return hai

@app.route("/generate-haiku", methods=['POST'])
def generate_haiku():

    data = request.get_json()


    print("Received data:", data)
    theme = data.get('theme',None)
    print("Received theme:", theme)

    connect = sqlite3.connect('haikus.db')
    cur=connect.cursor()
    


    cur.execute("CREATE TABLE IF NOT EXISTS haikus (id INTEGER PRIMARY KEY AUTOINCREMENT, theme TEXT , haiku TEXT)")
    add_theme = "INSERT INTO haikus (theme,haiku) VALUES (?, ?)"
   
    response = model.generate_content(f"Write a haiku about {theme}")
    themes = (theme,response.text)
    cur.execute(add_theme, themes)

    connect.commit()
    connect.close()
    return jsonify({"haiku": response.text})


if __name__== '__main__':
    app.run(debug=True)
