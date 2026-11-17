# 🚀 SupeRR Cricket Intelligence Platform — Render Deployment Guide

This guide details the exact steps to deploy the **SupeRR Cricket Intelligence Platform** on **Render** ([render.com](https://render.com)) to get a permanent live public URL (`https://<your-app>.onrender.com`) for your Rajasthan Royals SupeRR Selector Season 2 submission.

---

## ⚡ Why Render & How It Works
* **Automatic Port Binding**: Render dynamically assigns an incoming web port via `$PORT`. We have pre-configured Streamlit to bind dynamically to `--server.port $PORT --server.address 0.0.0.0`.
* **Zero-Config Blueprint (`render.yaml`)**: We have added a root `render.yaml` specification so Render automatically reads the build commands, start commands, and environment variables with 1 click.
* **Low Memory Footprint**: We downcast categorical features so the full 200,000+ delivery dataset runs in just **~152 MB RAM**, comfortably below Render's 512 MB free tier limit.

---

## 📋 Step-by-Step Instructions to Deploy on Render

### Step 1: Create a GitHub Repository & Push
Render deploys directly from your GitHub repository.

1. Go to [github.com/new](https://github.com/new).
2. Create a repository named `superr-cricket-intelligence` (set to **Public**).
3. Do **not** check "Add a README file" (we already have all files initialized).
4. In your terminal at `C:\Users\harsh\Desktop\RR`, push your code:
   ```powershell
   # 1. Link to your GitHub repository (replace with your GitHub username if different)
   git remote add origin https://github.com/harsh846pc-source/superr-cricket-intelligence.git

   # 2. Push to main branch
   git push -u origin main
   ```

---

### Step 2: Deploy on Render

Log into [dashboard.render.com](https://dashboard.render.com). You have two easy deployment options:

#### 🌟 Option A: 1-Click Blueprint (Easiest & Recommended)
1. Click the **"New +"** button in the top navigation bar.
2. Select **"Blueprint"**.
3. Connect your GitHub account and select your `superr-cricket-intelligence` repository.
4. Render will automatically detect `render.yaml` and parse:
   * **Service Name**: `superr-cricket-intelligence`
   * **Runtime**: `Python`
   * **Plan**: `Free`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
5. Click **"Apply"**.
6. Render will automatically build the environment, install packages, and deploy your live app!

---

#### 🛠️ Option B: Manual Web Service Setup
If you prefer setting up the Web Service manually:
1. On the Render Dashboard, click **"New +"** → **"Web Service"**.
2. Select **"Build and deploy from a Git repository"** and connect `superr-cricket-intelligence`.
3. Fill in the service details:
   * **Name**: `superr-cricket-intelligence`
   * **Language**: `Python 3`
   * **Branch**: `main`
   * **Region**: `Oregon (US West)` or `Singapore (Southeast Asia)`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
   * **Instance Type**: `Free`
4. Expand **Advanced** and add the following Environment Variables:
   | Key | Value |
   | :--- | :--- |
   | `PYTHON_VERSION` | `3.11.9` |
   | `STREAMLIT_SERVER_HEADLESS` | `true` |
   | `STREAMLIT_SERVER_ENABLE_CORS` | `false` |
   | `STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION` | `false` |
5. Click **"Create Web Service"**.

---

### Step 3: Access Your Live Web App
Render will build the project in ~2–3 minutes. Once the logs display:
```
==> Uploaded build to cache
==> Running 'streamlit run app.py --server.port $PORT ...'
==> You can now view your Streamlit app in your browser!
==> Your service is live 🎉
```
Your app will be live at:
`https://superr-cricket-intelligence.onrender.com`

You can include this live link directly in your:
- Unstop submission form
- `SuperRR_Final_Methodology_Report.pdf`
- Social media reel/post `#SuperSelector`

---

## 💡 Render Free Tier Notes
* **Sleep Mode**: On Render's free tier, if no one visits the app for 15 minutes, the service spins down to conserve energy. When someone clicks your link, it takes ~30–45 seconds to wake up.
* **Keep-Alive (Optional)**: If you want zero spin-down latency during evaluation, you can add your Render URL to a free ping monitor like [cron-job.org](https://cron-job.org) or [UptimeRobot](https://uptimerobot.com) to ping it every 10 minutes.
