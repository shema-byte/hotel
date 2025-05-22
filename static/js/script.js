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
    const checkIn = document.getElementById("check_in");
    const checkOut = document.getElementById("check_out");

    checkIn.addEventListener("change", function () {
        checkOut.min = this.value;
    });

    checkOut.addEventListener("change", function () {
        if (checkIn.value && checkOut.value && checkOut.value <= checkIn.value) {
            alert("Check-out date must be after the check-in date.");
            checkOut.value = "";
        }
    });

    // Set today's date as minimum for check-in
    window.onload = () => {
        const today = new Date().toISOString().split('T')[0];
        checkIn.setAttribute("min", today);
    };

    
});