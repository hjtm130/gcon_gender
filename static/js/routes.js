// ここに JavaScript のコードを記述します
console.log('routes.js が読み込まれました');

// static/js/routes.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('/header')
        .then(response => response.text())
        .then(data => {
            document.body.insertAdjacentHTML('afterbegin', data);
        })
        .catch(error => console.error('Error loading header:', error));
});
