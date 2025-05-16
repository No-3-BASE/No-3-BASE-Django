function toggleMenu(menuId) {
    const menu = document.getElementById(menuId)

    if (!menu) {
        console.error('Menu not found!')
        return
    }

    menu.style.display = (menu.style.display === 'flex' || menu.style.display === 'block') ? 'none' : 'flex'

    const allMenus = document.querySelectorAll('.menu')
    allMenus.forEach(m => {
        if (m !== menu) {
            m.style.display = 'none'
        }
    })
}

document.addEventListener('click', function (event) {
    if (!event.target.closest('.menuBtn')) {
        document.querySelectorAll('.menu').forEach(menu => {
            menu.style.display = 'none'
        })
    }
})
