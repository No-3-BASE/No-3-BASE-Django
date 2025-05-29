document.addEventListener("DOMContentLoaded", function () {
    const selectSection = document.getElementById("selectSection")
    const selectClass = document.getElementById("selectClass")
    const articleTitle = document.getElementById("articleTitle")
    const publishBtn = document.getElementById("publishBtn")

    function checkInputs() {
        const sectionVal = selectSection.value
        const classVal = selectClass.value
        const titleVal = articleTitle.value.trim()

        if (sectionVal && classVal && titleVal.length > 0) {
            publishBtn.disabled = false
            publishBtn.style.opacity = "1"
        } else {
            publishBtn.disabled = true
            publishBtn.style.opacity = "0.7"
        }
    }

    selectSection.addEventListener("change", checkInputs)
    selectClass.addEventListener("change", checkInputs)
    articleTitle.addEventListener("input", checkInputs)

    checkInputs()
})
