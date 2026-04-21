document.addEventListener("DOMContentLoaded", function () {
    const root = document.getElementById("support-chat-root");
    if (!root) return;

    const launcher = document.getElementById("support-chat-launcher");
    const panel = document.getElementById("support-chat-panel");
    const closeBtn = document.getElementById("support-chat-close-btn");
    const finishBtn = document.getElementById("support-chat-finish-btn");
    const startBtn = document.getElementById("start-support-chat-btn");
    const messagesWrap = document.getElementById("support-chat-messages-wrap");
    const startFormWrap = document.getElementById("support-chat-start-form-wrap");
    const messagesBox = document.getElementById("support-chat-messages");
    const sendBtn = document.getElementById("support-chat-send-btn");
    const newChatBtn = document.getElementById("support-chat-new-btn");
    const input = document.getElementById("support-chat-message-input");
    const statusNode = document.getElementById("support-chat-status");

    let socket = null;
    let sessionId = null;
    const renderedMessageIds = new Set();

    const isAuthenticated = root.dataset.isAuthenticated === "true";
    const senderName = root.dataset.senderName;
    const currentSessionUrl = root.dataset.currentSessionUrl;
    const createSessionUrl = root.dataset.createSessionUrl;
    const wsBaseUrl = root.dataset.wsBaseUrl;
    const csrfToken = root.dataset.csrfToken;

    function setStatus(text) {
        if (statusNode) statusNode.textContent = text;
    }

    function openPanel() {
        panel.classList.remove("d-none");
    }

    function closePanel() {
        panel.classList.add("d-none");
    }

    function switchToChatMode() {
        startFormWrap.classList.add("d-none");
        messagesWrap.classList.remove("d-none");
    }

    function switchToStartMode() {
        startFormWrap.classList.remove("d-none");
        messagesWrap.classList.add("d-none");
    }

    function clearMessages() {
        messagesBox.innerHTML = "";
        renderedMessageIds.clear();
    }

    function renderMessage(messageId, authorType, text) {
        if (messageId && renderedMessageIds.has(String(messageId))) {
            return;
        }

        const item = document.createElement("div");
        item.className = `support-chat-msg ${authorType}`;

        if (messageId) {
            item.dataset.messageId = String(messageId);
            renderedMessageIds.add(String(messageId));
        }

        item.textContent = text;
        messagesBox.appendChild(item);

        messagesBox.scrollTo({
            top: messagesBox.scrollHeight,
            behavior: "smooth"
        });
    }

    function connectWebSocket() {
        if (!sessionId) return;

        if (socket) {
            socket.close();
        }

        socket = new WebSocket(`${wsBaseUrl}${sessionId}/`);

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.event_type === "message") {
                renderMessage(data.message_id, data.sender_role, data.text);
            } else if (data.event_type === "operator_connected") {
                renderMessage(data.message_id || `operator-${Date.now()}`, "system", data.text);
                setStatus("Оператор підключився");
            } else if (data.event_type === "closed") {
                renderMessage(data.message_id || `closed-${Date.now()}`, "system", data.text);
                setStatus("Чат завершено");

                if (input) input.disabled = true;
                if (sendBtn) sendBtn.disabled = true;
                if (finishBtn) finishBtn.disabled = true;
                if (newChatBtn) newChatBtn.classList.remove("d-none");
            }
        };
    }

    function loadExistingSession() {
        fetch(currentSessionUrl)
            .then(response => response.json())
            .then(data => {
                if (!data.ok || !data.session) return;

                sessionId = data.session.id;
                switchToChatMode();
                clearMessages();

                (data.session.messages || []).forEach(message => {
                    renderMessage(message.id, message.author_type, message.text);
                });

                if (data.session.status === "waiting") {
                    setStatus("Очікуємо підключення оператора");
                } else if (data.session.status === "active") {
                    setStatus(
                        data.session.operator_name
                            ? `Оператор: ${data.session.operator_name}`
                            : "Оператор підключився"
                    );
                } else if (data.session.status === "closed") {
                    setStatus("Чат завершено");
                    if (input) input.disabled = true;
                    if (sendBtn) sendBtn.disabled = true;
                    if (finishBtn) finishBtn.disabled = true;
                    if (newChatBtn) newChatBtn.classList.remove("d-none");
                }

                connectWebSocket();
            });
    }

    function startChat() {
        const formData = new URLSearchParams();
        const description = document.getElementById("chat-description").value.trim();

        if (!description) {
            alert("Опишіть питання");
            return;
        }

        if (!isAuthenticated) {
            const guestName = document.getElementById("chat-guest-name").value.trim();
            const guestEmail = document.getElementById("chat-guest-email").value.trim();

            if (!guestName) {
                alert("Вкажіть ваше ім’я");
                return;
            }

            if (!guestEmail) {
                alert("Вкажіть email");
                return;
            }

            formData.append("guest_name", guestName);
            formData.append("guest_email", guestEmail);
        }

        formData.append("topic", document.getElementById("chat-topic").value);
        formData.append("initial_description", description);

        fetch(createSessionUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken,
            },
            body: formData.toString()
        })
        .then(async response => {
            const data = await response.json();
            return { status: response.status, data };
        })
        .then(({ status, data }) => {
            if (status >= 400 || !data.ok) {
                alert("Не вдалося створити чат");
                return;
            }

            sessionId = data.session_id;
            switchToChatMode();
            clearMessages();

            if (newChatBtn) newChatBtn.classList.add("d-none");
            if (input) input.disabled = false;
            if (sendBtn) sendBtn.disabled = false;
            if (finishBtn) finishBtn.disabled = false;

            (data.messages || []).forEach(message => {
                renderMessage(message.id, message.author_type, message.text);
            });

            setStatus("Очікуємо підключення оператора");
            connectWebSocket();
            openPanel();
        });
    }

    function sendMessage() {
        const text = input.value.trim();
        if (!text || !socket || socket.readyState !== WebSocket.OPEN) return;

        socket.send(JSON.stringify({
            type: "message",
            sender_role: "user",
            sender_name: senderName,
            text: text
        }));

        input.value = "";
    }

    function finishChat() {
        if (!socket || socket.readyState !== WebSocket.OPEN) return;

        socket.send(JSON.stringify({
            type: "close_chat"
        }));
    }

    function resetChat() {
        if (socket) {
            socket.close();
            socket = null;
        }

        sessionId = null;
        clearMessages();
        switchToStartMode();

        if (input) {
            input.value = "";
            input.disabled = false;
        }

        if (sendBtn) sendBtn.disabled = false;
        if (finishBtn) finishBtn.disabled = false;
        if (newChatBtn) newChatBtn.classList.add("d-none");

        setStatus("Чат не розпочато");

        const descriptionField = document.getElementById("chat-description");
        if (descriptionField) descriptionField.value = "";

        const guestNameField = document.getElementById("chat-guest-name");
        if (guestNameField) guestNameField.value = "";

        const guestEmailField = document.getElementById("chat-guest-email");
        if (guestEmailField) guestEmailField.value = "";
    }

    if (launcher) launcher.addEventListener("click", openPanel);
    if (closeBtn) closeBtn.addEventListener("click", closePanel);
    if (startBtn) startBtn.addEventListener("click", startChat);
    if (sendBtn) sendBtn.addEventListener("click", sendMessage);
    if (finishBtn) finishBtn.addEventListener("click", finishChat);
    if (newChatBtn) newChatBtn.addEventListener("click", resetChat);

    if (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    }

    loadExistingSession();
});