document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('mark').addEventListener('click', function () {
        const button = this;
        const sectionId = button.getAttribute('data-section-id');
        const articleId = button.getAttribute('data-article-id');
        const markCountElem = document.getElementById('articleMark');
        let markCount = parseInt(markCountElem.textContent);

        fetch(`/section/${sectionId}/article/${articleId}/mark_toggle/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                    if (data.marked) {
                        markCount++;
                        document.getElementById('mark').innerText = "已收藏"
                    } else {
                        markCount--;
                        document.getElementById('mark').innerText = "收藏"
                    }
                    markCountElem.textContent = markCount;
                } else {
                    alert('按讚失敗，請稍後再試');
                }
            })
            .catch(() => alert('網路錯誤'));

    });

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