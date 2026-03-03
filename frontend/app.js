let sessionId = null;
let isWaiting = false;

const chatContainer = document.getElementById("messagesArea");
const inputBox = document.getElementById("userInput");
const sendButton = document.getElementById("sendBtn");

// =======================
// Event Listeners
// =======================

sendButton.addEventListener("click", sendMessage);

inputBox.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !isWaiting) {
        e.preventDefault();
        sendMessage();
    }
});

// =======================
// Send Message
// =======================

async function sendMessage() {
    const question = inputBox.value.trim();
    if (!question || isWaiting) return;

    displayMessage(question, "user");
    inputBox.value = "";

    setInputState(true);
    isWaiting = true;

    displayMessage("Typing...", "assistant");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                question: question
            })
        });

        const data = await response.json();

        if (!sessionId && data.session_id) {
            sessionId = data.session_id;
        }

        removeLastMessage();
        displayMessage(data.answer || "No response", "assistant");

    } catch (err) {
        removeLastMessage();
        displayMessage("Server error.", "assistant");
        console.error(err);
    }

    setInputState(false);
    isWaiting = false;
}

// =======================
// UI Functions
// =======================

function displayMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}-message`;

    const bubble = document.createElement("p");
    bubble.textContent = text;

    msg.appendChild(bubble);
    chatContainer.appendChild(msg);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLastMessage() {
    if (chatContainer.lastChild) {
        chatContainer.removeChild(chatContainer.lastChild);
    }
}

function setInputState(disabled) {
    inputBox.disabled = disabled;
    sendButton.disabled = disabled;
}