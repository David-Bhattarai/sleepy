document.addEventListener('DOMContentLoaded', () => {
    const paymentMethods = document.getElementById('payment-methods');
    const proceedBtn = document.getElementById('proceed-btn');
    const errorMessage = document.getElementById('error-message');
    const paymentModal = document.getElementById('payment-modal');
    const modalContent = document.getElementById('modal-content');
    const modalMessage = document.getElementById('modal-message');
    const token = localStorage.getItem('token');

    let selectedMethod = null;

    // Handle payment method selection
    paymentMethods.addEventListener('click', (e) => {
        const methodDiv = e.target.closest('.payment-method');
        if (!methodDiv) return;

        // Clear previous selection
        document.querySelectorAll('.payment-method').forEach(div => {
            div.classList.remove('selected');
        });

        // Set new selection
        methodDiv.classList.add('selected');
        selectedMethod = methodDiv.dataset.method;
        proceedBtn.disabled = false;
        proceedBtn.textContent = `Pay with ${selectedMethod.charAt(0).toUpperCase() + selectedMethod.slice(1)}`;
    });

    // Handle payment processing
    proceedBtn.addEventListener('click', () => {
        if (!selectedMethod) {
            errorMessage.textContent = 'Please select a payment method.';
            return;
        }

        // Show the modal and simulate payment
        paymentModal.classList.remove('hidden');
        simulatePayment(selectedMethod);
    });

    function simulatePayment(method) {
        modalContent.innerHTML = `<img src="${getLogoUrl(method)}" alt="${method}" class="payment-logo mx-auto mb-4">`;
        modalMessage.textContent = 'Redirecting to secure payment gateway...';

        setTimeout(() => {
            modalMessage.textContent = 'Verifying payment details...';
        }, 2000);

        setTimeout(() => {
            modalMessage.textContent = 'Payment successful! Upgrading your account...';
            upgradeToPremium();
        }, 4000);
    }

    async function upgradeToPremium() {
        try {
            const response = await fetch('/api/subscribe', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('isPremium', 'true');
                modalMessage.textContent = 'Account upgraded successfully! Redirecting...';
                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 2000);
            } else {
                throw new Error(data.error || 'Upgrade failed. Please contact support.');
            }
        } catch (err) {
            modalMessage.style.color = '#f87171'; // Red color
            modalMessage.textContent = err.message;
        }
    }
    
    function getLogoUrl(method) {
        switch(method) {
            case 'esewa': return 'https://logowik.com/content/uploads/images/esewa-payment-gateway5481.jpg';
            case 'khalti': return 'https://logowik.com/content/uploads/images/khalti-digital-wallet5518.logowik.com.webp';
            case 'paypal': return 'https://www.paypalobjects.com/webstatic/mktg/logo-center/PP_Acceptance_Marks_for_LogoCenter_266x142.png';
            case 'payoneer': return 'https://logowik.com/content/uploads/images/payoneer-new-20212711.jpg';
            default: return '';
        }
    }
});
