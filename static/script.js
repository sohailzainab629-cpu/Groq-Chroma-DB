const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("sendBtn");
const chatArea = document.querySelector(".chat-area");

async function sendQuestion() {
const question = questionInput.value.trim();

```
if (!question) {
    return;
}

// Show user message
const userMessage = document.createElement("div");
userMessage.className = "message user-message";
userMessage.innerHTML = `
    <div class="avatar"></div>
    <div class="message-content">
        <p>${question}</p>
    </div>
`;

chatArea.appendChild(userMessage);

questionInput.value = "";

// Show loading message
const botMessage = document.createElement("div");
botMessage.className = "message bot-message";
botMessage.innerHTML = `
    <div class="avatar"></div>
    <div class="message-content">
        <p>Thinking...</p>
    </div>
`;

chatArea.appendChild(botMessage);

try {
    const response = await fetch("/rag/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question,
            top_k: 2
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            typeof data.detail === "string"
                ? data.detail
                : "Request failed"
        );
    }

    const answer =
        data.answer ||
        data.response ||
        data.result ||
        JSON.stringify(data);

    botMessage.querySelector("p").textContent = answer;

} catch (error) {
    botMessage.querySelector("p").textContent =
        "Error: " + error.message;
}

chatArea.scrollTop = chatArea.scrollHeight;
```

}

sendBtn.addEventListener("click", sendQuestion);

questionInput.addEventListener("keydown", function (event)
if (event.key === "Enter" && !event.shiftKey)
event.preventDefault();
sendQuestion();
