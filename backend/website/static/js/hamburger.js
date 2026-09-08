const hamburger = document.getElementById('hamburger');
const navMenu = document.querySelector('.menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
});