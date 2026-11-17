# 🚀 SupeRR Cricket Intelligence Platform — Deployment Guide

This guide details the exact steps to deploy the **SupeRR Cricket Intelligence Platform** to the web so Rajasthan Royals / Unstop evaluators can access your interactive dashboard via a live public URL.

---

## 🏆 Option 1: Streamlit Community Cloud (Recommended & 100% Free)
*This is the official, permanent, and most prestigious hosting platform for Streamlit apps. It provides a free `https://<your-app>.streamlit.app` domain with automated continuous deployment.*

### Step 1: Create a GitHub Repository
1. Log into your GitHub account: [github.com](https://github.com)
2. Go to [github.com/new](https://github.com/new)
3. Repository name: `superr-cricket-intelligence` (or `superr-selector-rr`)
4. Set visibility to **Public**
5. Do **not** check "Add a README file" (we already have a complete repo ready)
6. Click **Create repository**

### Step 2: Push Local Project to GitHub
In your project directory terminal (`C:\Users\harsh\Desktop\RR`), run:
```powershell
# Link to your new GitHub repository (replace with your repo URL)
git remote add origin https://github.com/harsh846pc-source/superr-cricket-intelligence.git

# Push main branch
git push -u origin main
```
*(If prompted, sign in with your GitHub credentials or Personal Access Token).*

### Step 3: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **"New app"** (or **"Create app"**).
3. Select your repository: `harsh846pc-source/superr-cricket-intelligence`
4. Set **Branch**: `main`
5. Set **Main file path**: `app.py`
6. (Optional) Under *Advanced settings*, confirm Python version is `3.11`.
7. Click **Deploy!** 🚀

Within ~2 minutes, your live web app will be accessible at:
`https://superr-cricket-intelligence.streamlit.app`

---

## ⚡ Option 2: Instant Public Tunnel (Live Right Now from Your Machine)
*If you need an immediate live public link to test on your phone or share with your team right this second without waiting for GitHub:*

1. Ensure your local app is running (Streamlit is currently running on `http://localhost:8501`).
2. Open a new PowerShell terminal and run:
   ```powershell
   npx --yes localtunnel --port 8501
   ```
3. It will output a public URL such as:
   `your url is: https://cuddly-cricket-42.loca.lt`
4. Click the link! (When prompted for password on first visit, enter your public IP address from [ipv4.icanhazip.com](https://ipv4.icanhazip.com)).

---

## 🤗 Option 3: Hugging Face Spaces (Free Cloud Hosting)
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Name your space (e.g., `superr-cricket-intelligence`)
3. Select **Space SDK**: **Streamlit**
4. Set Space hardware to the free tier (16GB RAM CPU)
5. Clone the space repository or add as a git remote:
   ```powershell
   git remote add hf https://huggingface.co/spaces/harsh846pc/superr-cricket-intelligence
   git push hf main
   ```
6. Your app will automatically build and launch at `https://huggingface.co/spaces/harsh846pc/superr-cricket-intelligence`.

---

## 🐳 Option 4: Docker Container Deployment (Render, Railway, Cloud Run)
A production `Dockerfile` has been pre-configured in the repository root:
```powershell
# Build Docker image
docker build -t superr-intelligence .

# Run Docker container
docker run -p 8501:8501 superr-intelligence
```
On **Render** or **Railway**, simply connect your GitHub repo; it will automatically detect the `Dockerfile` or `requirements.txt` and launch the service.

---

## 📦 What Was Optimized For Cloud Deployment
- **Ultra-Fast Parquet Caching:** 200,000+ enriched deliveries are compressed into `data/*.parquet` (~13 MB total), so the cloud server loads the data in under 1 second without needing 250MB+ raw CSV dumps.
- **Pre-Configured Dependencies:** Full `requirements.txt` with locked version compatibility for `streamlit`, `plotly`, `pyarrow`, `scikit-learn`, `python-docx`, `python-pptx`, and `reportlab`.
- **Custom RR Theme:** `.streamlit/config.toml` includes Rajasthan Royals brand colors (Royal Pink `#E4007C`, Deep Navy `#0A1428`, Card `#12203C`).
- **Clean Git Footprint:** Total repository footprint is under 70 MB, ensuring instant clone and zero build errors on Streamlit Cloud.
