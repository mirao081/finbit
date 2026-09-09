document.addEventListener("DOMContentLoaded", function () {

    const uploadButton = document.getElementById("uploadPictureBtn");
    const fileInput = document.querySelector(".file-upload-input");
    const preview = document.getElementById("profilePicturePreview");

    if (!uploadButton || !fileInput || !preview) {
        return;
    }
    uploadButton.addEventListener("click", function () {
        fileInput.click();
    });
    fileInput.addEventListener("change", function () {

        const file = this.files && this.files[0];

        if (!file) {
            return;
        }
        if (!file.type.startsWith("image/")) {
            alert("Please select a valid image file.");
            this.value = "";
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            alert("Please select an image smaller than 5 MB.");
            this.value = "";
            return;
        }
        const reader = new FileReader();

        reader.onload = function (event) {
            preview.src = event.target.result;
        };

        reader.readAsDataURL(file);
    });

});