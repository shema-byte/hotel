document.addEventListener('DOMContentLoaded', function () {
    const bookNowButtons = document.querySelectorAll('.book-now');
    const bookingModal = new bootstrap.Modal(document.getElementById('bookingModal'));
    const roomIdInput = document.getElementById('roomId');
    const confirmationMessage = document.getElementById('confirmationMessage');

    bookNowButtons.forEach(button => {
        button.addEventListener('click', function () {
            const roomType = this.getAttribute('data-room-type');
            roomIdInput.value = roomType;
            bookingModal.show();
        });
    });

    document.getElementById('bookingForm').addEventListener('submit', function () {
        confirmationMessage.classList.remove('d-none');
        setTimeout(() => {
            confirmationMessage.classList.add('d-none');
            bookingModal.hide();
        }, 2000);
    });
    
});