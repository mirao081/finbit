document.addEventListener("DOMContentLoaded", function () {

    document.addEventListener("click", function (event) {

        const question = event.target.closest(".faq-question");

        if (!question) {
            return;
        }

        const faqItem = question.closest(".faq-item");

        if (!faqItem) {
            return;
        }

        document.querySelectorAll(".faq-item.active").forEach(function (item) {

            if (item !== faqItem) {
                item.classList.remove("active");
            }

        });

        faqItem.classList.toggle("active");

    });

});