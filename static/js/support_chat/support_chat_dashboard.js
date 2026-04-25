/**
 * Функція для підключення до чату.
 * Використовує точні шляхи з вашого urls.py
 */
async function claimChat(sessionId) {
    const card = document.querySelector(`div[data-session-id="${sessionId}"]`);
    const button = card ? card.querySelector('button') : null;

    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
    }

    try {
        // Шлях згідно з вашим urls.py: operator/claim/<id>/
        const response = await fetch(`/operator/claim/${sessionId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN,
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            // Шлях згідно з вашим urls.py: operator/room/<id>/
            window.location.href = `/operator/room/${sessionId}/`;
        } else {
            const data = await response.json();
            alert('Помилка: ' + (data.error || 'Не вдалося підключитися'));
            if (button) {
                button.disabled = false;
                button.innerText = 'Підключитися';
            }
        }
    } catch (error) {
        console.error('Помилка виконання:', error);
        if (button) {
            button.disabled = false;
            button.innerText = 'Підключитися';
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("Dashboard ready");
});