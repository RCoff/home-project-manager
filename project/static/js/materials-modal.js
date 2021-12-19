let materialsModal = document.getElementById('materials-view-modal')
materialsModal.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget

    let name = button.getAttribute('data-bs-name')
    let modalTitle = materialsModal.querySelector('.modal-title')
    let modalName = materialsModal.querySelector('#modal-material-name')

    let description = button.getAttribute('data-bs-description')
    let modalDescription = materialsModal.querySelector('#modal-material-description')

    let cost = button.getAttribute('data-bs-cost')
    let modalCost = materialsModal.querySelector('#modal-material-cost')

    let quantity = button.getAttribute('data-bs-quantity')
    let modalQuantity = materialsModal.querySelector('#modal-material-quantity')

    let totalCost = button.getAttribute('data-bs-total-cost')
    let modalTotalCost = materialsModal.querySelector('#modal-material-total-cost')

    modalTitle.textContent = name
    modalName.textContent = name
    modalDescription.textContent = description
    modalCost.textContent = cost
    modalQuantity.textContent = quantity
    modalTotalCost.textContent = totalCost
})