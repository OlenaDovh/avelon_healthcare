document.addEventListener("DOMContentLoaded", function () {
    const sessionId = window.CHAT_SESSION_ID;
    const senderName = window.CHAT_SENDER_NAME;

    const messagesBox = document.getElementById("operator-chat-messages");
    const typingNode = document.getElementById("operator-chat-typing");
    const input = document.getElementById("operator-chat-input");
    const sendBtn = document.getElementById("operator-chat-send-btn");
    const finishBtn = document.getElementById("operator-chat-finish-btn");

    let typingTimeout = null;
    let isTypingSent = false;

    const renderedMessageIds = new Set(
        Array.from(messagesBox.querySelectorAll("[data-message-id]"))
            .map(node => node.dataset.messageId)
            .filter(Boolean)
    );

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/support-chat/${sessionId}/`);

    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function showTyping(text) {
        if (!typingNode) return;
        typingNode.textContent = text;
        typingNode.classList.remove("d-none");
    }

    function hideTyping() {
        if (!typingNode) return;
        typingNode.textContent = "";
        typingNode.classList.add("d-none");
    }

    function sendTypingStart() {
        if (!socket || socket.readyState !== WebSocket.OPEN || isTypingSent) return;

        socket.send(JSON.stringify({
            type: "typing_start",
            sender_role: "operator",
            sender_name: senderName,
        }));

        isTypingSent = true;
    }

    function sendTypingStop() {
        if (!socket || socket.readyState !== WebSocket.OPEN || !isTypingSent) return;

        socket.send(JSON.stringify({
            type: "typing_stop",
            sender_role: "operator",
            sender_name: senderName,
        }));

        isTypingSent = false;
    }

    function scheduleTypingStop() {
        if (typingTimeout) clearTimeout(typingTimeout);

        typingTimeout = setTimeout(sendTypingStop, 1200);
    }

    function appendMessage(messageId, authorType, authorName, text) {
        if (messageId && renderedMessageIds.has(String(messageId))) return;

        const wrapper = document.createElement("div");
        wrapper.className = "mb-2 d-flex";

        if (messageId) {
            wrapper.dataset.messageId = String(messageId);
            renderedMessageIds.add(String(messageId));
        }

        if (authorType === "operator") wrapper.classList.add("justify-content-end");
        else if (authorType === "user") wrapper.classList.add("justify-content-start");
        else wrapper.classList.add("justify-content-center");

        const bubble = document.createElement("div");
        bubble.className = "p-2 rounded";
        bubble.style.maxWidth = "75%";

        if (authorType === "operator") bubble.classList.add("bg-success-subtle", "text-dark");
        else if (authorType === "user") bubble.classList.add("bg-light");
        else bubble.classList.add("bg-warning-subtle", "text-dark");

        if (authorType !== "system") {
            const meta = document.createElement("div");
            meta.className = "small text-muted mb-1";
            meta.textContent = authorName || "";
            bubble.appendChild(meta);
        }

        const textNode = document.createElement("div");
        textNode.textContent = text;
        bubble.appendChild(textNode);

        wrapper.appendChild(bubble);
        messagesBox.appendChild(wrapper);

        scrollToBottom();
    }

    scrollToBottom();

    if (sendBtn) {
        sendBtn.addEventListener("click", function () {
            const text = input.value.trim();
            if (!text || socket.readyState !== WebSocket.OPEN) return;

            socket.send(JSON.stringify({
                type: "message",
                sender_role: "operator",
                sender_name: senderName,
                text: text,
            }));

            sendTypingStop();
            input.value = "";
        });
    }

    if (finishBtn) {
        finishBtn.addEventListener("click", function () {
            if (socket.readyState !== WebSocket.OPEN) return;

            socket.send(JSON.stringify({
                type: "close_chat",
            }));
        });
    }

    if (input) {
        input.addEventListener("input", function () {
            if (input.value.trim()) {
                sendTypingStart();
                scheduleTypingStop();
            } else {
                sendTypingStop();
            }
        });

        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendBtn.click();
            }
        });
    }

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        if (data.event_type === "message") {
            hideTyping();
            appendMessage(data.message_id, data.sender_role, data.sender_name, data.text);
        } else if (data.event_type === "operator_connected") {
            appendMessage(`system-${Date.now()}`, "system", "", data.text);
        } else if (data.event_type === "typing_start") {
            if (data.sender_role === "user") showTyping("Користувач друкує...");
        } else if (data.event_type === "typing_stop") {
            if (data.sender_role === "user") hideTyping();
        } else if (data.event_type === "closed") {
            hideTyping();
            appendMessage(`closed-${Date.now()}`, "system", "", data.text);

            if (input) input.disabled = true;
            if (sendBtn) sendBtn.disabled = true;
            if (finishBtn) finishBtn.disabled = true;
        }
    };
});