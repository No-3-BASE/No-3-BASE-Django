document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.filterBtn')
    const sections = document.querySelectorAll('.section')

    let selectedPlatforms = new Set()

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.getAttribute('data-value')

            // 切換選擇狀態
            if (selectedPlatforms.has(value)) {
                selectedPlatforms.delete(value)
                button.classList.remove('selected')
            } else {
                selectedPlatforms.add(value)
                button.classList.add('selected')
            }

            // 顯示或隱藏 section
            sections.forEach(section => {
                const platform = section.getAttribute('data-platform')
                if (selectedPlatforms.size === 0 || selectedPlatforms.has(platform)) {
                    section.style.display = ''
                } else {
                    section.style.display = 'none'
                }
            })
        })
    })
})
