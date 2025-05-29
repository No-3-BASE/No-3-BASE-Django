document.addEventListener("DOMContentLoaded", function () {
    const selectSection = document.getElementById('selectSection')
    const selectClass = document.getElementById('selectClass')

    const sectionTomSelect = new TomSelect(selectSection, {
        create: false,
        placeholder: '選擇板塊'
    })

    const classTomSelect = new TomSelect(selectClass, {
        create: false,
        placeholder: '選擇類別'
    })

    const initialCategoryId = document.getElementById('initialCategoryId')?.value;

    sectionTomSelect.on('change', function (value) {
        classTomSelect.clearOptions()
        classTomSelect.clear(true)

        fetch(`/article/ajax/load_categories/?section_id=${value}`, {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                classTomSelect.clearOptions()
                classTomSelect.addOption({ value: '', text: '選擇類別', disabled: true })
                classTomSelect.refreshOptions(false)

                data.forEach(category => {
                    classTomSelect.addOption({ value: category.id, text: category.name })
                })

                if (initialCategoryId) {
                    classTomSelect.setValue(initialCategoryId)
                }

                classTomSelect.refreshOptions(false)
            })
    })

    const selectedSectionValue = selectSection.value
    if (selectedSectionValue) {
        sectionTomSelect.setValue(selectedSectionValue)
    }

})
