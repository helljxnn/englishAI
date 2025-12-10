document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        userInput.value = '';

        // Show loading indicator
        const loadingId = showLoading();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            
            // Remove loading indicator
            removeLoading(loadingId);

            if (data.error) {
                addMessage(data.error, 'bot', true);
            } else {
                addMessage(data.response, 'bot');
            }

        } catch (error) {
            removeLoading(loadingId);
            addMessage("Sorry, I'm having trouble connecting right now.", 'bot', true);
            console.error('Error:', error);
        }
    });

    function addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        if (isError) contentDiv.style.color = '#ef4444';
        
        // Simple markdown parsing for bold text
        const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        contentDiv.innerHTML = formattedText;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showLoading() {
        const id = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('typing-indicator');
        loadingDiv.id = id;
        
        loadingDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;
        
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeLoading(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }
});
