# 🇮🇳 News Sentiment & Impact Engine (Nifty 50)

A real-time AI dashboard that fetches financial news, analyzes it using Google Gemini 1.5 Flash, and calculates market impact scores for Indian stocks.

## 🚀 Cloud Deployment (Streamlit Community Cloud)

You can deploy this dashboard for free in minutes!

### Step 1: Push to GitHub
1.  Create a new repository on GitHub.
2.  Push this code to the repository:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin <YOUR_REPO_URL>
    git push -u origin main
    ```

### Step 2: Deploy on Streamlit
1.  Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2.  Click **"New app"**.
3.  Select your repository (`market_sentiment_dashboard`), branch (`main`), and main file (`app.py`).
4.  Click **"Deploy!"**.

### Step 3: API Key Configuration
Once deployed, the app will ask for the Gemini API Key in the sidebar nicely. 
*Alternatively*, you can set it in Streamlit Secrets for auto-loading:
1.  On your deployed app dashboard, go to **Settings** -> **Secrets**.
2.  Add:
    ```toml
    GEMINI_API_KEY = "your-key-here"
    ```

## 🛠 Local Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Features
*   **RSS Integration**: MoneyControl, Economic Times, BBC.
*   **AI Analysis**: Gemini Flash analyzes sentiment and geopolitical risk.
*   **Defcon System**: Alerts on War/Sanctions news.
