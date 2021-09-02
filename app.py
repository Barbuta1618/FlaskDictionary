from flask import Flask, render_template, url_for, request
import DataBase
import os
from dotenv import load_dotenv


# env variables for database connection
load_dotenv()
DATABASE = os.getenv('DATABASE')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


# returns a list with all languages
def getLanguages():
    with open("languages.txt", "r") as input:
        return input.read().split("\n")

languages = getLanguages()
lastWords = []


# database connection
db = DataBase.DataBase((DATABASE, USER, PASSWORD, HOST, PORT))

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():

    # GET METHOD
    if request.method == "GET": 
        return render_template('index.html', languages = languages, lastWords = lastWords)
    else:
    
    # POST METHOD

        # getting the data from the user
        lst = [request.form['firstWord'], request.form['firstLang'], request.form['secondWord'], request.form['secondLang']]
        
        if db.checkData(lst) == 0:
            db.insert(lst)
            lastWords.append(lst)

        return render_template('index.html', languages = languages, lastWords = lastWords)


@app.route('/search', methods = ['GET', 'POST'])
def search():

    result = ""
    # GET METHOD
    if request.method == "GET":
        return render_template('search.html', languages = languages, result = result)
    else:
        lst = [request.form['word'], request.form['language1'], request.form['language2']]
        result = db.searchWord(lst)

        return render_template('search.html', languages = languages, result = result)


if __name__ == "__main__":
    app.run(debug=True)