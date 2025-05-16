document.addEventListener("DOMContentLoaded", () => {
    fetch("tool_bar.html")
        .then(res => res.text())
        .then(html => {
            document.getElementById("toolBar").innerHTML = html
            document.dispatchEvent(new Event("toolBarLoaded"))
        })
        .catch(err => console.log("載入失敗", err))
})
