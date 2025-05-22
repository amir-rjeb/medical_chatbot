// script.js

document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const userInput = document.getElementById("user-input");
  const message = userInput.value.trim();

  if (!message) return;

  // Afficher le message de l'utilisateur
  appendMessage("You", message);
  userInput.value = "";

  // Envoyer la requête à l'API locale (Flask ou autre backend)
  appendMessage("Bot", "Thinking...");

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: message })
    });

    const data = await response.json();
    const botReply = data.answer || "Sorry, I couldn't find an answer.";

    // Mettre à jour la dernière réponse "Thinking..."
    updateLastBotMessage(botReply);

  } catch (error) {
    updateLastBotMessage("An error occurred. Please try again.");
  }
});

function appendMessage(sender, text) {
  const chatLog = document.getElementById("chat-log");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatLog.appendChild(messageElement);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function updateLastBotMessage(newText) {
  const chatLog = document.getElementById("chat-log");
  const messages = chatLog.getElementsByClassName("message");
  if (messages.length > 0) {
    messages[messages.length - 1].innerHTML = `<strong>Bot:</strong> ${newText}`;
  }
}
