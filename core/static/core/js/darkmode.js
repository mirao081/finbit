document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("dark-mode-toggle");

    if (!toggle) {
        return;
    }


    function updateDarkModeButton() {

        const icon = toggle.querySelector("i");
        const text = toggle.querySelector(".dark-mode-text");

        const darkModeEnabled =
            document.body.classList.contains("dark-mode");


        toggle.setAttribute(
            "aria-pressed",
            darkModeEnabled ? "true" : "false"
        );


        if (darkModeEnabled) {

            if (icon) {
                icon.className = "fa-solid fa-sun";
            }

            if (text) {
                text.textContent = "Light";
            }

            toggle.setAttribute(
                "title",
                "Switch to Light Mode"
            );

        } else {

            if (icon) {
                icon.className = "fa-solid fa-moon";
            }

            if (text) {
                text.textContent = "Dark";
            }

            toggle.setAttribute(
                "title",
                "Switch to Dark Mode"
            );
        }
    }


    const savedMode =
        localStorage.getItem("finbit-dark-mode");


    if (savedMode === "dark") {

        document.body.classList.add("dark-mode");

    } else {

        document.body.classList.remove("dark-mode");

    }


    updateDarkModeButton();


    toggle.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");


        const darkModeEnabled =
            document.body.classList.contains("dark-mode");


        localStorage.setItem(
            "finbit-dark-mode",
            darkModeEnabled ? "dark" : "light"
        );


        updateDarkModeButton();

    });

});

