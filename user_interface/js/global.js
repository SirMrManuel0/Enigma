const IP = "127.0.0.1";
const PORT = "8000";

const allowed = [
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'
]

var code = 1;
var turn = 0;
var turn2 = 0;
var plugboard = {};
var alpha_code = [1, 1, 1];
var rotor1Kind = "I";
var rotor2Kind = "I";
var rotor3Kind = "I";
var reflectorKind = "B";
var beta_code = [1, 1, 1]

async function callServer(data) {
    let re = {};
    try {
        const response = await fetch('http://' + IP + ':' + PORT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        re = await response.json();
    } catch (error) {
        createError('POST Error:', error);
    }

    return re;
}

function getJSONed(msgP){
    return {
        code: code - 1,
        rotor1: { position: 1, kind: rotor1Kind, ringposition: 1 },
        rotor2: { position: 2, kind: rotor2Kind, ringposition: 1 },
        rotor3: { position: 3, kind: rotor3Kind, ringposition: 1 },
        reflector: { kind: reflectorKind },
        plugboard: plugboard,
        alpha_code: alpha_code,
        hide_code: beta_code,
        msg: msgP
    }
}

function removeError(){
    document.getElementById("errorMessageWrapper").classList.add('hidden');
    document.getElementById("errorMessage").textContent = "";
}
function createError(msg){
    document.getElementById("errorMessageWrapper").classList.remove('hidden');
    document.getElementById("errorMessage").textContent = msg;
}

function removeInfo(){
    document.getElementById("infoMessageWrapper").classList.add('hidden');
    document.getElementById("infoMessage").textContent = "";
}
function createInfo(msg){
    document.getElementById("infoMessageWrapper").classList.remove('hidden');
    document.getElementById("infoMessage").textContent = msg;
}

function increase_code(){
    if (code == 4) return;
    code ++;
    document.getElementById("CodeNum").textContent = code;
    switch (code) {
        case 1:
            createInfo("This mode is the standard mode. You can encrypt entire sentences / texts.");
            break;
        case 2:
            createInfo("This mode will encrypt the message according to german WW2 regulations.");
            break;
        case 3:
            createInfo("This mode will decrypt the message according to german WW2 regulations. It is recommended to paste from mode 2.");
            break;
        case 4:
            createInfo("This mode will encrypt / decrypt letter by letter. It is recommended to host the server locally for this.");
            break;
    }
    document.getElementById("message-input").value = "";
    document.getElementById("message-output").value = "";
    document.getElementById("leftButton").classList.remove('hidden');
    if (code == 4){
        document.getElementById("rightButton").classList.add('hidden');
    }
}
function decrease_code(){
    if (code == 1) return;
    code --;
    document.getElementById("CodeNum").textContent = code;
    switch (code) {
        case 1:
            createInfo("This mode is the standard mode. You can encrypt entire sentences / texts.");
            break;
        case 2:
            createInfo("This mode will encrypt the message according to german WW2 regulations.");
            break;
        case 3:
            createInfo("This mode will decrypt the message according to german WW2 regulations. It is recommended to paste from mode 2.");
            break;
        case 4:
            createInfo("This mode will encrypt / decrypt letter by letter. It is recommended to host the server locally for this.");
            break;
    }
    document.getElementById("message-input").value = "";
    document.getElementById("message-output").value = "";
    document.getElementById("rightButton").classList.remove('hidden');
    if (code == 1){
        document.getElementById("leftButton").classList.add('hidden');
    }
}

function hidePlugboardHover(){
    document.getElementById("plugboardHoverWrapper").classList.add('hidden');
    let parentElement = document.getElementById("inner-containerHoverPlug")
    while (parentElement.firstChild) {
        parentElement.removeChild(parentElement.firstChild);
    }
    let dontGoOver = [];
    let count = 1;
    for (let key in plugboard){
        if (inArr(key, dontGoOver)) continue;
        let val = plugboard[key];
        dontGoOver.push(String(val));
        let spanElement = document.getElementById('plug'+count);
        spanElement.textContent = String.fromCharCode(parseInt(key) + 64) + " - " + String.fromCharCode(val + 64);
        count++;
    }
}

function inArr(searchFor, toBeSearched){
    for (let i in toBeSearched){
        if (toBeSearched[i] == searchFor) return true;
    }
    return false;
}

// Function to handle letter clicks
function handleLetterClick(event) {
    const clickedLetter = event.target;
    const markedLetters = document.querySelectorAll('.letter.marked');
    
    if (clickedLetter.classList.contains('marked')) {
        clickedLetter.classList.remove('marked');
    } else if (markedLetters.length < 2) {
        clickedLetter.classList.add('marked');
    }
    if (markedLetters.length === 1 && clickedLetter.classList.contains('marked')) {
        let letter1 = markedLetters[0].textContent;
        let letter2 = clickedLetter.textContent;
        let num1 = letter1.charCodeAt(0) - 64; // Convert letter to number
        let num2 = letter2.charCodeAt(0) - 64; // Convert letter to number

        plugboard[num1] = num2;
        plugboard[num2] = num1;

        hidePlugboardHover();
    }
}

function showPlugboardHover(){
    if (Object.keys(plugboard).length >= 20) return;
    // Generate letter divs
    let innerContainer = document.querySelector('#inner-containerHoverPlug');
    for (let i = 65; i <= 90; i++) {
        if ((i - 64) in plugboard){
            continue;
        }
        let letterDiv = document.createElement('div');
        letterDiv.textContent = String.fromCharCode(i);
        letterDiv.className = 'letter';
        letterDiv.addEventListener('click', handleLetterClick);
        innerContainer.appendChild(letterDiv);
    }
}

function clearPlugboard(){
    plugboard = {};
    for (let i = 1; i <= 10; i++){
        let spanElement = document.getElementById('plug'+i);
        spanElement.textContent = "";
    }
}

function decrease_alpha_code(position){
    let pos = alpha_code[position];
    pos --;
    if (pos <= 0){
        pos = 26;
    }
    alpha_code[position] = pos;
    let element;
    switch (position){
        case 2:
            element = document.getElementById("rotor1Span");
            break;
        case 1:
            element = document.getElementById("rotor2Span");
            break;
        case 0:
            element = document.getElementById("rotor3Span");
            break;
    }
    element.textContent = String.fromCharCode(pos + 64);
}

function increase_alpha_code(position){
    let pos = alpha_code[position];
    pos ++
    if (pos >= 27){
        pos = 1;
    }
    alpha_code[position] = pos;
    let element;
    switch (position){
        case 2:
            element = document.getElementById("rotor1Span");
            break;
        case 1:
            element = document.getElementById("rotor2Span");
            break;
        case 0:
            element = document.getElementById("rotor3Span");
            break;
    }
    element.textContent = String.fromCharCode(pos + 64);
}

function showRotor1Hover(){
    document.getElementById("rotor1HoverWrapper").classList.remove('hidden');

}
function showRotor2Hover(){
    document.getElementById("rotor2HoverWrapper").classList.remove('hidden');
}
function showRotor3Hover(){
    document.getElementById("rotor3HoverWrapper").classList.remove('hidden');
}

function sendMessage(str = null){
    let msg = document.getElementById("message-input").value;
    if (typeof str === 'string') msg = str.toUpperCase();
    if (msg.length < 1) return;
    switch (code){
        case 2:
            msg = msg.replace(/ /g, "X");
        case 1:
            msg = validateCode1(msg);
            break;
        case 3:
            msg = validateCode3(msg);
            break;
    }
    if (msg == null) return;
    setResponse(msg);

}

function validateCode1(msg){
    msg = msg.replace(/ /g, "");
    msg = msg.replace(/\n/g, "");
    if (msg.length == 0) return;
    for (let i = 0; i < msg.length; i++){
        if (!inArr(msg.charAt(i), allowed)) {
            createError("Only uppercase english letters, space and new line!");
            return null;
        }
    }
    return msg;
}

function validateCode3(msg){
    return msg;
}

async function setResponse(msg){
    let response = await callServer(getJSONed(msg));
    response = response["encrypted_message"];
    if (code != 4){
        document.getElementById("message-output").value = response;
    } else{
        document.getElementById("message-output").value += response;
    }
}

function setBeta(){
    let c = document.getElementById("beta-code-input").value;
    if (c.length != 3){
        createError("The code must be exactly 3 letters long!");
        return;
    }
    c = c.toUpperCase();
    let b_code = ["A", "A", "A"];
    for (let i = 0; i < 3; i++){
        if (c.charCodeAt(i) <= (26 + 64) && c.charCodeAt(i) >= 65) {
            b_code[i] = (c.charCodeAt(i) - 64);
        } else {
            createError("The code must consist of only english letters!");
            return;
        }
    }
    beta_code = b_code;
    console.log(beta_code);
    sendMessage();
    document.getElementById("betaCodeHoverWrapper").classList.add("hidden");
}

window.onload = function() {
    document.getElementById("rightButton").addEventListener('click', increase_code);
    document.getElementById("leftButton").addEventListener('click', decrease_code);
    document.getElementById("rightButton").addEventListener('click', clearPlugboard);
    document.getElementById("leftButton").addEventListener('click', clearPlugboard);
    document.getElementById("plus-button").addEventListener('click', showPlugboardHover);
    document.addEventListener('click', function(event) {
        const wrapper = document.getElementById('plugboardHoverWrapper');
        const targetElement = event.target;

        if ((!wrapper.classList.contains('hidden') && !wrapper.contains(targetElement) && targetElement !== document.getElementById('plus-button'))
             || wrapper == targetElement) {
            hidePlugboardHover()
        }
    });
    document.getElementById("rotor3ButUp").addEventListener('click', function(){increase_alpha_code(0)});
    document.getElementById("rotor2ButUp").addEventListener('click', function(){increase_alpha_code(1)});
    document.getElementById("rotor1ButUp").addEventListener('click', function(){increase_alpha_code(2)});
    document.getElementById("rotor1ButDown").addEventListener('click', function(){decrease_alpha_code(2)});
    document.getElementById("rotor2ButDown").addEventListener('click', function(){decrease_alpha_code(1)});
    document.getElementById("rotor3ButDown").addEventListener('click', function(){decrease_alpha_code(0)});
    document.getElementById("switchRotor1").addEventListener('click', showRotor1Hover);
    document.getElementById("switchRotor2").addEventListener('click', showRotor2Hover);
    document.getElementById("switchRotor3").addEventListener('click', showRotor3Hover);
    document.getElementById('send-button').addEventListener('click', function(){
        if (code != 2) sendMessage();
        else{
            document.getElementById("betaCodeHoverWrapper").classList.remove("hidden");
        }
    });
    document.getElementById('beta-button').addEventListener('click', setBeta);

    document.getElementById('message-input').addEventListener('keypress', function(event) {
        const charStr = event.key;
        if (code == 3) {
            if (!(/[a-zA-Z\s0-9-]/.test(charStr)) && charStr !== 'Enter') {
                event.preventDefault();     
            }
            // Check if Enter is pressed without Shift
            if (charStr === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
                return;
            }
        }
        // Allow only letters (uppercase and lowercase), spaces, and return (enter) key
        if (!(/[a-zA-Z\s]/.test(charStr)) && charStr !== 'Enter') {
            event.preventDefault();
        }
    
        // Check if Enter is pressed without Shift
        if (charStr === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (code == 4){
                turn = 0;
            } else if (code == 2){
                document.getElementById("betaCodeHoverWrapper").classList.remove("hidden");
            } else{
                sendMessage();
            }

        }
        if (code == 4){
            if (/[a-zA-Z]/.test(charStr)){
                sendMessage(charStr);
                turn += 1;
                increase_alpha_code(2)
                if (turn == 25){
                    increase_alpha_code(1)
                    turn2 += 1
                    turn = 0;
                }
                if (turn2 == 25){
                    increase_alpha_code(0)
                    turn2 = 0;
                }

            }   
        }
    });
    
    
    document.getElementById('message-input').addEventListener('input', function(event) {
        // Convert all input to uppercase
        this.value = this.value.toUpperCase();
    });
    
    document.getElementById('message-input').addEventListener('paste', function(event) {
        event.preventDefault();
        if (code == 4) return;
        let paste = (event.clipboardData || window.clipboardData).getData('text');
        if (code == 3){
            paste = paste.toUpperCase().replace(/[^A-Z\s\n0-9-]/g, '');
        } else {
            paste = paste.toUpperCase().replace(/[^A-Z\s\n]/g, '');
        }
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const textBefore = this.value.substring(0, start);
        const textAfter  = this.value.substring(end, this.value.length);
        this.value = textBefore + paste + textAfter;
        this.setSelectionRange(start + paste.length, start + paste.length);
    });
    document.getElementById('beta-code-input').addEventListener('keypress', function(event) {
        const charStr = event.key;
        if (!(/[a-zA-Z]/.test(charStr)) && charStr !== 'Enter') {
            event.preventDefault();     
        }
        if (charStr === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.value = this.value.toUpperCase();
            setBeta();
            return;
        }
    });
    
    
    document.getElementById('beta-code-input').addEventListener('input', function(event) {
        this.value = this.value.toUpperCase();
    });
    
    document.getElementById('beta-code-input').addEventListener('paste', function(event) {
        event.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const textBefore = this.value.substring(0, start);
        const textAfter  = this.value.substring(end, this.value.length);
        if (paste.length >= 3) paste = paste.substring(0, 2);
        this.value = textBefore + paste + textAfter;
        this.setSelectionRange(start + paste.length, start + paste.length);
    });

    document.getElementById("reflectorButton").addEventListener('click', function(){
        document.getElementById("reflectorHoverWrapper").classList.remove('hidden');
    });
    document.getElementById("reflector-select-B").addEventListener('click', function(){
        document.getElementById("reflectorHoverWrapper").classList.add('hidden');
        document.getElementById("reflectorButton").textContent = "B";
        reflectorKind = "B";
    });
    document.getElementById("reflector-select-C").addEventListener('click', function(){
        document.getElementById("reflectorHoverWrapper").classList.add('hidden');
        document.getElementById("reflectorButton").textContent = "C";
        reflectorKind = "C";
    });

    document.getElementById("rotor1-select-I").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "I";
        rotor1Kind = "I";
    });
    document.getElementById("rotor1-select-II").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "II";
        rotor1Kind = "II";
    });
    document.getElementById("rotor1-select-III").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "III";
        rotor1Kind = "III";
    });
    document.getElementById("rotor1-select-IV").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "IV";
        rotor1Kind = "IV";
    });
    document.getElementById("rotor1-select-V").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "V";
        rotor1Kind = "V";
    });
    document.getElementById("rotor1-select-VI").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "VI";
        rotor1Kind = "VI";
    });
    document.getElementById("rotor1-select-VII").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "VII";
        rotor1Kind = "VII";
    });
    document.getElementById("rotor1-select-VIII").addEventListener('click', function(){
        document.getElementById("rotor1HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor1").textContent = "VIII";
        rotor1Kind = "VIII";
    });
    document.getElementById("rotor2-select-I").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "I";
        rotor2Kind = "I";
    });
    document.getElementById("rotor2-select-II").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "II";
        rotor2Kind = "II";
    });
    document.getElementById("rotor2-select-III").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "III";
        rotor2Kind = "III";
    });
    document.getElementById("rotor2-select-IV").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "IV";
        rotor2Kind = "IV";
    });
    document.getElementById("rotor2-select-V").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "V";
        rotor2Kind = "V";
    });
    document.getElementById("rotor2-select-VI").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "VI";
        rotor2Kind = "VI";
    });
    document.getElementById("rotor2-select-VII").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "VII";
        rotor2Kind = "VII";
    });
    document.getElementById("rotor2-select-VIII").addEventListener('click', function(){
        document.getElementById("rotor2HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor2").textContent = "VIII";
        rotor2Kind = "VIII";
    });
    document.getElementById("rotor3-select-I").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "I";
        rotor3Kind = "I";
    });
    document.getElementById("rotor3-select-II").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "II";
        rotor3Kind = "II";
    });
    document.getElementById("rotor3-select-III").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "III";
        rotor3Kind = "III";
    });
    document.getElementById("rotor3-select-IV").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "IV";
        rotor3Kind = "IV";
    });
    document.getElementById("rotor3-select-V").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "V";
        rotor3Kind = "V";
    });
    document.getElementById("rotor3-select-VI").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "VI";
        rotor3Kind = "VI";
    });
    document.getElementById("rotor3-select-VII").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "VII";
        rotor3Kind = "VII";
    });
    document.getElementById("rotor3-select-VIII").addEventListener('click', function(){
        document.getElementById("rotor3HoverWrapper").classList.add('hidden');
        document.getElementById("switchRotor3").textContent = "VIII";
        rotor3Kind = "VIII";
    });
};