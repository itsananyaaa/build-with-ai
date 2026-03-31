const API_URL = "http://localhost:8000";
let authToken = null;
let activePersona = "Professional";
let isConnecting = true;

// View Management
const landingView = document.getElementById("landing-view");
const loginView = document.getElementById("login-view");
const appContainer = document.getElementById("app-container");
const bgMesh = document.getElementById("chat-bg-mesh");

document.body.classList.add("light-theme");

document.getElementById("goto-login-btn").addEventListener("click", () => {
    landingView.style.display = "none";
    loginView.style.display = "flex";
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user = document.getElementById("login-user").value;
    const pass = document.getElementById("login-pass").value;
    const errDiv = document.getElementById("login-error");
    
    try {
        const formData = new URLSearchParams();
        formData.append("username", user);
        formData.append("password", pass);

        const authRes = await fetch(`${API_URL}/auth/init-session`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData.toString()
        });

        if (!authRes.ok) throw new Error("Invalid username or password");
        const authData = await authRes.json();
        authToken = authData.access_token;
        
        // Success: Switch to main app view
        loginView.style.display = "none";
        document.body.classList.remove("light-theme");
        bgMesh.style.display = "block";
        appContainer.style.display = "flex";
        
        initAppUI();
    } catch (err) {
        errDiv.innerText = err.message;
    }
});

// DOM Elements
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const messagesArea = document.getElementById("messages-area");
const suggestionsArea = document.getElementById("suggestions-area");
const personaList = document.getElementById("persona-list");
const statusDot = document.querySelector(".status-dot");
const statusText = document.getElementById("connection-status");
const currentPersonaName = document.getElementById("current-persona-name");
const currentEmotion = document.getElementById("current-emotion");

// Voice Elements
const languageSelect = document.getElementById("language-select");
const ttsCheckbox = document.getElementById("tts-checkbox");
const micBtn = document.getElementById("mic-btn");

// Speech Recognition Setup
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
if (window.SpeechRecognition) {
    recognition = new window.SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
}

let isRecording = false;

if (micBtn) {
    micBtn.addEventListener("click", () => {
        if (!recognition) {
            alert("Speech Recognition not supported in this browser. Please use Chrome/Edge.");
            return;
        }
        
        if (isRecording) {
            recognition.stop();
            return;
        }

        // Set language dynamically
        recognition.lang = languageSelect.value === "Malayalam" ? 'ml-IN' : 'en-US';
        recognition.start();
        isRecording = true;
        micBtn.classList.add("recording");
        chatInput.placeholder = "Listening...";
    });

    if (recognition) {
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
            chatForm.dispatchEvent(new Event("submit")); // Auto-submit voice
        };
        recognition.onend = () => {
            isRecording = false;
            micBtn.classList.remove("recording");
            chatInput.placeholder = "Type or speak your message...";
        };
        recognition.onerror = (e) => {
            console.error("Speech error", e);
            isRecording = false;
            micBtn.classList.remove("recording");
            chatInput.placeholder = "Type or speak your message...";
        };
    }
}

// Text-to-Speech Helper
function speakResponse(text) {
    if (!ttsCheckbox.checked || !window.speechSynthesis) return;
    
    // Cancel existing
    window.speechSynthesis.cancel();
    
    const ut = new SpeechSynthesisUtterance(text);
    // Rough language mapping for TTS
    ut.lang = languageSelect.value === "Malayalam" ? 'ml-IN' : 'en-US';
    
    // Find better voices if available
    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {
        const langCode = languageSelect.value === "Malayalam" ? 'ml' : 'en';
        const targetVoice = voices.find(v => v.lang.startsWith(langCode));
        if (targetVoice) ut.voice = targetVoice;
    }
    
    window.speechSynthesis.speak(ut);
}

// Ensure voices are loaded (browser quirk)
if (window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
}

// Initialize Application (Called after successful login)
async function initAppUI() {
    try {
        await loadPersonas();
        await switchPersona("Professional");

        statusDot.classList.add("connected");
        statusText.innerText = "Connected & Ready";
        isConnecting = false;

        addMessage("Backend connection established! Choose a language (English/Malayalam) and type or use the microphone.", "ai");
    } catch (e) {
        statusText.innerText = "Backend Offline";
        addMessage(`[System] Backend offline at ${API_URL}`, "ai");
    }
}

async function loadPersonas() {
    const res = await fetch(`${API_URL}/persona/list`, {
        headers: { "Authorization": `Bearer ${authToken}` }
    });
    const personas = await res.json();
    
    personaList.innerHTML = "";
    personas.forEach(p => {
        const btn = document.createElement("button");
        btn.className = `persona-btn ${p.name === activePersona ? "active" : ""}`;
        btn.innerText = `${p.name} Persona`;
        btn.onclick = () => switchPersona(p.name, btn);
        personaList.appendChild(btn);
    });
}

async function switchPersona(name, targetBtn = null) {
    if (!authToken) return;
    
    const res = await fetch(`${API_URL}/persona/select`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify({ persona_name: name })
    });
    
    if (res.ok) {
        activePersona = name;
        currentPersonaName.innerText = `${name} Persona`;
        
        document.querySelectorAll(".persona-btn").forEach(b => b.classList.remove("active"));
        if (targetBtn) targetBtn.classList.add("active");
        
        suggestionsArea.innerHTML = "";
        currentEmotion.innerText = "Scanning Context...";
        
        // Stop any current reading
        if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
}

// Handle Chat Submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message || isConnecting) return;
    
    addMessage(message, "user");
    chatInput.value = "";
    currentEmotion.innerText = "Analyzing...";
    
    try {
        const res = await fetch(`${API_URL}/chat/message`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
            },
            // Pass the globally selected language dynamically!
            body: JSON.stringify({ 
                message: message, 
                language: languageSelect.value 
            })
        });
        
        const data = await res.json();
        
        addMessage(data.response, "ai");
        currentEmotion.innerText = `Emotion Detected: ${data.emotion.toUpperCase()}`;
        renderSuggestions(data.suggestions);

        // Auto-Speak AI response!
        speakResponse(data.response);

    } catch (err) {
        addMessage("[Error] Failed to get response.", "ai");
    }
});

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}-message`;
    div.innerHTML = `<div class="message-content">${text}</div>`;
    messagesArea.appendChild(div);
    scrollToBottom();
}

function renderSuggestions(suggestionsArray) {
    suggestionsArea.innerHTML = "";
    suggestionsArray.forEach(txt => {
        const pill = document.createElement("div");
        pill.className = "suggestion-pill";
        pill.innerText = txt;
        pill.onclick = () => {
            chatInput.value = txt;
            chatForm.dispatchEvent(new Event("submit"));
        };
        suggestionsArea.appendChild(pill);
    });
}

function scrollToBottom() {
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Do not auto-initialize. Wait for login logic.
