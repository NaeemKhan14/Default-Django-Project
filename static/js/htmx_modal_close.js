function closeModal(modal_name) {
    var container = document.getElementById(modal_name)
    var backdrop = document.getElementById(modal_name + "-backdrop")
    var modal = document.getElementById(modal_name + "_modal")

    modal.classList.remove("show")
    backdrop.classList.remove("show")

    setTimeout(function () {
        container.removeChild(backdrop)
        container.removeChild(modal)
    }, 200)
}