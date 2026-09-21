document.addEventListener("DOMContentLoaded", function () {

    window.copyRecoveryCodes = async function () {

        const codes = Array.from(
            document.querySelectorAll(".recovery-code code")
        ).map(function (element) {
            return element.textContent.trim();
        });

        if (!codes.length) {
            return;
        }

        const text = codes.join("\n");

        try {

            await navigator.clipboard.writeText(text);

            const button = document.querySelector(
                ".recovery-actions .two-factor-btn"
            );

            if (button) {

                const originalText = button.innerHTML;

                button.innerHTML =
                    '<i class="fas fa-check"></i> Copied';

                setTimeout(function () {
                    button.innerHTML = originalText;
                }, 2000);

            }

        } catch (error) {

            const textarea = document.createElement("textarea");

            textarea.value = text;

            textarea.style.position = "fixed";
            textarea.style.opacity = "0";

            document.body.appendChild(textarea);

            textarea.select();

            document.execCommand("copy");

            textarea.remove();

        }

    };

});