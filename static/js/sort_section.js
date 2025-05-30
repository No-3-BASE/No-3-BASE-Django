document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.filterBtn')
    const sections = document.querySelectorAll('.section')
    const searchField = document.getElementById('searchSectionsField')
    const searchButton = document.getElementById('searchSectionButton')

    let selectedPlatform = 'all'
    let searchKeyword = ''
    let isSearching = false

    let selectedPlatforms = new Set()

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.getAttribute('data-value')

            if (selectedPlatforms.has(value)) {
                selectedPlatforms.delete(value)
                button.classList.remove('selected')
            } else {
                selectedPlatforms.add(value)
                button.classList.add('selected')
            }

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

    function filterSections() {
        sections.forEach(section => {
            const platform = section.getAttribute('data-platform')
            const name = section.querySelector('.sectionA').textContent.toLowerCase()

            const matchPlatform = selectedPlatform === 'all' || platform === selectedPlatform
            const matchKeyword = name.includes(searchKeyword)

            if (matchPlatform && matchKeyword) {
                section.style.display = ''
            } else {
                section.style.display = 'none'
            }
        })
    }

    function showAllSections() {
        sections.forEach(section => {
            section.style.display = ''
        })
    }

    searchButton.addEventListener('click', () => {
        if (!isSearching) {
            searchKeyword = searchField.value.trim().toLowerCase()
            isSearching = true
            searchButton.textContent = '取消'
            filterSections()
        } else {
            isSearching = false
            searchKeyword = ''
            searchField.value = ''
            searchButton.textContent = '搜尋'
            selectedPlatform = 'all'

            buttons.forEach(btn => btn.classList.remove('selected'))

            showAllSections()
        }
    })

    searchField.addEventListener('input', () => {
        if (isSearching) {
            isSearching = false
            searchButton.textContent = '搜尋'
            searchKeyword = ''
        }
    })
})
