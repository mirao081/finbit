function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        {
            pageLanguage: "en",
            includedLanguages: "af,ar,bg,ca,cs,da,de,el,en,es,et,fa,fi,fr,ga,he,hi,hr,hu,id,is,it,ja,ko,lt,lv,ms,mt,nl,no,pl,pt,ro,ru,sk,sl,sr,sv,sw,th,tr,uk,vi,zh-CN,zh-TW,yo,ha,ig,zu,bn,ta,te,ml,kn,pa",
            autoDisplay: true
        },
        "google_translate_element"
    );
    setupLanguageMenu();
    applySavedLanguage();
}

function applySavedLanguage() {
    const savedCookie = document.cookie
        .split("; ")
        .find((item) => item.startsWith("googtrans="));
    const savedLanguage = savedCookie?.split("/").pop();
    if (!savedLanguage || savedLanguage === "en") return;

    let attempts = 0;
    const timer = window.setInterval(() => {
        const select = document.querySelector("#google_translate_element select");
        const option = Array.from(select?.options || []).find(
            (item) => item.value.toLowerCase() === savedLanguage.toLowerCase()
        );

        if (option) {
            select.value = option.value;
            const event = document.createEvent("HTMLEvents");
            event.initEvent("change", true, true);
            select.dispatchEvent(event);
            window.clearInterval(timer);
        }

        attempts += 1;
        if (attempts >= 20) window.clearInterval(timer);
    }, 250);
}

const googleLanguages = [
    ["en", "English"], ["af", "Afrikaans"], ["ar", "Arabic"],
    ["bg", "Bulgarian"], ["ca", "Catalan"], ["cs", "Czech"],
    ["da", "Danish"], ["de", "German"], ["el", "Greek"],
    ["es", "Spanish"], ["fr", "French"], ["hi", "Hindi"],
    ["bn", "Bengali"], ["ur", "Urdu"], ["tr", "Turkish"],
    ["fa", "Persian"], ["pl", "Polish"], ["uk", "Ukrainian"],
    ["ro", "Romanian"], ["nl", "Dutch"], ["sv", "Swedish"],
    ["no", "Norwegian"], ["fi", "Finnish"], ["he", "Hebrew"],
    ["th", "Thai"], ["vi", "Vietnamese"], ["id", "Indonesian"],
    ["ms", "Malay"], ["sr", "Serbian"], ["hr", "Croatian"],
    ["hu", "Hungarian"], ["sk", "Slovak"], ["sl", "Slovenian"],
    ["et", "Estonian"], ["lv", "Latvian"], ["lt", "Lithuanian"],
    ["sw", "Swahili"], ["ta", "Tamil"], ["te", "Telugu"],
    ["ml", "Malayalam"], ["kn", "Kannada"], ["pa", "Punjabi"],
    ["si", "Sinhala"], ["km", "Khmer"], ["my", "Burmese"],
    ["ne", "Nepali"], ["it", "Italian"], ["pt", "Portuguese"],
    ["ru", "Russian"], ["ja", "Japanese"], ["ko", "Korean"],
    ["zh-CN", "Simplified Chinese"], ["zh-TW", "Traditional Chinese"]
];

function setupLanguageMenu() {
    const button = document.querySelector(".google-translate-button");
    const menu = document.getElementById("google-language-menu");
    if (!button || !menu || menu.dataset.ready === "true") return;

    menu.dataset.ready = "true";
    googleLanguages.forEach(([code, name]) => {
        const option = document.createElement("button");
        option.type = "button";
        option.className = "google-language-option";
        option.dataset.language = code;
        option.setAttribute("role", "menuitem");
        option.textContent = name;
        menu.appendChild(option);
    });

    button.addEventListener("click", () => {
        const open = menu.hidden;
        menu.hidden = !open;
        button.setAttribute("aria-expanded", String(open));
        if (open) menu.querySelector("button")?.focus();
    });

    menu.addEventListener("click", (event) => {
        const option = event.target.closest(".google-language-option");
        const select = document.querySelector("#google_translate_element select");
        if (!option) return;

        const languageCode = option.dataset.language;
        let appliedImmediately = false;

        if (select) {
            const googleOption = Array.from(select.options).find(
                (item) => item.value.toLowerCase() === languageCode.toLowerCase()
            );

            if (googleOption) {
                const widget = document.querySelector("#google_translate_element");
                const previousStyle = widget?.getAttribute("style");
                if (widget) {
                    widget.style.position = "fixed";
                    widget.style.width = "150px";
                    widget.style.height = "40px";
                    widget.style.opacity = "1";
                    widget.style.pointerEvents = "auto";
                    widget.style.overflow = "visible";
                }

                select.value = googleOption.value;
                const changeEvent = document.createEvent("HTMLEvents");
                changeEvent.initEvent("change", true, true);
                select.dispatchEvent(changeEvent);
                if (typeof select.onchange === "function") {
                    select.onchange.call(select, changeEvent);
                }

                if (widget) {
                    if (previousStyle === null) {
                        widget.removeAttribute("style");
                    } else {
                        widget.setAttribute("style", previousStyle);
                    }
                }
                appliedImmediately = true;
            }
        }

        if (languageCode === "en") {
            document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
        } else {
            document.cookie = `googtrans=/en/${languageCode}; path=/`;
        }

        menu.hidden = true;
        button.setAttribute("aria-expanded", "false");
        window.setTimeout(() => {
            window.location.reload();
        }, appliedImmediately ? 600 : 0);
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".google-translate")) {
            menu.hidden = true;
            button.setAttribute("aria-expanded", "false");
        }
    });
}

function removeGoogleToolbar() {
    const cleanToolbar = () => {
        document.querySelectorAll("body > .skiptranslate").forEach((wrapper) => {
            if (
                wrapper.id !== "google_translate_element" &&
                !wrapper.querySelector("#google_translate_element")
            ) {
                wrapper.remove();
            }
        });

        document.querySelectorAll("iframe.goog-te-banner-frame").forEach((frame) => {
            frame.remove();
        });

        document.documentElement.style.marginTop = "0";
        document.documentElement.style.top = "0";
        document.body.style.marginTop = "0";
        document.body.style.top = "0";
    };

    cleanToolbar();

    if (!document.body.dataset.googleToolbarObserver) {
        document.body.dataset.googleToolbarObserver = "true";
        new MutationObserver(cleanToolbar).observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}