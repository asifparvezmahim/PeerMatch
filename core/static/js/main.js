document.addEventListener('DOMContentLoaded', () => {
    // Reveal animations on scroll
    const reveal = () => {
        const elements = document.querySelectorAll('.animate');
        elements.forEach(el => {
            const windowHeight = window.innerHeight;
            const elementTop = el.getBoundingClientRect().top;
            const elementVisible = 150;
            if (elementTop < windowHeight - elementVisible) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    };

    window.addEventListener('scroll', reveal);
    reveal(); // Initial check

    // Add visual feedback to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', () => {
            btn.style.transform = 'scale(0.95)';
        });
        btn.addEventListener('mouseup', () => {
            btn.style.transform = 'scale(1)';
        });
    });
});
