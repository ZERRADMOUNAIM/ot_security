/**
 * OTMindset — Frontend JavaScript
 * Handles API calls, card animations, and UI interactions.
 */

// CSRF token helper
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

// Animate cards on scroll
function initCardAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.analysis-card').forEach(card => {
        observer.observe(card);
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initCardAnimations();
});
