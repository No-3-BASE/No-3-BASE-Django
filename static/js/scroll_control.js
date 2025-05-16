document.addEventListener("DOMContentLoaded", function () {
    const announcementsContainer = document.getElementById("announcements")
    const scrollRightBtn = document.getElementById("scrollRightBtn")
    const scrollLeftBtn = document.getElementById("scrollLeftBtn")

    // 顯示/隱藏按鈕的邏輯
    function updateScrollButtons() {
        // 滾動到最左邊時隱藏左按鈕
        if (announcementsContainer.scrollLeft === 0) {
            scrollLeftBtn.style.color = 'transparent'
            scrollLeftBtn.style.pointerEvents = 'none'
        } else {
            scrollLeftBtn.style.color = 'var(--Text-Color)'
            scrollLeftBtn.style.pointerEvents = 'auto'
        }

        // 滾動到最右邊時隱藏右按鈕
        if (announcementsContainer.scrollLeft + announcementsContainer.clientWidth >= announcementsContainer.scrollWidth) {
            scrollRightBtn.style.color = 'transparent'
            scrollRightBtn.style.pointerEvents = 'none'
        } else {
            scrollRightBtn.style.color = 'var(--Text-Color)'
            scrollRightBtn.style.pointerEvents = 'auto'
        }
    }

    // 每次滾動後更新按鈕顯示狀態
    announcementsContainer.addEventListener('scroll', updateScrollButtons)

    // 初始時檢查並更新按鈕顯示狀態
    updateScrollButtons()

    // 向右滾動的按鈕
    scrollRightBtn.addEventListener("click", () => {
        announcementsContainer.scrollBy({
            left: 280,
            behavior: 'smooth' // 平滑滾動
        })
    })

    // 向左滾動的按鈕
    scrollLeftBtn.addEventListener("click", () => {
        announcementsContainer.scrollBy({
            left: -280,
            behavior: 'smooth' // 平滑滾動
        })
    })
})
