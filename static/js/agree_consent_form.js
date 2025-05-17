document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('agreeCheckbox')
    const submitBtn = document.getElementById('submitBtn')
    const signInput = document.getElementById('sign')

    let isComposing = false

    function getLength(str) {
        let length = 0
        for (let char of str) {
            length += char.match(/[^\x00-\xff]/) ? 2 : 1
        }
        return length
    }

    function truncateToMaxLength(str, maxLen) {
        let length = 0
        let result = ''
        for (let char of str) {
            let charLen = char.match(/[^\x00-\xff]/) ? 2 : 1
            if (length + charLen > maxLen) {
                break
            }
            result += char
            length += charLen
        }
        return result
    }

    function updateSubmitState() {
        const isChecked = checkbox.checked
        const length = getLength(signInput.value.trim())
        const hasValidName = length > 0 && length <= 16

        submitBtn.disabled = !(isChecked && hasValidName)
        submitBtn.style.opacity = submitBtn.disabled ? '0.7' : '1'
        submitBtn.style.cursor = submitBtn.disabled ? 'default' : 'pointer'
    }

    signInput.addEventListener('compositionstart', () => {
        isComposing = true
    })

    signInput.addEventListener('compositionend', () => {
        isComposing = false
        const truncated = truncateToMaxLength(signInput.value, 16)
        if (signInput.value !== truncated) {
            signInput.value = truncated
        }
        updateSubmitState()
    })

    signInput.addEventListener('beforeinput', function (e) {
        if (isComposing) {
            return
        }
        if (!e.data) {
            return
        }

        const currentVal = signInput.value
        const selectionStart = signInput.selectionStart
        const selectionEnd = signInput.selectionEnd

        const newVal = currentVal.slice(0, selectionStart) + e.data + currentVal.slice(selectionEnd)
        const length = getLength(newVal)

        if (length > 16) {
            e.preventDefault()
            console.log("over")
        }
    })

    signInput.addEventListener('input', function () {
        if (isComposing) {
            return
        }

        const truncated = truncateToMaxLength(signInput.value, 16)
        if (signInput.value !== truncated) {
            signInput.value = truncated
        }
        updateSubmitState()
    })

    checkbox.addEventListener('change', updateSubmitState)
    updateSubmitState()
})
