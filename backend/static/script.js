document.addEventListener('DOMContentLoaded', function() {
    sendMessage('', true); // Send an initial empty message to trigger the first LLM message
});

document.getElementById('send-button').addEventListener('click', function() {
    sendMessage();
});

function sendMessage(initialMessage = '', isFirstMessage = false) {
    const userInput = document.getElementById('user-input');
    const messageText = initialMessage || userInput.value.trim();
    
    if (messageText !== "" || isFirstMessage) {
        if (!isFirstMessage) addMessageToChat('user', messageText);
        userInput.value = ''; // Clear input field
        
        // Send the user message to the backend and get the chatbot response
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Django CSRF token
            },
            body: JSON.stringify({ message: messageText, is_first_message: isFirstMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Add the chatbot response to the chat
            addMessageToChat('bot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('bot', 'Sorry, an error occurred. Please try again.');
        });
    }
}

function addMessageToChat(sender, text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = text;
    
    messageElement.appendChild(messageContent);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}