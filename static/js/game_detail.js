async function loadSectionOptions(selectEl) {
    try {
        const res = await fetch('/profile_center/api/sections/')
        const sections = await res.json()

        selectEl.innerHTML = '<option value="" disabled selected>請選擇板塊或輸入名稱</option>'

        sections.forEach(section => {
            const opt = document.createElement('option')
            opt.value = section.id
            opt.textContent = section.name
            selectEl.appendChild(opt)
        })

        new TomSelect(selectEl, {
            create: true,
            placeholder: '請選擇板塊或輸入名稱'
        })

    } catch (err) {
        console.error("無法載入板塊資料", err)
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const initialSelects = document.querySelectorAll('.select-input')
    initialSelects.forEach(select => loadSectionOptions(select))

    document.getElementById("addBtn").addEventListener("click", function () {
        const container = document.getElementById("selectFields")

        const wrapper = document.createElement("div")
        wrapper.className = "field-container"

        wrapper.innerHTML = `
        <div class="editField">
            <select name="section[]" class="select-input"></select>
            <input name="uid[]" class="gameUID" type="text" placeholder="請輸入遊戲UID">
        </div>
        <button type="button" class="removeBtn">✕</button>
        `

        container.appendChild(wrapper)

        const newSelect = wrapper.querySelector('select.select-input')
        loadSectionOptions(newSelect)
    })

    document.getElementById("selectFields").addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("removeBtn")) {
            const fieldContainer = e.target.closest(".field-container")
            if (fieldContainer) fieldContainer.remove()
        }
    })
})