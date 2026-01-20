document.addEventListener('DOMContentLoaded', () => {
    const moodButtons = document.querySelectorAll('.mood-btn');
    const musicSections = document.querySelectorAll('.music-section');
    const musicCards = document.querySelectorAll('.music-card');

    // Mood filter functionality
    moodButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            moodButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const category = button.getAttribute('data-category');
            
            // Show/hide sections based on category
            musicSections.forEach(section => {
                if (category === 'all' || section.getAttribute('data-category') === category) {
                    section.style.display = 'block';
                    // Animate in
                    section.style.opacity = '0';
                    section.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        section.style.transition = 'all 0.5s ease';
                        section.style.opacity = '1';
                        section.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    section.style.display = 'none';
                }
            });
        });
    });

    // Music card hover effects and animations
    musicCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
            const playOverlay = card.querySelector('.play-overlay');
            if (playOverlay) {
                playOverlay.style.opacity = '1';
                playOverlay.style.transform = 'scale(1)';
            }
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            const playOverlay = card.querySelector('.play-overlay');
            if (playOverlay) {
                playOverlay.style.opacity = '0';
                playOverlay.style.transform = 'scale(0.8)';
            }
        });

        // Click animation
        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
            }, 150);
        });
    });

    // Music link click tracking
    const musicLinks = document.querySelectorAll('.music-link');
    musicLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Add click effect
            const card = link.closest('.music-card');
            card.style.boxShadow = '0 0 30px rgba(79, 70, 229, 0.5)';
            setTimeout(() => {
                card.style.boxShadow = '';
            }, 1000);

            // Optional: Track music plays (you can add analytics here)
            const songTitle = card.querySelector('h3').textContent;
            console.log(`Playing: ${songTitle}`);
        });
    });

    // Search functionality (optional enhancement)
    function addSearchFunctionality() {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search for songs...';
        searchInput.className = 'w-full max-w-md mx-auto px-4 py-2 rounded-lg bg-black bg-opacity-30 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:border-indigo-500';
        
        const headerCard = document.querySelector('.glass-card');
        const moodSelector = headerCard.querySelector('.flex.flex-wrap');
        headerCard.insertBefore(searchInput, moodSelector);

        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            musicCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const description = card.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                }
            });
        });
    }

    // Add search functionality
    addSearchFunctionality();

    // Smooth scroll to sections when mood is selected
    moodButtons.forEach(button => {
        button.addEventListener('click', () => {
            const category = button.getAttribute('data-category');
            if (category !== 'all') {
                const targetSection = document.querySelector(`[data-category="${category}"]`);
                if (targetSection) {
                    setTimeout(() => {
                        targetSection.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'start' 
                        });
                    }, 200);
                }
            }
        });
    });

    // Initialize with all music showing
    musicSections.forEach(section => {
        section.style.display = 'block';
        section.style.opacity = '1';
        section.style.transform = 'translateY(0)';
    });

    // Add loading animation for thumbnails
    const thumbnails = document.querySelectorAll('.music-thumbnail img');
    thumbnails.forEach(img => {
        img.addEventListener('load', () => {
            img.style.opacity = '1';
        });
        
        img.addEventListener('error', () => {
            // Fallback for broken images
            img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjE4MCIgdmlld0JveD0iMCAwIDMyMCAxODAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMjAiIGhlaWdodD0iMTgwIiBmaWxsPSIjMzc0MTUxIi8+CjxwYXRoIGQ9Ik0xNDQgNzJIMTc2VjEwOEgxNDRWNzJaIiBmaWxsPSIjNkI3Mjg0Ii8+CjxwYXRoIGQ9Ik0xNTIgODRIMTY4Vjk2SDE1MlY4NFoiIGZpbGw9IiM5Q0E0QUYiLz4KPC9zdmc+';
        });
    });
});