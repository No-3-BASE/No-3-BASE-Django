async function loadSectionOptions(selectEl, selectedValue = null) {
    try {
        const res = await fetch('/profile_center/api/sections/')
        const sections = await res.json()

        selectEl.innerHTML = '<option value="" selected disabled hidden>請選擇板塊或輸入名稱</option>'

        sections.forEach(section => {
            const opt = document.createElement('option')
            opt.value = section.id
            opt.textContent = section.name
            if (section.id === selectedValue) {
                opt.selected = true
            }
            selectEl.appendChild(opt)
        })

        const tom = new TomSelect(selectEl, {
            create: true,
            placeholder: '請選擇板塊或輸入名稱',
        })

        if (selectedValue && !sections.some(s => s.id === selectedValue)) {
            tom.addOption({ value: selectedValue, text: selectedValue })
            tom.setValue(selectedValue)
        }

    } catch (err) {
        console.error("無法載入板塊資料", err)
    }
}

function renderCard(card) {
    const container = document.getElementById("selectFields")

    const wrapper = document.createElement("div")
    wrapper.className = "field-container"

    wrapper.innerHTML = `
        <div class="editField">
            <select name="section[]" class="select-input" value="${card.id}"></select>
            <input name="uid[]" class="gameUID" type="text" value="${card.uid}" placeholder="請輸入遊戲UID">
        </div>
        <button type="button" class="removeBtn">✕</button>
    `

    container.appendChild(wrapper)

    const selectEl = wrapper.querySelector('select.select-input')
    const sectionValue = card.section || card.customName || ''
    loadSectionOptions(selectEl, sectionValue)
}

document.addEventListener("DOMContentLoaded", function () {
    const cards = JSON.parse(document.getElementById("initial-cards").textContent)
    console.log(cards)
    cards.forEach(renderCard)

    document.getElementById("addBtn").addEventListener("click", function () {
        renderCard({ uid: "", section: "" })
    })

    document.getElementById("selectFields").addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("removeBtn")) {
            const fieldContainer = e.target.closest(".field-container")
            if (fieldContainer) fieldContainer.remove()
        }
    })
})