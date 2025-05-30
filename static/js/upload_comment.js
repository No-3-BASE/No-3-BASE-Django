window.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('commentForm')
    const commentInput = form.querySelector('textarea[name="comment"]')
    const commentsList = document.getElementById('commentsList')

    function getCookie(name) {
        let cookieValue = null
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';')
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim()
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
                }
            }
        }
        return cookieValue
    }
    const csrftoken = getCookie('csrftoken')

    form.addEventListener('submit', function (e) {
        e.preventDefault()

        const comment = commentInput.value.trim()
        if (!comment) {
            alert('訊號無效：請輸入有效內容以啟動傳輸')
            return
        }

        const formData = new FormData()
        formData.append('comment', comment)

        const parentId = document.getElementById('parent_id').value
        if (parentId) {
            formData.append('parent', parentId)
        }

        fetch(window.location.pathname + 'comment/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error)
                    return
                }
                const newCommentHTML = `
                <div class="articleMessage">
                    <div class="player">
                        <div class="playerDetail">
                            <img src="${data.authorPhoto}" alt="">
                            <div>
                                <a class="playerLink" href="">
                                    <p class="playerName">${data.author}</p>
                                </a>
                                <p class="playerDays">進入基地 ${data.authorDays} 天<span class="level">Lv. ${data.authorLevel}</span></p>
                            </div>
                        </div>
                        <p class="floor" id="16">${data.floor}樓</p>
                        <p class="signTitle">個性簽名</p>
                        <p class="sign">${data.authorSlogan}</p>
                    </div>
                    <div class="messageField">
                        <div class="addBtn">
                            <p class="messageContent">
                                ${data.parentFloor ? `<a class="floorLink" href="#${data.parentId}">@${data.parentFloor}樓</a>` : ''}
                                ${data.content}
                            </p>
                            <button class="menuBtn" type="button" onclick="toggleMenu('${data.id}')">⋮</button>
                            <div id="${data.id}2" class="menu">
                                <a>檢舉</a>
                            </div>
                        </div>
                        <div class="downDetail">
                            <div>
                                <p class="time">Activated：${data.createAt}</p>
                            </div>
                            <div class="articleDetail">
                                <button class="articleBtn replyBtn" data-id="${data.id}" data-floor="${data.floor}">回覆</button>
                                <p>獲讚　0</p>
                                <button class="articleBtn">按讚</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="line"></div>
                `
                commentsList.insertAdjacentHTML('beforeend', newCommentHTML)

                commentInput.value = ''

                commentsList.scrollTop = commentsList.scrollHeight
                window.scrollTo(0, document.body.scrollHeight)

                document.getElementById('reply').style.display = 'none'
                document.getElementById('parent_id').value = ''
            })
            .catch(err => {
                alert('送出失敗，請稍後再試')
                console.error(err)
            })
    })
})