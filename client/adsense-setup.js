/**
 * MINDBRIDGE - Google AdSense Setup
 * 
 * SETUP INSTRUCTIONS:
 * 1. https://adsense.google.com ma janus
 * 2. Tapai ko website add garne
 * 3. Approval pachhi ADSENSE_PUBLISHER_ID replace garne
 * 4. Ad units create garne ra AD_SLOT_ID replace garne
 */

const ADSENSE_CONFIG = {
    // Replace with your actual Publisher ID from AdSense dashboard
    // Format: ca-pub-XXXXXXXXXXXXXXXX
    publisherId: 'ca-pub-XXXXXXXXXXXXXXXX',
    
    // Replace with your actual Ad Slot IDs
    adSlots: {
        banner: 'XXXXXXXXXX',      // Bottom banner ad
        sidebar: 'XXXXXXXXXX',     // Sidebar ad
        inContent: 'XXXXXXXXXX'    // In-content ad
    },
    
    // Set to true after AdSense approval
    enabled: false
};

/**
 * AdSense script load garne
 */
function loadAdSense() {
    if (!ADSENSE_CONFIG.enabled) {
        console.log('AdSense disabled - enable after approval');
        return;
    }
    
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CONFIG.publisherId}`;
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);
}

/**
 * Bottom banner ad inject garne
 */
function injectBannerAd() {
    if (!ADSENSE_CONFIG.enabled) return;
    
    const adContainer = document.createElement('div');
    adContainer.style.cssText = `
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: rgba(15, 15, 30, 0.95);
        padding: 6px 0;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    `;
    
    adContainer.innerHTML = `
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="${ADSENSE_CONFIG.publisherId}"
             data-ad-slot="${ADSENSE_CONFIG.adSlots.banner}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});<\/script>
    `;
    
    document.body.appendChild(adContainer);
    
    // Body ko bottom padding add garne taaki content hide na hos
    document.body.style.paddingBottom = '90px';
}

/**
 * Premium users ko lagi ads hide garne
 */
function hideAdsForPremiumUsers() {
    const user = JSON.parse(localStorage.getItem('mindbridge_user') || '{}');
    if (user.isPremium) {
        document.querySelectorAll('.adsbygoogle').forEach(ad => {
            ad.style.display = 'none';
        });
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadAdSense();
    injectBannerAd();
    hideAdsForPremiumUsers();
});
