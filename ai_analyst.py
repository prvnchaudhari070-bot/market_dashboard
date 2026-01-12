import google.generativeai as genai
import json
import logging

def configure_genai(api_key):
    """Configures the Gemini API with the provided key."""
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return False

def clean_json_string(json_str):
    """
    Cleans the JSON string returned by the model.
    Sometimes models return markdown code blocks e.g. ```json ... ```
    """
    json_str = json_str.strip()
    if json_str.startswith("```json"):
        json_str = json_str[7:]
    if json_str.startswith("```"):
        json_str = json_str[3:]
    if json_str.endswith("```"):
        json_str = json_str[:-3]
    return json_str.strip()

def analyze_news(headline, summary, api_key):
    """
    Analyzes a single news item using Gemini Flash.
    Returns a dict with structured impact data.
    """
    if not api_key:
        return {
            "related_stock_ticker": "N/A",
            "sector": "N/A",
            "impact_score": 0,
            "impact_type": "Data Missing",
            "sentiment": "Neutral",
            "trade_signal": "API Key Missing"
        }
        
    system_prompt = "You are a specialized Hedge Fund risk engine. Analyze the following news. Output ONLY valid JSON."
    
    user_prompt = f"""
    Headline: {headline}
    Summary: {summary}
    
    Required JSON Output Structure:
    {{
      "related_stock_ticker": "RELIANCE / HDFCBANK / NIFTY50 / NONE (or other specific Indian ticker)",
      "sector": "Banking / Oil&Gas / Geopolitics / Macro / IT / Auto / etc.",
      "impact_score": "Integer between -10 (Catastrophic) to +10 (Skyrocketing)",
      "impact_type": "Sanctions / War / Duty_Change / Earnings / General / Regulatory",
      "sentiment": "Bullish / Bearish / Neutral",
      "trade_signal": "Short explanation of how the stock will react in the next 1 hour."
    }}
    
    Rule: If the news mentions "Sanctions", "War", "Strike", or "Customs Duty", the score must be high magnitude (above 7 or below -7).
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([system_prompt, user_prompt])
        
        raw_text = response.text
        cleaned_json = clean_json_string(raw_text)
        
        parsed_result = json.loads(cleaned_json)
        
        # Ensure impact_score is int
        if 'impact_score' in parsed_result:
            try:
                parsed_result['impact_score'] = int(parsed_result['impact_score'])
            except ValueError:
                parsed_result['impact_score'] = 0
                
        return parsed_result

    except json.JSONDecodeError:
        print(f"Failed to parse JSON for headline: {headline}")
        return {
            "related_stock_ticker": "ERROR",
            "sector": "ERROR",
            "impact_score": 0,
            "impact_type": "Parse Error",
            "sentiment": "Neutral",
            "trade_signal": "Manual Review Needed"
        }
    except Exception as e:
        print(f"API Error for headline: {headline}. Error: {e}")
        return {
            "related_stock_ticker": "ERROR",
            "sector": "ERROR",
            "impact_score": 0,
            "impact_type": "API Error",
            "sentiment": "Neutral",
            "trade_signal": f"Error: {str(e)}"
        }
