
document.addEventListener('DOMContentLoaded', () => {
    // --- Global Elements & State ---
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const token = localStorage.getItem('token');
    const isAdmin = localStorage.getItem('isAdmin') === 'true';


    // --- Navigation Handling ---
    const updateNav = () => {
        const navLinksContainer = document.getElementById('nav-links');
        let links = '';
        const linkClass = "text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors";
        const activeLinkClass = "bg-indigo-600 text-white px-3 py-2 rounded-md text-sm font-medium";
        const currentPage = window.location.pathname;

        if (token) {
            links = `
                <a href=\"/dashboard.html\" class=\"${currentPage.includes('dashboard') ? activeLinkClass : linkClass}\">Dashboard</a>
                <a href=\"/mood-tracker.html\" class=\"${currentPage.includes('mood-tracker') ? activeLinkClass : linkClass}\">Mood Tracker</a>
                <a href=\"/emotion-detection.html\" class=\"${currentPage.includes('emotion-detection') ? activeLinkClass : linkClass}\">🎭 Emotion Detection</a>
                <a href=\"/relaxation.html\" class=\"${currentPage.includes('relaxation') ? activeLinkClass : linkClass}\">Relaxation</a>
                <a href=\"/games.html\" class=\"${currentPage.includes('games') ? activeLinkClass : linkClass}\">Games</a>
                <a href=\"/video-chat.html\" class=\"${currentPage.includes('video-chat') ? activeLinkClass : linkClass}\">Video Chat</a>
                <a href=\"/professional-consultation.html\" class=\"${currentPage.includes('professional-consultation') ? activeLinkClass : linkClass}\">👨‍⚕️ Find Therapist</a>
                ${isAdmin ? '<a href=\"/admin.html\" class=\"text-red-400 font-bold hover:text-red-500 px-3 py-2 rounded-md text-sm font-medium\">Admin</a>' : ''}
                <a href=\"#\" id=\"logout-btn\" class=\"${linkClass}\">Logout</a>
            `;
        } else {
            links = `
                <a href=\"/signin.html\" class=\"${linkClass}\">Sign In</a>
                <a href=\"/signup.html\" class=\"bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700\">Sign Up</a>
            `;
        }
        if (navLinksContainer) navLinksContainer.innerHTML = links;
        if (mobileMenu) mobileMenu.innerHTML = `<div class=\"px-2 pt-2 pb-3 space-y-1 sm:px-3\">${links}</div>`;
        
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', handleLogout);
        }
    };

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('isAdmin');

        window.location.href = '/signin.html';
    };

    if (menuBtn) {
        menuBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    }

    // Handle video chat button click
    const videoChatBtn = document.getElementById('video-chat-btn');
    if (videoChatBtn) {
        videoChatBtn.addEventListener('click', () => {
            const token = localStorage.getItem('token');
            if (token) {
                window.location.href = '/video-chat.html';
            } else {
                window.location.href = '/signin.html';
            }
        });
    }

    // --- Page-Specific Logic (existing code remains the same) ---
    // ... (dashboard logic, etc.)

    // --- Global Initialization ---
    updateNav();
});

// Add font-awesome for the star icon
const fontAwesomeLink = document.createElement('link');
fontAwesomeLink.rel = 'stylesheet';
fontAwesomeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css';
document.head.appendChild(fontAwesomeLink);
