document.addEventListener('DOMContentLoaded', () => {
    // --- Sign Up ---
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorEl = document.getElementById('signup-error');

            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password })
                });
                const data = await response.json();
                if (response.ok) {
                    window.location.href = '/signin.html?signed_up=true';
                } else {
                    errorEl.textContent = data.error || 'An error occurred.';
                    errorEl.classList.remove('hidden');
                }
            } catch (err) {
                errorEl.textContent = 'Could not connect to the server.';
                errorEl.classList.remove('hidden');
            }
        });
    }

    // --- Sign In ---
    const signinForm = document.getElementById('signin-form');
    if (signinForm) {
        // Show success message on redirect from signup
        const params = new URLSearchParams(window.location.search);
        if (params.get('signed_up') === 'true') {
            const successEl = document.getElementById('signin-success');
            if(successEl) {
                successEl.textContent = 'Signup successful! Please sign in.';
                successEl.classList.remove('hidden');
            }
        }

        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorEl = document.getElementById('signin-error');

            try {
                const response = await fetch('/api/signin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('isAdmin', data.isAdmin);
                    window.location.href = '/dashboard.html';
                } else {
                    errorEl.textContent = data.error || 'An error occurred.';
                    errorEl.classList.remove('hidden');
                }
            } catch (err) {
                errorEl.textContent = 'Could not connect to the server.';
                errorEl.classList.remove('hidden');
            }
        });
    }
});
