const STATIC_URL = "/static/"

const darkcss = STATIC_URL + "css/global_dark.css"
const lightcss = STATIC_URL + "css/global_light.css"

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
        height: "24px",
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

    console.log("themeLink href 設定為:", html.documentElement)
})
//下面是toolbar圖標和切換
/*
document.addEventListener("toolBarLoaded", function () {
    const themeLink = document.getElementById("themeStyleSheet")
    const themeButtonIcon = document.getElementById("themeImg")
    const messageImg = document.getElementById("messageImg")
    const noticeImg = document.getElementById("noticeImg")

    if (themeLink.href.includes("light")) {
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
    const themeLink = document.getElementById("themeStyleSheet")
    const themeButtonIcon = document.getElementById("themeImg")
    const messageImg = document.getElementById("messageImg")
    const noticeImg = document.getElementById("noticeImg")

    if (themeLink.href.includes("light")) {
        themeLink.href = darkcss
        localStorage.setItem("theme", darkcss)
        themeButtonIcon.src = icons.dark.theme
        themeButtonIcon.style.height = icons.dark.height
        messageImg.src = icons.dark.message
        noticeImg.src = icons.dark.notice
    }
    else {
        themeLink.href = lightcss
        localStorage.setItem("theme", lightcss)
        themeButtonIcon.src = icons.light.theme
        themeButtonIcon.style.height = icons.light.height
        messageImg.src = icons.light.message
        noticeImg.src = icons.light.notice
    }


    console.log("themeLink href 設定為:", themeLink.href)
}
*/