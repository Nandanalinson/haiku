
from flask import Flask, render_template ,request,jsonify
import psycopg2
'''import sqlite3'''
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


@app.route('/api/haikus', methods=['GET'])
def haikus():
    '''connect = sqlite3.connect('haikus.db')
    cur = connect.cursor()
    cur.execute("SELECT theme, haiku FROM haikus")
    data = cur.fetchall()

    replaced_data = []

    for theme, haiku in data:
        clean_theme = theme.replace(',', ':')
        replaced_data.append(f"Theme: {clean_theme}\n{haiku}\n")

    replaced_data_str = '\n'.join(replaced_data)

    print("data", replaced_data_str)

    return jsonify({"haiku": replaced_data_str})'''
    connect = psycopg2.connect(database="haiku", 
                        user="myuser",
                        password="mypassword", 
                        host="localhost", port="5433")

    cur = connect.cursor()
    cur.execute("SELECT theme, haiku FROM haikus")

    data = cur.fetchall()
    replaced_data = []
    #replaced

    for theme, haiku in data:
        clean_theme = theme.replace(',', ':')
        replaced_data.append(f"Theme: {clean_theme}\n{haiku}\n")

    replaced_data_str = '\n'.join(replaced_data)

    print("data", replaced_data_str)

    return jsonify({"haiku": replaced_data_str})


@app.route('/haikus')
def haikus_page():
    return render_template('haikus.html')

@app.route("/generate-haiku", methods=['POST'])
def generate_haiku():

    data = request.get_json()


    print("Received data:", data)
    theme = data.get('theme',None)
    print("Received theme:", theme)

    connect = psycopg2.connect(database="haiku", 
                        user="myuser",
                        password="mypassword", 
                        host="localhost", port="5433")
    cur=connect.cursor()
    


    cur.execute("CREATE TABLE IF NOT EXISTS haikus (id SERIAL PRIMARY KEY, theme TEXT , haiku TEXT)")
    add_theme = "INSERT INTO haikus (theme, haiku) VALUES (%s, %s)"
   
    response = model.generate_content(f"Write a haiku about {theme}")
    themes = (theme,response.text)
    cur.execute(add_theme, themes)

    connect.commit()
    connect.close()
    return jsonify({"haiku": response.text})


if __name__== '__main__':
    app.run(debug=True)
