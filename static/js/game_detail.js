document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.select-input').forEach(el => {
        new TomSelect(el, {
            create: true,
            placeholder: '請選擇板塊或輸入名稱'
        })
    })

    document.getElementById("addBtn").addEventListener("click", function () {
        const container = document.getElementById("selectFields")

        const wrapper = document.createElement("div")
        wrapper.className = "field-container"

        wrapper.innerHTML = `
        <div class="editField">
            <select name="board[]" class="select-input">
                <option value="" selected disabled hidden>請選擇板塊或輸入名稱</option>
                <option value="rpg">RPG 遊戲</option>
                <option value="action">動作遊戲</option>
                <option value="puzzle">解謎遊戲</option>
                 <option value="horror">恐怖遊戲</option>
             </select>
            <input name="uid[]" class="gameUID" type="text" placeholder="請輸入遊戲UID">
        </div>
        <button type="button" class="removeBtn">✕</button>
        `

        container.appendChild(wrapper)

        const newSelect = wrapper.querySelector('select.select-input')
        new TomSelect(newSelect, {
            create: true,
            placeholder: '請選擇板塊或輸入名稱'
        })
    })

    document.getElementById("selectFields").addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("removeBtn")) {
            const fieldContainer = e.target.closest(".field-container")
            if (fieldContainer) {
                fieldContainer.remove()
            }
        }
    })
})
