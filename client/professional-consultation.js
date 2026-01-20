document.addEventListener('DOMContentLoaded', () => {
    const countryButtons = document.querySelectorAll('.country-btn');
    const therapistSections = document.querySelectorAll('.therapist-section');
    const searchInput = document.getElementById('search-therapists');
    const therapistCards = document.querySelectorAll('.therapist-card');

    // Search clinic function for real Nepal clinics
    window.searchClinic = function(clinicName) {
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(clinicName + ' contact information')}`;
        window.open(searchUrl, '_blank');
    };

    // Country filter functionality
    countryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            countryButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const country = button.getAttribute('data-country');
            
            // Show/hide sections based on country
            therapistSections.forEach(section => {
                if (country === 'all' || section.getAttribute('data-country') === country) {
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

            // Smooth scroll to first visible section
            if (country !== 'all') {
                const targetSection = document.querySelector(`[data-country="${country}"]`);
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

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            therapistCards.forEach(card => {
                const name = card.querySelector('h3').textContent.toLowerCase();
                const specialization = card.querySelector('.specialization').textContent.toLowerCase();
                const location = card.querySelector('.location').textContent.toLowerCase();
                const languages = card.querySelector('.languages').textContent.toLowerCase();
                
                if (name.includes(searchTerm) || 
                    specialization.includes(searchTerm) || 
                    location.includes(searchTerm) || 
                    languages.includes(searchTerm)) {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                } else {
                    card.style.display = 'none';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.8)';
                }
            });
        });
    }

    // Therapist card hover effects
    therapistCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
            card.style.boxShadow = '0 20px 40px rgba(79, 70, 229, 0.3)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.2)';
        });
    });

    // Contact button click tracking and animations (for non-Nepal therapists)
    const contactButtons = document.querySelectorAll('.contact-btn');
    contactButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Add click effect
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 150);

            // Track contact method
            const therapistName = button.closest('.therapist-card').querySelector('h3').textContent;
            console.log(`Contact info requested for ${therapistName}`);
        });
    });

    // Search contact button click tracking
    const searchContactButtons = document.querySelectorAll('.search-contact-btn');
    searchContactButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Add click effect
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 150);

            // Track search request
            const clinicName = button.closest('.therapist-card').querySelector('h3').textContent;
            console.log(`Search requested for ${clinicName}`);
        });
    });

    // Initialize with all therapists showing
    therapistSections.forEach(section => {
        section.style.display = 'block';
        section.style.opacity = '1';
        section.style.transform = 'translateY(0)';
    });
});