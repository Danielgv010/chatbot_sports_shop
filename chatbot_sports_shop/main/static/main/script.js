onload = main;

function main(){
    document.querySelectorAll('.buy').forEach(function(button) {
        button.addEventListener('click', redirect);
    });

    document.getElementById('chat-button').addEventListener('click', openChat);

    document.getElementById('close-chat-modal').addEventListener('click', closeChat);

    document.getElementById('chat-send').addEventListener('click', sendMessage);
}

function redirect(event){
    var url = window.location.href + "/item/" + event.target.id;
    window.location.replace(url)
}

function openChat(){
    document.getElementById('chat-button').style.display = 'none';
    document.getElementById('chat-modal').style.display = 'block';
}

function closeChat(){
    document.getElementById('chat-button').style.display = 'flex';
    document.getElementById('chat-modal').style.display = 'none';
}

function sendMessage(){
    CHATINPUT = document.getElementById('chat-input');

    if(CHATINPUT.value == ''){
        return;
    }
    
    let userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.innerHTML = CHATINPUT.value;

    CHATINPUT.value = '';
    document.getElementById('chat-box').appendChild(userMessage);
}