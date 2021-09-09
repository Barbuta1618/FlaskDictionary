
function makeQuery(word1, word2, lang1, lang2){
    return "?word1=" + word1 + "&word2=" + word2 + "&lang1=" + lang1 + "&lang2=" + lang2;
}

var URL_API = "http://localhost:5000/word";
var last_data = null

async function checkWord(){
    
    var lang1 = document.getElementById('firstLang').value;
    var lang2 = document.getElementById('secondLang').value;
    var word1 = document.getElementById('firstWord').value;
    var word2 = document.getElementById('secondWord').value;
    
    if(word1 == "" || word2 == ""){
        const response = await fetch(URL_API + makeQuery(word1, word2, lang1, lang2));
        const data = await response.json();
        last_data = {
            lang1: lang1,
            lang2: lang2,
            word1: data.word1,
            word2: data.word2
        }

        if(word1 == "" && word2 != ""){
            document.getElementById('firstWord').value = data.word1;
        }else{
            if(word2 == "" && word1 != ""){
                document.getElementById('secondWord').value = data.word2;
            }
        }
    }
}

function sendData(){

    var lang1 = document.getElementById('firstLang').value;
    var lang2 = document.getElementById('secondLang').value;
    var word1 = document.getElementById('firstWord').value;
    var word2 = document.getElementById('secondWord').value;

    
    $.ajax({
        url: '/update',
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            old_word1: last_data.word1,
            old_lang1: last_data.lang1,
            old_word2: last_data.word2,
            old_lang2: last_data.lang2,
            new_word1: word1,
            new_lang1: lang1,
            new_word2: word2,
            new_lang2: lang2
        }),

        success: function (data) {
            if (data.success){
                location.reload()
            }
        }
    });
}

function checkLanguages() {

    var lang1Input = document.getElementById('firstLang');
    var lang2Input = document.getElementById('secondLang');
    var lang1 = lang1Input.value;
    var lang2 = lang2Input.value;

    if(lang1 == '0' || lang2 == '0'){
        window.location.replace('/add')
    }
    
    if(lang1 == lang2 && lang1 != ""){
        lang1Input.style.backgroundColor = 'red';
        lang2Input.style.backgroundColor = 'red';
        document.getElementById('submit').disabled = true;
        return false;
    }else{
        lang1Input.style.backgroundColor = '';
        lang2Input.style.backgroundColor = '';
        document.getElementById('submit').disabled = false;
    }

}

function checkLanguage(){

    language = document.getElementById('language').value
    if(language == '0'){
        window.location.replace('/add')
    }
}


