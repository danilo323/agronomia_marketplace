document.addEventListener('DOMContentLoaded', function () {
    const launcher = document.getElementById('chatbot-launcher');
    const windowEl = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('chatbot-close');
    const input = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send');
    const messagesContainer = document.getElementById('chatbot-messages');
    const charCount = document.getElementById('chatbot-char-count');
    const MAX_CHARS = 150;

    launcher.addEventListener('click', function () {
        windowEl.classList.toggle('chatbot-hidden');
    });

    closeBtn.addEventListener('click', function () {
        windowEl.classList.add('chatbot-hidden');
    });

    input.addEventListener('input', function () {
        const length = input.value.length;
        charCount.textContent = `${length}/${MAX_CHARS}`;
        sendBtn.disabled = length === 0 || length > MAX_CHARS;
    });

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                sendMessage();
            }
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    function appendMessage(type, text) {
        const msg = document.createElement('div');
        msg.classList.add('chatbot-message', type);

        if (type === 'bot') {
            const avatar = document.createElement('div');
            avatar.classList.add('chatbot-avatar');
            avatar.textContent = '֎';
            msg.appendChild(avatar);
        }

        const bubble = document.createElement('div');
        bubble.classList.add('chatbot-bubble');
        bubble.textContent = text;

        msg.appendChild(bubble);
        messagesContainer.appendChild(msg);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        appendMessage('user', text);
        input.value = '';
        charCount.textContent = `0/${MAX_CHARS}`;
        sendBtn.disabled = true;

        fetch('/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.reply || 'Lo siento, no pude generar una respuesta.');
        })
        .catch(() => {
            appendMessage('bot', 'Ocurrió un error al conectar con el servidor.');
        });
    }
});
