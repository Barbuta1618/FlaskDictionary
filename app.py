from flask import Flask, render_template, url_for, request
from flask.helpers import flash
from werkzeug.utils import redirect
import DataBase
import os
from dotenv import load_dotenv


# env variables for database connection
load_dotenv()
lastWords = []


# database connection
db = DataBase.DataBase()
languages = db.getLanguages()

app = Flask(__name__)


SECRET_KEY = os.getenv('SECRET_KEY')
app.config.update(
    SECRET_KEY = SECRET_KEY
)

@app.route('/', methods = ['GET', 'POST'])
def index():

    languages = db.getLanguages()
    # GET METHOD
    if request.method == "POST":
        # getting data from user

        lst = ["", "", "", ""]
        try:
            lst = [request.form['firstWord'], request.form['firstLang'], request.form['secondWord'], request.form['secondLang']]
        except Exception as e:
            print(e)
        
        
        errorCode = db.checkData(lst)
        if errorCode == 0:
            db.insertWords(lst)
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

    languages = db.getLanguages()
    result = ""
    # GET METHOD
    if request.method == "POST":
        lst = [request.form['word'], request.form['language1'], request.form['language2']]
        result = db.searchWord(lst)

        if len(result) == 0:
            flash('No results found!')
            return redirect(url_for('search'))

    return render_template('search.html', languages = languages, result = result)


@app.route('/dictionary', methods = ['GET', 'POST'])
def dictionary():

    languages = db.getLanguages()
    results = list()
    lst = ["", ""]
    if request.method == "POST":
        try:
            lst = [request.form['lang1'], request.form['lang2']]
        except Exception as e:
            print(e)
        results = db.getDictionary(lst)
        if len(results) == 0:
            flash('No results found!')
            return redirect(url_for('dictionary'))
        

    return render_template('dictionary.html', languages = languages, result = results, language1 = lst[0], language2 = lst[1])

if __name__ == "__main__":
    app.run(debug=True)