const chatBox = document.querySelector(".chat-box");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");

function addMessage(message, type) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(type === "user" ? "user-message" : "bot-message");
    messageDiv.innerText = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function speakText(text) {
    if (!("speechSynthesis" in window)) {
        alert("Voice output is not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.95;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    userInput.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        addMessage(data.reply, "bot");
        speakText(data.reply);

    } catch (error) {
        const errorMessage = "Something went wrong. Please try again.";
        addMessage(errorMessage, "bot");
        speakText(errorMessage);
        console.error(error);
    }
}

function startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    voiceBtn.innerText = "Listening...";

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        voiceBtn.innerText = "🎙 Voice";
        sendMessage();
    };

    recognition.onerror = function(event) {
        voiceBtn.innerText = "🎙 Voice";
        alert("Voice input error: " + event.error);
    };

    recognition.onend = function() {
        voiceBtn.innerText = "🎙 Voice";
    };
}

sendBtn.addEventListener("click", sendMessage);

voiceBtn.addEventListener("click", startVoiceInput);

userInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});