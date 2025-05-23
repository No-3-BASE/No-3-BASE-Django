document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("saveBtnDown").addEventListener("click", function () {
        const boards = Array.from(document.querySelectorAll("select[name='board[]']")).map(s => s.value)
        const uids = Array.from(document.querySelectorAll("input[name='uid[]']")).map(i => i.value)

        const payload = {
            boards: boards,
            uids: uids
        }

        fetch("/player/card/edit/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        })
            .then(res => res.json())
            .then(data => {
                console.log("成功", data)
                alert("資料已送出！")
            })
            .catch(err => {
                console.error("錯誤", err)
            })
    })
})