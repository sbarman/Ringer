document.addEventListener('DOMContentLoaded', function() {
    button = document.getElementById('button1');
    button.addEventListener('click', event => {
        text = document.getElementById('text1')
        text.textContent = "Button clicked"
    })
}, false);
