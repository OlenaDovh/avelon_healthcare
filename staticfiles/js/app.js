window.showAppToast = function(title, text, variant = "success", timeout = 4000) {
    const container = document.getElementById("app-toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `app-toast app-toast--${variant}`;

    toast.innerHTML = `
        <div class="app-toast-title">${title}</div>
        <p class="app-toast-text">${text}</p>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, timeout);
};