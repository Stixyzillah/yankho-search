// Example script for client-side validation or other interactivity

document.addEventListener('DOMContentLoaded', function() {
    // Example of handling form validation for the Contact Form
    const contactForm = document.querySelector('.form-add-contact form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const name = document.querySelector('#name').value;
            const business = document.querySelector('#business').value;
            if (!name || !business) {
                event.preventDefault();
                alert('Please fill out the required fields.');
            }
        });
    }
});
