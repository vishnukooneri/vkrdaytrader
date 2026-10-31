import streamlit as st
import subprocess
import os
import sys
import json

# 1. Page Configuration
st.set_page_config(page_title="VKR Day Trader OS", page_icon="📈", layout="wide")

# 2. Premium TradingView-Style Custom CSS
st.markdown("""
    <style>
        .main .block-container { background-color: #131722; padding-top: 2rem; }
        section[data-testid="stSidebar"] { background-color: #1e222d !important; border-right: 1px solid #2a2e39; }
        h1, h2, h3 { color: #d1d4dc !important; }
        p, label, span { color: #787b86 !important; }
        .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select { 
            background-color: #2a2e39 !important; color: #d1d4dc !important; border: 1px solid #363a45 !important; border-radius: 4px;
        }
        .stButton > button { 
            background-color: #2962ff !important; color: #ffffff !important; font-weight: 600; border: none; border-radius: 4px; width: 100%; transition: all 0.2s ease;
        }
        .stButton > button:hover { background-color: #1e53e5 !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(41, 98, 255, 0.3); }
        code { 
            background-color: #000000 !important; color: #00c853 !important; border: 1px solid #2a2e39; border-radius: 4px; font-family: 'Courier New', Courier, monospace; font-size: 0.85rem;
        }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 0.2rem; color: #d1d4dc;'>📈 VKR Day Trader Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #787b86; margin-top: 0; font-size: 1.1rem;'>Execute algorithmic trading modules directly from your browser.</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. Sidebar Navigation
st.sidebar.markdown("### 🛠️ Modules")
module = st.sidebar.radio("", [
    "1. 📰 News Monitor",
    "2. 🕵️ Pelosi Tracker",
    "3. 📊 Chart Scanner",
    "4. ⏱️ Entry Timer",
    "5. 🎯 Exit Planner",
    "6. ⏳ Time Machine Simulator",
    "7. ⚖️ Budget Manager",
    "8. 🛡️ Risk Manager",
    "9. 🏦 Order Executor",
    "10. 🔔 Price Alerts",
    "11. 📑 Earnings Analyst"
], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("💡 *Tip: Use `.NS` for Indian stocks (e.g., `RELIANCE.NS`)*")

# 4. Smart Helper Function
def run_script(command_list):
    with st.spinner(f"⚙️ Running: {command_list[1]}"):
        try:
            safe_cmd = [sys.executable] + command_list[1:]
            result = subprocess.run(safe_cmd, capture_output=True, text=True, timeout=60, cwd=os.getcwd())
            
            combined_output = result.stdout + result.stderr
            
            # SMART HANDLING: The original script sometimes returns Exit Code 1 
            # when it successfully runs but finds "Nothing new" or skips SEC filings.
            is_success = (result.returncode == 0) or \
                         ("Checked" in combined_output) or \
                         ("Nothing new" in combined_output) or \
                         ("Headlines are leads" in combined_output) or \
                         ("SEC filings skipped" in combined_output)
            
            if not is_success:
                st.error(f"❌ Script failed (Exit Code: {result.returncode})")
                if combined_output:
                    st.code(combined_output, language="bash")
            else:
                st.success("✅ Execution Successful")
                st.code(combined_output, language="bash")
                
        except FileNotFoundError:
            st.error(f"❌ File not found! Ensure '{command_list[1]}' exists in your GitHub repo.")
        except subprocess.TimeoutExpired:
            st.error("⏱️ Timeout: The script took longer than 60 seconds to run.")
        except Exception as e:
            st.error(f"❌ Critical Error: {str(e)}")

# 5. Module Logic
if module == "1. 📰 News Monitor":
    st.header("📰 News Monitor")
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Enter Ticker (e.g., AAPL or RELIANCE.NS)", "AAPL")
    with col2:
        hours = st.number_input("Lookback Hours", min_value=1, max_value=168, value=24)
    if st.button("Run News Scanner"):
        run_script(["python3", "trader-news/news.py", "--tickers", ticker.replace(" ", ""), "--hours", str(hours)])

elif module == "2. 🕵️ Pelosi Tracker":
    st.header("🕵️ Congressional Trade Tracker")
    member = st.text_input("Member Name", "pelosi")
    if st.button("Fetch Disclosures"):
        run_script(["python3", "trader-pelosi/ptr.py", "index", "--member", member])

elif module == "3. 📊 Chart Scanner":
    st.header("📊 Chart Scanner")
    scan_type = st.selectbox("Scan Type", ["orb", "daily", "universe"])
    if st.button("Start Scan"):
        if scan_type == "orb":
            run_script(["python3", "trader-scanner/scan.py", "orb", "--at", "10:15"])
        elif scan_type == "daily":
            run_script(["python3", "trader-scanner/scan.py", "daily"])
        else:
            st.info("Scanning the full universe may take several minutes.")
            run_script(["python3", "trader-scanner/scan.py", "universe"])

elif module == "4. ⏱️ Entry Timer":
    st.header("⏱️ Entry Timer")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Ticker to Watch", "TSLA")
    with col2:
        setup = st.selectbox("Setup Type", ["orb", "flag", "bounce"])
    if st.button("Check Entry Trigger"):
        run_script(["python3", "trader-entry/entry.py", "check", ticker, "--setup", setup])

elif module == "5. 🎯 Exit Planner":
    st.header("🎯 Exit Planner")
    col1, col2 = st.columns(2)
    with col1:
        stop_type = st.selectbox("Stop Loss Type", ["or-mid", "fixed", "atr"])
    with col2:
        target_type = st.selectbox("Target Type", ["1R", "2R", "fixed"])
    if st.button("Generate Exit Plan"):
        run_script(["python3", "trader-exit/exit.py", "plan", "--stop", stop_type, "--target", target_type, "--write"])

elif module == "6. ⏳ Time Machine Simulator":
    st.header("⏳ Time Machine Simulator")
    st.warning("⚠️ This simulation replays a trade setup 10,000 times and may take 15-30 seconds.")
    if st.button("Run Time Machine Simulation"):
        run_script(["python3", "trader-timemachine/timemachine.py", "run", "--write"])

elif module == "7. ⚖️ Budget Manager":
    st.header("⚖️ Budget Manager")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Total Budget ($)", value=5000)
    with col2:
        max_loss = st.number_input("Max Loss per Trade ($)", value=50)
    if st.button("Calculate Position Sizes"):
        run_script(["python3", "trader-budget/size.py", "--budget", str(budget), "--write"])

elif module == "8. 🛡️ Risk Manager":
    st.header("🛡️ Risk Manager")
    st.info("Ensure `trader/orders.json` has been generated by the Budget Manager first.")
    if st.button("Run Risk Check"):
        run_script(["python3", "trader-risk/check.py"])

elif module == "9. 🏦 Order Executor":
    st.header("🏦 Order Executor (Paper Trading)")
    st.warning("⚠️ This is set to PAPER TRADING by default. No real money is used.")
    if st.button("Show Pending Tickets"):
        run_script(["python3", "trader-broker/ticket.py", "show"])

elif module == "10. 🔔 Price Alerts":
    st.header("🔔 Price Alerts")
    action = st.selectbox("Alert Action", ["add --from-plan", "check"])
    if st.button("Manage Alerts"):
        if action == "add --from-plan":
            run_script(["python3", "trader-alerts/alerts.py", "add", "--from-plan"])
        else:
            run_script(["python3", "trader-alerts/alerts.py", "check"])

elif module == "11. 📑 Earnings Analyst":
    st.header("📑 Earnings Analyst")
    ticker = st.text_input("Enter Ticker for Earnings Analysis", "AAPL")
    if st.button("Analyze Earnings"):
        run_script(["python3", "trader-analyst/facts.py", ticker])

st.markdown("---")
st.markdown("<p style='text-align: center; color: #787b86; font-size: 0.8rem;'>Built with Streamlit • Powered by your GitHub Repository • Not Financial Advice</p>", unsafe_allow_html=True)
