document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('like').addEventListener('click', function () {
        const button = this;
        const sectionId = button.getAttribute('data-section-id');
        const articleId = button.getAttribute('data-article-id');
        const likeCountElem = document.getElementById('articleLike');
        let likeCount = parseInt(likeCountElem.textContent);

        fetch(`/section/${sectionId}/article/${articleId}/like_toggle/`, {
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
                    if (data.liked) {
                        likeCount++;
                        document.getElementById('like').innerText = "已讚"
                    } else {
                        likeCount--;
                        document.getElementById('like').innerText = "按讚"
                    }
                    likeCountElem.textContent = likeCount;
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