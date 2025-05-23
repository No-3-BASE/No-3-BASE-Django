document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".copyUID").forEach(button => {
        button.addEventListener("click", function () {
            const uidElement = this.closest("tr").querySelector(".gameUID")
            const uid = uidElement.textContent.trim()

            navigator.clipboard.writeText(uid).then(() => {
                alert("UID 已複製：" + uid)
            }).catch(err => {
                console.error("複製失敗：", err)
                alert("複製失敗")
            })
        })
    })
})