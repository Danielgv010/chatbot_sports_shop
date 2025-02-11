onload = main;
jsonStatus = 0;


function main() {
    document.querySelectorAll('.buy').forEach(function (button) {
        button.addEventListener('click', redirect);
    });

    document.getElementById('chat-button').addEventListener('click', openChat);

    document.getElementById('close-chat-modal').addEventListener('click', closeChat);

    document.getElementById('show-json').addEventListener('click', showJson);

    document.getElementById('chat-send').addEventListener('click', sendMessage);
}

function redirect(event) {
    var url = window.location.href + "/item/" + event.target.id;
    window.location.replace(url)
}

function openChat() {
    document.getElementById('chat-button').style.display = 'none';
    document.getElementById('chat-modal').style.display = 'block';
}

function closeChat() {
    document.getElementById('chat-button').style.display = 'flex';
    document.getElementById('chat-modal').style.display = 'none';
}

function sendMessage() {
    CHATINPUT = document.getElementById('chat-input');

    if (CHATINPUT.value == '') {
        return;
    }

    let userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerHTML = CHATINPUT.value;

    getResponse(CHATINPUT.value);

    CHATINPUT.value = '';
    document.getElementById('chat-box').appendChild(userMessage);
}

function getResponse(inputValue) {
    let xhr = new XMLHttpRequest();
    let url = `http://127.0.0.1:8000/send_message?query=${encodeURIComponent(inputValue)}`;

    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                let response = JSON.parse(xhr.responseText);

                let systemMessageJson = document.createElement('div');
                systemMessageJson.className = 'json-message';
                systemMessageJson.innerHTML = JSON.stringify(response.result.prediction);
                document.getElementById('chat-box').appendChild(systemMessageJson);

                let systemMessage = document.createElement('div');
                systemMessage.className = 'system-message';
                systemMessage.innerHTML = JSON.stringify(response.result.prediction.topIntent);
                document.getElementById('chat-box').appendChild(systemMessage);
            } else {
                console.error("Error:", xhr.responseText);
            }
        }
    };
    xhr.send();
}

function showJson() {
    if (!jsonStatus) {
        jsonStatus = 1;
        document.querySelectorAll(".json-message").forEach((item) => {
            item.style.display = 'block';
        });

        document.querySelectorAll(".system-message").forEach((item) => {
            item.style.display = 'none';
        });
    } else {
        jsonStatus = 0;
        document.querySelectorAll(".json-message").forEach((item) => {
            item.style.display = 'none';
        });

        document.querySelectorAll(".system-message").forEach((item) => {
            item.style.display = 'block';
        });
    }
}