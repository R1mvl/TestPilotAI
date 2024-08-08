export function notification(color, title, message) {
    console.log('notification');

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.backgroundColor = color;

    const titleElement = document.createElement('h3');
    titleElement.innerHTML = title;
    notification.appendChild(titleElement);

    const messageElement = document.createElement('pre');
    messageElement.innerHTML = message;
    notification.appendChild(messageElement);

    const closeButton = document.createElement('button');
    closeButton.innerHTML = 'X';
    closeButton.className = 'closeButton';
    closeButton.addEventListener('click', () => {
        notification.remove();
    });
    notification.appendChild(closeButton);

    document.body.appendChild(notification);
}

// si tu click sur l'element qui a la class logo tu est redirigé vers la page d'accueil
document.querySelector('.logo').addEventListener('click', () => {
    window.location.href = '/home';
});