import streamlit as st
import pandas as pd
import time
import news_engine
import ai_analyst
from streamlit_autorefresh import st_autorefresh

# Page Config
st.set_page_config(
    page_title="Nifty 50 News Sentiment Engine",
    page_icon="📈",
    layout="wide"
)

# Auto-refresh every 60 seconds
count = st_autorefresh(interval=60 * 1000, key="newsrefresh")

# Title and Header
st.title("🇮🇳 News Sentiment & Impact Engine (Nifty 50)")
st.markdown("Live AI-powered analysis of financial news impact on Indian Markets.")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get it from Google AI Studio")
    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key to enable analysis.")
    
    st.divider()
    st.markdown("### Status")
    st.write(f"Last Refresh: {time.strftime('%H:%M:%S')}")
    
    if st.button("Manual Refresh"):
        st.rerun()

# --- Main Logic ---

# Initialize Session State for Data
if 'news_data' not in st.session_state:
    st.session_state.news_data = pd.DataFrame()

def apply_styling(df):
    """
    Applies styling to the dataframe.
    """
    def color_impact(val):
        if isinstance(val, int):
            if val > 5:
                return 'background-color: #28a745; color: white'  # Green
            elif val < -5:
                return 'background-color: #dc3545; color: white'  # Red
            elif val > 0:
                return 'color: #28a745'
            elif val < 0:
                return 'color: #dc3545'
        return ''

    def highlight_defcon(val):
        if val in ["Sanctions", "War"]:
            return 'background-color: darkred; color: white; font-weight: bold'
        return ''

    # Reorder columns if they exist
    cols = ['impact_score', 'related_stock_ticker', 'sentiment', 'headline', 'impact_type', 'trade_signal']
    available_cols = [c for c in cols if c in df.columns]
    df = df[available_cols]

    return df.style.map(color_impact, subset=['impact_score'])\
                   .map(highlight_defcon, subset=['impact_type'])

# Fetch and Analyze Data
if api_key:
    with st.spinner('Fetching and Analyzing Latest News...'):
        # 1. Fetch News
        raw_news = news_engine.fetch_latest_news()
        
        # 2. Analyze with AI (Limit to top 5 for demo/speed purposes if this was a loop, effectively doing all)
        # Note: In a real high-freq app, we'd cache results to avoid re-analyzing same headlines.
        # For this prototype, we'll analyze a subset or check against simple cache if we implemented it.
        # We will just analyze the top 5 freshest items to save tokens/time for this demo.
        
        analyzed_results = []
        
        ai_analyst.configure_genai(api_key)
        
        progress_bar = st.progress(0)
        
        for idx, item in enumerate(raw_news[:5]): # analyzing top 5 for responsiveness
            analysis = ai_analyst.analyze_news(item['title'], item['summary'], api_key)
            result = {
                "headline": item['title'],
                **analysis,
                "source": item['source'],
                "published": item['published']
            }
            analyzed_results.append(result)
            progress_bar.progress((idx + 1) / 5)

        progress_bar.empty()
            
        # Create Dataframe
        if analyzed_results:
            df = pd.DataFrame(analyzed_results)
            
            # Sort by absolute impact score desc
            if 'impact_score' in df.columns:
                df['abs_impact'] = df['impact_score'].abs()
                df = df.sort_values(by='abs_impact', ascending=False).drop(columns=['abs_impact'])
            
            st.session_state.news_data = df
else:
    if st.session_state.news_data.empty:
         st.info("Waiting for API Key to fetch data...")

# --- Dashboard Display ---

if not st.session_state.news_data.empty:
    df = st.session_state.news_data

    # Geopolitical Defcon
    if 'impact_type' in df.columns:
        critical_threats = df[df['impact_type'].isin(["Sanctions", "War", "Strike", "Customs Duty"])]
        if not critical_threats.empty:
            st.error("🚨 **GEOPOLITICAL DEFCON ALERT**: CRITICAL MARKET THREAT DETECTED 🚨")
            for i, row in critical_threats.iterrows():
                st.write(f"**{row['headline']}** - {row['trade_signal']}")
        else:
            st.success("✅ Geopolitical Status: Stable")

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    avg_sentiment = df['impact_score'].mean() if 'impact_score' in df.columns else 0
    c1.metric("Market Sentiment Index", f"{avg_sentiment:.1f}", delta_color="normal")
    c2.metric("News Analyzed", len(df))
    top_sector = df['sector'].mode()[0] if 'sector' in df.columns and not df.empty else "N/A"
    c3.metric("Top Active Sector", top_sector)

    # Main Data Table
    st.subheader("Latest Market Impact Analysis")
    st.dataframe(
        apply_styling(df),
        use_container_width=True,
        height=600,
        column_config={
            "impact_score": st.column_config.NumberColumn(
                "Impact Score",
                help="Score from -10 to +10",
                format="%d ⭐",
            ),
             "headline": st.column_config.TextColumn(
                "Headline",
                width="large"
            ),
        }
    )

elif api_key:
    st.warning("No news found or analysis failed.")
