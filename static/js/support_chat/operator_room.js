document.addEventListener("DOMContentLoaded", function () {
    const sessionId = window.CHAT_SESSION_ID;
    const senderName = window.CHAT_SENDER_NAME || "Оператор";

    const messagesBox = document.getElementById("operator-chat-messages");
    const input = document.getElementById("operator-chat-input");
    const sendBtn = document.getElementById("operator-chat-send-btn");
    const finishBtn = document.getElementById("operator-chat-finish-btn");

    if (!sessionId || !messagesBox) {
        console.error("Немає sessionId або контейнера чату");
        return;
    }

    const renderedMessageIds = new Set(
        Array.from(messagesBox.querySelectorAll("[data-message-id]"))
            .map(node => node.dataset.messageId)
            .filter(Boolean)
    );

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(
        `${protocol}://${window.location.host}/ws/support-chat/${sessionId}/`
    );

    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function appendMessage(messageId, authorType, text) {
        // ❌ повністю прибираємо system
        if (authorType === "system") return;

        if (messageId && renderedMessageIds.has(String(messageId))) return;

        const wrapper = document.createElement("div");
        wrapper.className = "mb-2 d-flex";

        if (messageId) {
            wrapper.dataset.messageId = String(messageId);
            renderedMessageIds.add(String(messageId));
        }

        if (authorType === "operator") {
            wrapper.classList.add("justify-content-end");
        } else {
            wrapper.classList.add("justify-content-start");
        }

        const bubble = document.createElement("div");
        bubble.className = "p-2 px-3 rounded-3 shadow-sm";
        bubble.style.maxWidth = "70%";

        if (authorType === "operator") {
            bubble.classList.add("bg-success-subtle");
        } else {
            bubble.classList.add("bg-light");
        }

        bubble.textContent = text;

        wrapper.appendChild(bubble);
        messagesBox.appendChild(wrapper);

        scrollToBottom();
    }

    function disableChat() {
        if (input) input.disabled = true;
        if (sendBtn) sendBtn.disabled = true;
        if (finishBtn) finishBtn.disabled = true;
    }

    function sendMessage() {
        const text = input.value.trim();

        if (!text) return;
        if (socket.readyState !== WebSocket.OPEN) return;

        socket.send(JSON.stringify({
            type: "message",
            sender_role: "operator",
            sender_name: senderName,
            text: text
        }));

        input.value = "";
    }

    function finishChat() {
        if (socket.readyState !== WebSocket.OPEN) return;

        socket.send(JSON.stringify({
            type: "close_chat"
        }));

        disableChat(); // одразу блокуємо
    }

    // кнопки
    if (sendBtn) sendBtn.addEventListener("click", sendMessage);
    if (finishBtn) finishBtn.addEventListener("click", finishChat);

    // Enter = send
    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }

    // WebSocket події
    socket.onopen = function () {
        console.log("WS підключено");
        scrollToBottom();
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (data.event_type === "message") {
            appendMessage(
                data.message_id,
                data.sender_role,
                data.text
            );
        }

        // ❌ ігноруємо system-події
        if (data.event_type === "operator_connected") return;

        if (data.event_type === "closed") {
            disableChat();
        }
    };

    socket.onerror = function (e) {
        console.error("WS помилка", e);
    };

    socket.onclose = function () {
        console.log("WS закрито");
    };

    scrollToBottom();
});