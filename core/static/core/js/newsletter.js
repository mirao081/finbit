document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("newsletter-form");
    const messageBox = document.getElementById("newsletter-message");

    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        formData.append("newsletter", "1");

        try {
            const response = await fetch(form.action || window.location.href, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (data.status === "ok") {
                messageBox.innerText = "✅ Thank you for subscribing!";
                messageBox.style.color = "lime";
                form.reset();

            } else if (data.status === "exists") {
                messageBox.innerText = "ℹ️ You're already subscribed!";
                messageBox.style.color = "orange";

            } else {
                const error =
                    data.errors?.email?.[0] || "Something went wrong.";

                messageBox.innerText = "❌ " + error;
                messageBox.style.color = "red";
            }

        } catch (error) {
            console.error(error);
            messageBox.innerText = "❌ Unable to subscribe. Please try again.";
            messageBox.style.color = "red";
        }
    });
});