function copyRecoveryCodes() {
    const textarea = document.getElementById("recoveryCodesText");
    const button = document.querySelector(".btn-copy-codes");

    if (!textarea || !button) {
        return;
    }

    const codes = textarea.value.trim();

    if (!codes) {
        return;
    }

    const original = button.innerHTML;

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(codes)
            .then(function () {
                showCopied(button, original);
            })
            .catch(function () {
                fallbackCopy(textarea, button, original);
            });
    } else {
        fallbackCopy(textarea, button, original);
    }
}

function fallbackCopy(textarea, button, original) {
    textarea.focus();
    textarea.select();

    try {
        document.execCommand("copy");
        showCopied(button, original);
    } catch (error) {
        console.error("Unable to copy recovery codes:", error);
    }

    window.getSelection().removeAllRanges();
}

function showCopied(button, original) {
    button.innerHTML = '<i class="fas fa-check"></i> Copied';

    setTimeout(function () {
        button.innerHTML = original;
    }, 2000);
}