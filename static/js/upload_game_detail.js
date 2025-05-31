document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("saveBtnDown").addEventListener("click", function () {
        const boards = Array.from(document.querySelectorAll("select[name='section[]']"))
        const uids = Array.from(document.querySelectorAll("input[name='uid[]']"))

        const payload = []

        for (let i = 0; i < boards.length; i++) {
            const board = boards[i].value
            const uid = uids[i].value

            if (board && uid) {
                payload.push({ board, uid })
            }
        }

        if (payload.length === 0) {
            alert("請至少填寫一組 Section 與 UID")
            return
        }

        fetch("/profile_center/edit_game/edit/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ cards: payload })
        })
            .then(res => res.json())
            .then(data => {
                console.log("成功", data)
                alert("資料已送出！")
            })
            .catch(err => {
                console.error("錯誤", err)
                alert("發生錯誤，請檢查網路或伺服器")
            })
    })

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})