# 🚀 MindBridge - Deployment & Income Generation Guide

## STEP 1: GitHub ma Upload Garne

```bash
git add .
git commit -m "Add deployment files"
git push origin main
```

---

## STEP 2: Render.com ma Deploy Garne (FREE)

1. **https://render.com** ma janus
2. "New Web Service" click garne
3. GitHub repo connect garne
4. Yo settings use garne:
   - **Build Command:** `pip install -r server/requirements.txt`
   - **Start Command:** `cd server && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Environment:** Python 3
5. Environment Variables add garne:
   - `GEMINI_API_KEY` = tapai ko Gemini API key
6. "Deploy" click garne

**Tapai ko app live URL milcha:** `https://mindbridge-app.onrender.com`

---

## STEP 3: Google AdSense Setup (INCOME)

### AdSense Apply Garne:
1. **https://adsense.google.com** ma janus
2. Google account le sign in garne
3. "Get Started" click garne
4. Tapai ko website URL add garne (Render URL)
5. 1-3 din wait garne approval ko lagi

### Approval Pachhi - HTML Files ma Add Garne:

**`client/index.html` ko `<head>` section ma:**
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

**`client/dashboard.html` ko `</body>` agadi:**
```html
<!-- Bottom Banner Ad -->
<div style="position:fixed; bottom:0; left:0; right:0; z-index:9999; background:#1a1a2e; padding:4px 0; text-align:center;">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
         data-ad-slot="XXXXXXXXXX"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>
```

> **Note:** `ca-pub-XXXXXXXXXXXXXXXX` lai tapai ko actual Publisher ID le replace garne

---

## STEP 4: Income Badhauney Ko Lagi Premium Features

### Option A: Freemium Model (Recommended)

**Free Users:**
- 10 AI chat messages/day
- Basic mood tracking
- Ads dekhauney

**Premium Users ($5-10/month):**
- Unlimited AI chat
- Video consultation
- No ads
- Advanced emotion detection

### Option B: Professional Consultation Fees
- Doctors/therapists list garne
- Per-session fee: $10-20
- App 20% commission linccha

---

## STEP 5: Payment Integration (Stripe)

```python
# server/app.py ma add garne
import stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/api/create-subscription', methods=['POST'])
def create_subscription():
    # Premium subscription create garne
    pass
```

**Environment Variables:**
- `STRIPE_SECRET_KEY` = sk_live_...
- `STRIPE_PUBLISHABLE_KEY` = pk_live_...

---

## Expected Income Estimate

| Source | Monthly Estimate |
|--------|-----------------|
| Google AdSense (1000 users) | $50-200 |
| Premium Subscriptions (50 users × $5) | $250 |
| Professional Consultations | $100-500 |
| **Total** | **$400-950/month** |

---

## Quick Deploy Commands

```bash
# 1. Requirements update garne
pip freeze > server/requirements.txt

# 2. Git push garne
git add .
git commit -m "Deploy MindBridge"
git push origin main

# 3. Render ma auto-deploy hunchha
```

---

## Alternative Free Hosting Options

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Render.com** | 750 hrs/month | Backend + Frontend |
| **Railway.app** | $5 credit/month | Easy deploy |
| **Fly.io** | 3 shared VMs | Production |
| **Vercel** | Unlimited | Frontend only |

**Recommendation: Render.com** - sabai bhanda easy ra free!
