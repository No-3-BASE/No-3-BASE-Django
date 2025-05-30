document.addEventListener('DOMContentLoaded', function () {
    const inputMessage = document.getElementById('inputMessage')
    const largeMessage = document.getElementById('largeMessage')
    const openBtn = document.getElementById('open')
    const closeBtn = document.getElementById('close')
    const smallTextarea = document.getElementById('smallTextarea')
    const largeTextarea = document.getElementById('largeTextarea')

    openBtn.addEventListener('click', function (e) {
        e.stopPropagation()
        largeTextarea.value = smallTextarea.value
        inputMessage.style.display = 'none'
        largeMessage.style.display = 'flex'
        largeTextarea.focus()
    })

    function collapse() {
        smallTextarea.value = largeTextarea.value
        largeMessage.style.display = 'none'
        inputMessage.style.display = 'block'
    }

    closeBtn.addEventListener('click', function (e) {
        e.stopPropagation()
        collapse()
    })

    document.addEventListener('click', function (e) {
        if (largeMessage.style.display === 'flex' && !largeMessage.contains(e.target)) {
            collapse()
        }
    })
})
