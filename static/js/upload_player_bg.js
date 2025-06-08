document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('bgInput')
    const profilePhoto = document.getElementById('backgroundPhoto')

    fileInput.addEventListener('change', function () {
        const file = this.files[0]
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader()
            reader.onload = function (e) {
                profilePhoto.src = e.target.result
            }
            reader.readAsDataURL(file)
        }
    })
})
