let knownWaitingSessionIds = new Set();

function initKnownSessions() {
    knownWaitingSessionIds = new Set(
        Array.from(document.querySelectorAll("#waiting-sessions-container [data-session-id]"))
            .map(node => node.dataset.sessionId)
    );
}

function claimChat(sessionId) {
    fetch(`/support-chat/operator/claim/${sessionId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": window.CSRF_TOKEN,
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.ok) return;

        loadDashboardData();
        window.open(`/support-chat/operator/room/${sessionId}/`, "_blank");
    });
}

function renderWaitingSessions(sessions) {
    const container = document.getElementById("waiting-sessions-container");
    container.innerHTML = "";

    if (!sessions.length) {
        container.innerHTML = '<p id="waiting-empty-text">Немає чатів у черзі.</p>';
        return;
    }

    sessions.forEach(session => {
        const card = document.createElement("div");
        card.className = "card mb-3";
        card.dataset.sessionId = session.id;

        card.innerHTML = `
            <div class="card-body">
                <p><strong>Користувач:</strong> ${session.customer_display_name}</p>
                <p><strong>Тема:</strong> ${session.topic_display}</p>
                <p><strong>Опис:</strong> ${session.initial_description}</p>
                <button class="btn btn-primary" onclick="claimChat(${session.id})">
                    Підключитися
                </button>
            </div>
        `;

        container.appendChild(card);
    });
}

function renderActiveSessions(sessions) {
    const container = document.getElementById("active-sessions-container");
    container.innerHTML = "";

    if (!sessions.length) {
        container.innerHTML = '<p id="active-empty-text">Немає активних чатів.</p>';
        return;
    }

    sessions.forEach(session => {
        const card = document.createElement("div");
        card.className = "card mb-3";
        card.dataset.sessionId = session.id;

        card.innerHTML = `
            <div class="card-body">
                <p><strong>Користувач:</strong> ${session.customer_display_name}</p>
                <p><strong>Тема:</strong> ${session.topic_display}</p>
                <a href="/support-chat/operator/room/${session.id}/" class="btn btn-outline-primary">
                    Відкрити чат
                </a>
            </div>
        `;

        container.appendChild(card);
    });
}

function loadDashboardData() {
    fetch("/support-chat/operator/dashboard-data/")
        .then(response => response.json())
        .then(data => {
            const waitingSessions = data.waiting_sessions || [];
            const activeSessions = data.active_sessions || [];

            const newWaitingIds = new Set(waitingSessions.map(item => String(item.id)));

            waitingSessions.forEach(session => {
                const sessionId = String(session.id);

                if (!knownWaitingSessionIds.has(sessionId) && window.showAppToast) {
                    window.showAppToast(
                        "Новий чат у черзі",
                        `${session.customer_display_name} очікує підключення.`,
                        "info"
                    );
                }
            });

            knownWaitingSessionIds = newWaitingIds;

            renderWaitingSessions(waitingSessions);
            renderActiveSessions(activeSessions);
        });
}

document.addEventListener("DOMContentLoaded", function () {
    initKnownSessions();
    setInterval(loadDashboardData, 5000);
});