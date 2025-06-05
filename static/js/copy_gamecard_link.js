document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".copyLink").forEach(button => {
        button.addEventListener("click", function () {
            const path = button.dataset.link

            navigator.clipboard.writeText(path)
                .then(() => {
                    alert("識別連結已複製，可用於外部通訊")
                })
                .catch(err => {
                    console.error("複製失敗", err)
                    alert("複製失敗")
                })
        })
    })
})
