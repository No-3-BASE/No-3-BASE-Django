const STATIC_URL = "/static/"

const icons = {
    light: {
        theme: STATIC_URL + "assets/images/Tool_3D5272/moon.png",
        message: STATIC_URL + "assets/images/Tool_3D5272/message.png",
        notice: STATIC_URL + "assets/images/Tool_3D5272/notice.png",
        height: "20px",
    },
    dark: {
        theme: STATIC_URL + "assets/images/Tool_B56387/sun.png",
        message: STATIC_URL + "assets/images/Tool_B56387/message.png",
        notice: STATIC_URL + "assets/images/Tool_B56387/notice.png",
        height: "22px",
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("No3BASE-theme")
    const html = document.documentElement

    if (savedTheme) {
        html.setAttribute("data-theme", savedTheme)
    }
    else {
        const prefersLight = window.matchMedia("(prefers-color-scheme: ligth)").matches
        html.setAttribute("data-theme", prefersLight ? "light" : "dark")
    }

    const themeButtonIcon = document.getElementById("themeImg")
    const messageImg = document.getElementById("messageImg")
    const noticeImg = document.getElementById("noticeImg")

    if (html.getAttribute("data-theme") === "light") {
        themeButtonIcon.src = icons.light.theme
        themeButtonIcon.style.height = icons.light.height
        messageImg.src = icons.light.message
        noticeImg.src = icons.light.notice
    }
    else {
        themeButtonIcon.src = icons.dark.theme
        themeButtonIcon.style.height = icons.dark.height
        messageImg.src = icons.dark.message
        noticeImg.src = icons.dark.notice
    }
})

function toggleTheme() {
    const html = document.documentElement
    const themeButtonIcon = document.getElementById("themeImg")
    const messageImg = document.getElementById("messageImg")
    const noticeImg = document.getElementById("noticeImg")

    const currentTheme = html.getAttribute("data-theme")
    const newTheme = currentTheme === "light" ? "dark" : "light"

    localStorage.setItem("No3BASE-theme", newTheme)
    html.setAttribute("data-theme", newTheme)

    const themeSet = icons[newTheme]
    themeButtonIcon.src = themeSet.theme
    themeButtonIcon.style.height = themeSet.height
    messageImg.src = themeSet.message
    noticeImg.src = themeSet.notice

    console.log("主題已切換為:", newTheme)
}