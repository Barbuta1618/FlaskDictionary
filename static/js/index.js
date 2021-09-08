
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
        
        if(word1 == "" && word2 != ""){
            document.getElementById('firstWord').value = data.word1;
        }else{
            if(word2 == "" && word1 != ""){
                document.getElementById('secondWord').value = data.word2;
            }
        }
    }
}


function checkLanguages() {

    var lang1Input = document.getElementById('firstLang');
    var lang2Input = document.getElementById('secondLang');
    var lang1 = lang1Input.value;
    var lang2 = lang2Input.value;

    if(lang1 == lang2 && lang1 != ""){
        lang1Input.style.backgroundColor = 'red';
        lang2Input.style.backgroundColor = 'red';
        return false;
    }else{
        lang1Input.style.backgroundColor = '';
        lang2Input.style.backgroundColor = '';
    }
}
