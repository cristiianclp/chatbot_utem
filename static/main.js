let messageId = 0;

// Función para agregar mensajes al chat
function addMessage(content, isUser = false, isLoading = false) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}${isLoading ? ' loading' : ''}`;
    messageDiv.id = `message-${messageId++}`;
            
    if (isLoading) {
        messageDiv.innerHTML = `
            <span>Escribiendo</span>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
    } else {
        messageDiv.textContent = content;
    }
            
    // Remover mensaje de bienvenida si existe
    const welcomeMessage = messagesContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
            
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
    return messageDiv;
}

// Función principal de consulta (modificada para el nuevo diseño)
async function consultar() {
    const pregunta = document.getElementById("pregunta").value.trim();
    const sendButton = document.getElementById("sendButton");
            
    if (!pregunta) {
        // Agregar animación de shake al input
        const input = document.getElementById("pregunta");
        input.style.animation = 'shake 0.5s';
        setTimeout(() => input.style.animation = '', 500);
        return;
    }

    // Agregar mensaje del usuario
    addMessage(pregunta, true);
            
    // Limpiar input y deshabilitar botón
    document.getElementById("pregunta").value = "";
    sendButton.disabled = true;
            
    // Agregar mensaje de carga
    const loadingMessage = addMessage("", false, true);

    try {
        const res = await fetch("/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta })
        });

        if (!res.ok) {
            throw new Error("Error en la consulta");
        }

        const data = await res.json();
                
        // Remover mensaje de carga
        loadingMessage.remove();
                
        // Agregar respuesta del bot
        addMessage(data.respuesta, false);

    } catch (error) {
        // Remover mensaje de carga
        loadingMessage.remove();
                
        // Agregar mensaje de error
        addMessage("❌ " + error.message, false);
    } finally {
        // Rehabilitar botón
        sendButton.disabled = false;
        document.getElementById("pregunta").focus();
    }
}

// Permitir envío con Enter
document.getElementById("pregunta").addEventListener("keypress", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        consultar();
    }
});

// Animación de shake para el input
const shakeAnimation = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
        
// Agregar animación de shake al CSS
const style = document.createElement('style');
style.textContent = shakeAnimation;
document.head.appendChild(style);

// Focus automático en el input al cargar
window.addEventListener('load', () => {
    document.getElementById("pregunta").focus();
});