# Non-Technical Guide: How to Put Your Code on GitHub

Follow these steps one by one. You don't need to understand the complex terms!

## Phase 1: Create your "Digital Folder" (Repository)
1. Go to **[GitHub.com](https://github.com)** and sign up or log in.
2. Look for a **+** icon in the top-right corner and select **"New repository"**.
3. **Repository name**: Type `market_dashboard` (or any name you like).
4. **Public/Private**: Select **Public** (Streamlit Cloud needs it to be Public for the free tier).
5. **Initialize this repository**: Leave all these unchecked (start fresh).
6. Click the green **"Create repository"** button.
7. You will see a page with a list of commands. **Keep this page open!**

## Phase 2: Send Your Code (Using Terminal)
I have already prepared your code folder on your laptop. Now we just need to "push" it.

1. Open your **Terminal** app on your Mac.
2. Copy and paste the following commands **one by one** (press Enter after each):

   **Step A: Go to your project folder**
   ```bash
   cd /Users/pravin/.gemini/antigravity/scratch/market_sentiment_dashboard
   ```

   **Step B: Turn it into a Git folder**
   ```bash
   git init
   ```
   *(It might say "Initialized empty Git repository..." - that's good!)*

   **Step C: Rename the main branch**
   ```bash
   git branch -M main
   ```

   **Step D: Add your files**
   ```bash
   git add .
   ```

   **Step E: Save them (Commit)**
   ```bash
   git commit -m "My first upload"
   ```

   **Step F: Link to GitHub**
   *(Go back to the browser page you kept open. Look for the command starting with `git remote add origin`. It looks like this below, but use YOUR specific URL)*:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/market_dashboard.git
   ```
   *(Paste that command into your terminal)*

   **Step G: Push the code!**
   ```bash
   git push -u origin main
   ```

   > **Note:** If it asks for a username/password, you might need to sign in via the browser pop-up.

## Phase 3: Launch the App
1. Go to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Click **"New App"**.
3. Select "Use existing repo".
4. You should see `market_dashboard` in the list. Select it.
5. Click **"Deploy!"**.
6. Done! 🎉 Your app is now online.
