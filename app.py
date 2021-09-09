from flask import Flask, render_template, url_for, request
from flask_cors import CORS, cross_origin
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

# allowing cross origin requests
CORS(app)
cors = CORS(app, resources={r"/update": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


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
        
        if lst[1] == lst[3]:
            flash('The languages cannot be the same!')
            return redirect(url_for('index'))
        
        errorCode = db.checkData(lst)
        if errorCode == 0:
            db.insertWords(lst)
            lastWords.append(lst)

        elif errorCode == 1:
            flash('Please insert a valid word!')
            return redirect(url_for('index'))

        elif errorCode == 2:
            flash('The pair of words already exists!')
            return redirect(url_for('index'))

    return render_template('index.html', languages = languages, lastWords = lastWords)


@app.route('/search', methods = ['GET', 'POST'])
def search():

    languages = db.getLanguages()
    result = ""
    # GET METHOD
    if request.method == "POST":
        lst = [request.form['word'], request.form['language1'], request.form['language2']]

        if lst[1] == lst[2]:
            flash('The languages cannot be the same!')
            return redirect(url_for('search'))
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

        if lst[1] == lst[0]:
            flash('The languages cannot be the same!')
            return redirect(url_for('dictionary'))
        results = db.getDictionary(lst)
        if db.cursor.rowcount == 0:
            flash('No results found!')
            return redirect(url_for('dictionary'))
        
    return render_template('dictionary.html', languages = languages, result = results, language1 = lst[0], language2 = lst[1])


@app.route('/update', methods = ['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def update():
    languages = db.getLanguages()
    error = 1

    if request.method == "POST":
        try:
            data = request.get_json()
            old_pair = [data['old_word1'], data['old_lang1'], data['old_word2'], data['old_lang2']]
            new_pair = [data['new_word1'], data['new_lang1'], data['new_word2'], data['new_lang2']]

            
            error_new_pair = db.checkData(new_pair)
            if db.checkData(old_pair) == 0:
                flash('The pair of words doesn t exist!')
                return redirect(url_for('update'))
            elif error_new_pair == 1:
                flash('Please insert a valid word!')
                return redirect(url_for('update'))
            elif error_new_pair == 2:
                flash('The pair of words already exists!')
                return redirect(url_for('update'))
            else:
                error = db.update(old_pair, new_pair)
        except Exception as e:
            print(e)

    return render_template('update.html', languages = languages, error = error)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    languages = db.getLanguages()
    error = 1

    if request.method == 'POST':
        try:
            error = db.deleteLanguage(request.form['language'])
            languages = db.getLanguages()
        except Exception as e:
            print(e)

    return render_template('delete.html', languages = languages, error = error)

@app.route('/add', methods = ['GET', 'POST'])
def addLang():
    languages = db.getLanguages()
    error = 1
    if request.method == 'POST':
        language = request.form['language'].upper()
        if db.insertLanguage(language) == 1:
            flash('The language already exists!')
            return redirect(url_for('addLang'))
        else:
            error = 0

    return render_template('add.html', languages = languages, error = error)

@app.route('/word', methods = ['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def word():

    # searching in database for update page
    data = request.get_json()
    word1 = data['word1']
    word2 = data['word2']
    lang1 = data['lang1']
    lang2 = data['lang2']

    if lang1 != "" and lang2 != "":
        if word1 != "" and word2 == "":

            pair = db.searchWord((word1, lang1, lang2))
            if db.cursor.rowcount != 0:
                if word1 == pair[0][2]:
                    word2 = pair[0][0]
                else:
                    word2 = pair[0][2]

        if word2 != "" and word1 == "":
            pair = db.searchWord((word2, lang2, lang1))
            if db.cursor.rowcount != 0:
                if word2 == pair[0][0]:
                    word1 = pair[0][2]
                else:
                    word1 = pair[0][0]

    return {'word1' : word1, 'word2' : word2}


if __name__ == "__main__":
    app.run(debug=True)