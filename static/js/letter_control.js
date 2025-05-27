document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('sign')
    const counter = document.getElementById('charCount')
    const maxLength = 80

    const updateCounter = () => {
        if (textarea.value.length > maxLength) {
            textarea.value = textarea.value.slice(0, maxLength)
        }
        counter.textContent = textarea.value.length
    };

    textarea.addEventListener('input', updateCounter)

    updateCounter()
})