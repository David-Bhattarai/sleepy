
document.addEventListener('DOMContentLoaded', () => {
    // --- Global Elements & State ---
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const token = localStorage.getItem('token');
    const isAdmin = localStorage.getItem('isAdmin') === 'true';
    const isPremium = localStorage.getItem('isPremium') === 'true'; // Check for premium status

    // --- Navigation Handling ---
    const updateNav = () => {
        const navLinksContainer = document.getElementById('nav-links');
        let links = '';
        const linkClass = "text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors";
        const activeLinkClass = "bg-indigo-600 text-white px-3 py-2 rounded-md text-sm font-medium";
        const currentPage = window.location.pathname;

        if (token) {
            let premiumLink = '';
            if (isPremium) {
                premiumLink = `<span class=\"text-yellow-300 font-bold px-3 py-2 text-sm\"><i class=\"fas fa-star\"></i> Premium</span>`;
            } else {
                premiumLink = `<a href=\"/premium.html\" class=\"text-yellow-300 hover:text-yellow-400 font-bold px-3 py-2 rounded-md text-sm\"><i class=\"fas fa-star\"></i> Go Premium</a>`;
            }

            links = `
                <a href=\"/dashboard.html\" class=\"${currentPage.includes('dashboard') ? activeLinkClass : linkClass}\">Dashboard</a>
                <a href=\"/mood-tracker.html\" class=\"${currentPage.includes('mood-tracker') ? activeLinkClass : linkClass}\">Mood Tracker</a>
                <a href=\"/relaxation.html\" class=\"${currentPage.includes('relaxation') ? activeLinkClass : linkClass}\">Relaxation</a>
                <a href=\"/emotional-intelligence.html\" class=\"${currentPage.includes('emotional-intelligence') ? activeLinkClass : linkClass}\">EI Profile</a>
                <a href=\"/games.html\" class=\"${currentPage.includes('games') ? activeLinkClass : linkClass}\">Games</a>
                ${premiumLink}
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
        localStorage.removeItem('isPremium'); // Clear premium status on logout
        window.location.href = '/signin.html';
    };

    if (menuBtn) {
        menuBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
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
