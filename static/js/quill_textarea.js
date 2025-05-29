const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['blockquote', 'code-block'],
    [{ header: 1 }, { header: 2 }],
    [{ list: 'ordered' }, { list: 'bullet' }],
    [{ script: 'sub' }, { script: 'super' }],
    [{ indent: '-1' }, { indent: '+1' }],
    [{ direction: 'rtl' }],
    [{ color: [] }, { background: [] }],
    [{ align: [] }],
    ['link', 'image'],
    ['clean']
]

const quill = new Quill('#editor-container', {
    theme: 'snow',
    modules: {
        toolbar: {
            container: toolbarOptions,
            handlers: {
                image: imageHandler
            }
        }
    }
})

function imageHandler() {
    const input = document.createElement('input')
    input.setAttribute('type', 'file')
    input.setAttribute('accept', 'image/*')
    input.click()

    input.onchange = async () => {
        const file = input.files[0]
        if (!file) return

        const formData = new FormData()
        formData.append('image', file)

        try {
            const response = await fetch('/article/ajax/upload_image/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'x-requested-with': 'XMLHttpRequest'
                },
                body: formData
            })

            if (!response.ok) {
                alert('圖片上傳失敗')
                return
            }

            const result = await response.json()
            const range = quill.getSelection(true)
            quill.insertEmbed(range.index, 'image', result.url)
            quill.setSelection(range.index + 1)

        } catch (error) {
            alert('圖片上傳錯誤')
            console.error(error)
        }
    }
}

function getCSRFToken() {
    const cookies = document.cookie.split(';')
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=')
        if (name === 'csrftoken') return decodeURIComponent(value)
    }
    return ''
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('saveBtn').addEventListener('click', function () {
        document.querySelector('#hidden-content').value = quill.root.innerHTML
        const form = document.getElementById('article')
        form.insertAdjacentHTML('beforeend', '<input type="hidden" name="action" value="draft">')
        form.submit()
    })

    document.getElementById('publishBtn').addEventListener('click', function () {
        document.querySelector('#hidden-content').value = quill.root.innerHTML
        const form = document.getElementById('article')
        form.insertAdjacentHTML('beforeend', '<input type="hidden" name="action" value="article">')
        form.submit()
    })
})
