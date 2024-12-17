const buttons = document.getElementById('dis-message');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        const message = button.nextElementSibling; // Select the .not_message element
        if (message.style.display === 'block') {
            message.style.display = 'none';
        } else {
            message.style.display = 'block';

        }
    });
});
