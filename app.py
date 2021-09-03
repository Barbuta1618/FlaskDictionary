from flask import Flask, render_template, url_for, request
from flask.helpers import flash
from werkzeug.utils import redirect
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
SECRET_KEY = os.getenv('SECRET_KEY')


# returns a list with all languages
def getLanguages():
    with open("languages.txt", "r") as input:
        return input.read().split("\n")

languages = getLanguages()
lastWords = []


# database connection
try:
    db = DataBase.DataBase((DATABASE, USER, PASSWORD, HOST, PORT))
except:
    raise TypeError("Connection with database cannot be established!\nPlease make sure the .env file contains valid information!")


app = Flask(__name__)

app.config.update(
    SECRET_KEY = SECRET_KEY
)

@app.route('/', methods = ['GET', 'POST'])
def index():

    # GET METHOD
    if request.method == "GET": 
        return render_template('index.html', languages = languages, lastWords = lastWords)
    else:
    
    # POST METHOD

        # getting the data from the user
        lst = [request.form['firstWord'], request.form['firstLang'], request.form['secondWord'], request.form['secondLang']]
        
        errorCode = db.checkData(lst)
        if errorCode == 0:
            db.insert(lst)
            lastWords.append(lst) 

        elif errorCode == 1:
            flash('Please insert a valid word!')
            return redirect(url_for('index'))

        elif errorCode == 2:
            flash('The pair of words already exits!')
            return redirect(url_for('index'))

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

        if len(result) == 0:
            flash('No results found!')
            return redirect(url_for('search'))
        return render_template('search.html', languages = languages, result = result)


if __name__ == "__main__":
    app.run(debug=True)