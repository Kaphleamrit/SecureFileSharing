document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });

    // Show password toggle
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            // Toggle the type attribute using getAttribure() method
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);

            // Toggle the eye / eye slash icon
            this.classList.toggle('bi-eye');
        });
    }

    // File input label update
    const fileInput = document.querySelector('#file');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            const fileName = this.files[0].name;
            const nextSibling = this.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    }
});
