document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("recovery-toggle");
    const codeInput = document.getElementById("code");
    const codeLabel = document.getElementById("code-label");
    const description = document.getElementById(
        "verification-description"
    );

    if (
        !toggle ||
        !codeInput ||
        !codeLabel ||
        !description
    ) {
        return;
    }

    let recoveryMode = false;

    toggle.addEventListener("click", function () {

        recoveryMode = !recoveryMode;

        if (recoveryMode) {

            codeLabel.textContent = "Recovery Code";

            description.textContent =
                "Enter one of your unused recovery codes to continue.";

            codeInput.value = "";
            codeInput.placeholder = "XXXX-XXXX-XXXX";
            codeInput.maxLength = 100;

            codeInput.removeAttribute("inputmode");

            codeInput.setAttribute(
                "autocomplete",
                "off"
            );

            toggle.textContent =
                "Use authenticator app instead";

        } else {

            codeLabel.textContent =
                "Authentication Code";

            description.textContent =
                "Enter the 6-digit verification code from your authenticator app to continue.";

            codeInput.value = "";
            codeInput.placeholder = "000000";
            codeInput.maxLength = 6;

            codeInput.setAttribute(
                "inputmode",
                "numeric"
            );

            codeInput.setAttribute(
                "autocomplete",
                "one-time-code"
            );

            toggle.textContent =
                "Use a recovery code instead";
        }

        codeInput.focus();
    });

});