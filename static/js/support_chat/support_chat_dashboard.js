async function claimChat(sessionId) {
    const card = document.querySelector(`div[data-session-id="${sessionId}"]`);
    const button = card ? card.querySelector('button') : null;

    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>...';
    }

    try {
        const response = await fetch(`/support/operator/claim/${sessionId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN,
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            window.location.href = `/support/operator/room/${sessionId}/`;
        } else {
            const data = await response.json();
            alert('Помилка: ' + (data.error || 'Не вдалося підключитися'));

            if (button) {
                button.disabled = false;
                button.innerText = 'Підключитися';
            }
        }
    } catch (error) {
        console.error('Помилка запиту:', error);
        alert('Сталася помилка на сервері.');

        if (button) {
            button.disabled = false;
            button.innerText = 'Підключитися';
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Панель оператора готова до роботи.");
});