document.addEventListener('DOMContentLoaded', function () {
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

    const followButtons = document.querySelectorAll('.followToggleBtn')

    followButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const isFollowing = btn.classList.contains('playerFollow') || btn.classList.contains('isfollow')
            const action = isFollowing ? 'unfollow' : 'follow'
            const toggleUrl = btn.dataset.url
            const targetId = btn.dataset.id

            fetch(toggleUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    target_id: targetId,
                    action: action
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // 樣式 A：playerFollow <-> playerUnfollow
                        if (btn.classList.contains('playerFollow') || btn.classList.contains('playerUnfollow')) {
                            if (action === 'follow') {
                                btn.classList.remove('playerUnfollow')
                                btn.classList.add('playerFollow')
                                btn.textContent = '已關注'
                            } else {
                                btn.classList.remove('playerFollow')
                                btn.classList.add('playerUnfollow')
                                btn.textContent = '關注'
                            }
                        }
                        // 樣式 B：isFollow <-> unFollow
                        else if (btn.classList.contains('isfollow') || btn.classList.contains('unfollow')) {
                            if (action === 'follow') {
                                btn.classList.remove('unfollow')
                                btn.classList.add('isfollow')
                                btn.textContent = '已關注'
                            } else {
                                btn.classList.remove('isfollow')
                                btn.classList.add('unfollow')
                                btn.textContent = '關注'
                            }
                        }
                    } else {
                        alert('通訊錯誤：' + data.message)
                    }
                })
                .catch(error => {
                    console.error('錯誤：', error)
                    alert('無法連接基地')
                })
        })
    })
})
