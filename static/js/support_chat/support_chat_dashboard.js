document.addEventListener("DOMContentLoaded", function () {
    const sessionList = document.getElementById("support-chat-session-list");
    const messagesBox = document.getElementById("support-chat-messages");
    const messageInput = document.getElementById("support-chat-message-input");
    const sendButton = document.getElementById("support-chat-send-btn");
    const closeButton = document.getElementById("support-chat-close-btn");
    const sessionTitle = document.getElementById("support-chat-session-title");

    let socket = null;
    let currentSessionId = null;
    const renderedMessageIds = new Set();

    function getCsrfToken() {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : "";
    }

    function clearMessages() {
        messagesBox.innerHTML = "";
        renderedMessageIds.clear();
    }

    function renderMessage(messageId, authorType, text) {
        if (!messagesBox) return;

        if (messageId && renderedMessageIds.has(String(messageId))) {
            return;
        }

        const item = document.createElement("div");
        item.className = `support-chat-msg ${authorType}`;
        item.textContent = text;

        if (messageId) {
            renderedMessageIds.add(String(messageId));
        }

        messagesBox.appendChild(item);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function connectSocket(sessionId) {
        if (socket) {
            socket.close();
        }

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        socket = new WebSocket(`${protocol}://${window.location.host}/ws/support-chat/${sessionId}/`);

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.event_type === "message") {
                renderMessage(data.message_id, data.sender_role, data.text);
            }

            if (data.event_type === "closed") {
                renderMessage(data.message_id || `closed-${Date.now()}`, "system", data.text);
            }

            if (data.event_type === "operator_connected") {
                renderMessage(data.message_id || `operator-${Date.now()}`, "system", data.text);
            }
        };

        socket.onclose = function () {
            console.warn("Support chat socket closed");
        };
    }

    function loadSession(sessionId) {
        currentSessionId = sessionId;
        clearMessages();

        fetch(`/support-chat/staff/sessions/${sessionId}/`)
            .then(response => response.json())
            .then(data => {
                if (!data.ok) {
                    alert("Не вдалося завантажити чат");
                    return;
                }

                if (sessionTitle) {
                    sessionTitle.textContent = data.session.title || `Чат #${sessionId}`;
                }

                (data.session.messages || []).forEach(message => {
                    renderMessage(message.id, message.author_type, message.text);
                });

                connectSocket(sessionId);
            })
            .catch(error => {
                console.error(error);
                alert("Помилка завантаження чату");
            });
    }

    function sendMessage() {
        const text = messageInput.value.trim();

        if (!text || !socket || socket.readyState !== WebSocket.OPEN) {
            return;
        }

        socket.send(JSON.stringify({
            type: "message",
            sender_role: "operator",
            sender_name: "Спеціаліст",
            text: text
        }));

        messageInput.value = "";
    }

    function closeChat() {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            return;
        }

        socket.send(JSON.stringify({
            type: "close_chat"
        }));
    }

    if (sessionList) {
        sessionList.addEventListener("click", function (event) {
            const button = event.target.closest("[data-session-id]");

            if (!button) {
                return;
            }

            const sessionId = button.dataset.sessionId;
            loadSession(sessionId);
        });
    }

    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    }

    if (closeButton) {
        closeButton.addEventListener("click", closeChat);
    }

    if (messageInput) {
        messageInput.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }
});