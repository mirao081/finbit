document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const toggleBtn = document.getElementById("dark-mode-toggle");

    const savedTheme = localStorage.getItem("adminTheme");

    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        updateButton(true);
    }

    toggleBtn?.addEventListener("click", () => {
        body.classList.toggle("dark-mode");

        const isDark = body.classList.contains("dark-mode");

        localStorage.setItem("adminTheme", isDark ? "dark" : "light");

        updateButton(isDark);
    });

    function updateButton(isDark) {
        if (!toggleBtn) return;

        toggleBtn.innerHTML = isDark
            ? '<i class="fas fa-sun"></i> Light Mode'
            : '<i class="fas fa-moon"></i> Dark Mode';
    }
});