// Handle form submission events (optional additional behavior)
document.getElementById("text-translation-form").addEventListener("submit", (event) => {
    const inputText = document.getElementById("input-text").value.trim();
    if (!inputText) {
        event.preventDefault();
        alert("Please enter text to translate.");
    }
});

document.getElementById("file-translation-form").addEventListener("submit", (event) => {
    const fileInput = document.getElementById("uploaded_file").files[0];
    if (!fileInput) {
        event.preventDefault();
        alert("Please upload a file to translate.");
    }
});
