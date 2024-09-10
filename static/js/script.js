document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('attendanceForm');

    // Dynamic font size adjustment for mobile
    function adjustFontSize() {
        if (window.innerWidth < 600) {
            document.querySelector('h1').style.fontSize = '20px';
            document.querySelector('.form-container').style.padding = '15px';
        } else {
            document.querySelector('h1').style.fontSize = '24px';
            document.querySelector('.form-container').style.padding = '30px';
        }
    }

    // Run on page load and window resize
    adjustFontSize();
    window.addEventListener('resize', adjustFontSize);

    // Basic form validation
    form.addEventListener('submit', function(event) {
        const registerNo = document.getElementById('register_no').value.trim();
        const name = document.getElementById('name').value.trim();
        const dept = document.getElementById('dept').value.trim();

        if (registerNo === "" || name === "" || dept === "") {
            alert("All fields must be filled out.");
            event.preventDefault(); // Prevent form submission
        }
    });
});
