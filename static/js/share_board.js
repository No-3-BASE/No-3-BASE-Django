document.addEventListener('DOMContentLoaded', function () {
    var shareBtn = document.getElementById('shareBtn')
    var shareBoard = document.getElementById('shareBoard')

    shareBtn.addEventListener('click', function (event) {
        event.stopPropagation()
        var isVisible = shareBoard.style.display === 'block'
        shareBoard.style.display = isVisible ? 'none' : 'block'
    })

    document.addEventListener('click', function (event) {
        var isClickInside = shareBoard.contains(event.target) || shareBtn.contains(event.target)
        if (!isClickInside) {
            shareBoard.style.display = 'none'
        }
    })
})