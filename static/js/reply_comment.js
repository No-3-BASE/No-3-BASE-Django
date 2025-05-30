document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.replyBtn').forEach(btn => {
        btn.addEventListener('click', function () {
            const id = this.dataset.id
            const floor = this.dataset.floor

            const replyBox = document.getElementById('reply')
            const replyLink = replyBox.querySelector('a.floorLink')
            const hiddenInput = document.getElementById('parent_id')

            replyBox.style.display = 'block'
            replyLink.href = `#${id}`
            replyLink.textContent = `@${floor}樓`
            hiddenInput.value = id
        })
    })

    const closeBtn = document.getElementById('removeReply')
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            document.getElementById('reply').style.display = 'none'
            document.getElementById('parent_id').value = ''
        })
    }

    const commentsList = document.getElementById('commentsList')

    commentsList.addEventListener('click', (e) => {
        const btn = e.target.closest('.replyBtn')
        if (!btn) return

        const commentId = btn.getAttribute('data-id')
        const floor = btn.getAttribute('data-floor')

        document.getElementById('parent_id').value = commentId

        const replyP = document.getElementById('reply')
        const floorLink = replyP.querySelector('.floorLink')
        floorLink.textContent = `@${floor}樓`
        floorLink.href = `#${commentId}`
        replyP.style.display = 'block'

        document.getElementById('inputMessage').style.display = 'block'
        document.getElementById('largeMessage').style.display = 'none'

        document.getElementById('smallTextarea').focus()

        window.scrollTo(0, document.getElementById('commentForm').offsetTop - 80)
    })

})
