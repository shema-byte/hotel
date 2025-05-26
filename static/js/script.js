// Make sure isAuthenticated is set above this script with Django context!

document.addEventListener('DOMContentLoaded', function () {
    const bookNowButtons = document.querySelectorAll('.book-now');
    const bookingModalElement = document.getElementById('bookingModal');
    const bookingModal = bookingModalElement ? new bootstrap.Modal(bookingModalElement) : null;
    const roomIdInput = document.getElementById('roomId');
    const confirmationMessage = document.getElementById('confirmationMessage');

    // Optional: Add alert box for guest users
    let loginAlert = document.getElementById('loginAlert');
    if (!loginAlert) {
        loginAlert = document.createElement('div');
        loginAlert.id = 'loginAlert';
        loginAlert.className = 'alert alert-warning alert-dismissible fade';
        loginAlert.role = 'alert';
        loginAlert.style.display = 'none';
        loginAlert.style.position = 'fixed';
        loginAlert.style.top = '80px';
        loginAlert.style.left = '50%';
        loginAlert.style.transform = 'translateX(-50%)';
        loginAlert.style.zIndex = '2000';
        loginAlert.innerHTML = `
            Please login to book.
            <button type="button" class="btn-close" onclick="this.parentElement.style.display='none';"></button>
        `;
        document.body.appendChild(loginAlert);
    }

    bookNowButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!isAuthenticated) {
                event.preventDefault();
                loginAlert.style.display = 'block';
                loginAlert.classList.add('show');
                setTimeout(() => {
                    loginAlert.classList.remove('show');
                    loginAlert.style.display = 'none';
                }, 2000);
                return false;
            }
            const roomType = this.getAttribute('data-room-type');
            if (roomIdInput) roomIdInput.value = roomType;
            if (bookingModal) bookingModal.show();
        });
    });

    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm && confirmationMessage && bookingModal) {
        bookingForm.addEventListener('submit', function () {
            confirmationMessage.classList.remove('d-none');
            setTimeout(() => {
                confirmationMessage.classList.add('d-none');
                bookingModal.hide();
            }, 2000);
        });
    }

    const checkIn = document.getElementById("check_in");
    const checkOut = document.getElementById("check_out");

    if (checkIn && checkOut) {
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
        const today = new Date().toISOString().split('T')[0];
        checkIn.setAttribute("min", today);
    }
});