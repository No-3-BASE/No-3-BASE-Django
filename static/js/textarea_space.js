document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById('articleTitle')

    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 'px'

    textarea.addEventListener('input', function () {
        this.style.height = 'auto'
        this.style.height = this.scrollHeight + 'px'
    })
})