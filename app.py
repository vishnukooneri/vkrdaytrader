import streamlit as st
import subprocess
import os

# Page Configuration
st.set_page_config(page_title="VKR Day Trader OS", page_icon="📈", layout="wide")

# Modern, Sleek Custom CSS for Terminal-like code blocks and clean spacing
st.markdown("""
        /* Premium Light Fintech Theme */
    .main { background-color: #ffffff !important; }
    section[data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid #e2e8f0; }
    .stButton > button { 
        background-color: #2563eb !important; 
        color: #ffffff !important; 
        font-weight: 600; 
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
    }
    .stButton > button:hover { background-color: #1d4ed8 !important; box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3); transform: translateY(-1px); }
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select { 
        background-color: #ffffff !important; 
        color: #0f172a !important; 
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px;
        transition: all 0.2s;
    }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > select:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    code { 
        background-color: #f1f5f9 !important; 
        color: #0f172a !important; 
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>📈 VKR Day Trader Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-top: 0;'>Execute all 11 algorithmic trading modules directly from your browser.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Navigation
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
st.sidebar.markdown("⚠️ *All executions default to paper trading.*")

# Helper function to run Python scripts
def run_script(command_list):
    with st.spinner(f"⚙️ Executing {command_list[1].replace('.py', '')}..."):
        try:
            result = subprocess.run(
                command_list, 
                capture_output=True, 
                text=True, 
                timeout=45,
                cwd=os.getcwd()
            )
            if result.stdout:
                st.success("✅ Execution Successful")
                st.code(result.stdout, language="bash")
            if result.stderr:
                st.warning("⚠️ Warnings / Info:")
                st.code(result.stderr, language="bash")
            if not result.stdout and not result.stderr:
                st.info("ℹ️ Script ran successfully. Check generated JSON files in the repository.")
        except subprocess.TimeoutExpired:
            st.error("⏱️ Timeout: The script took longer than 45 seconds to run.")
        except Exception as e:
            st.error(f"❌ Failed to run script: {str(e)}")

# --- 1. News Monitor ---
if module == "1. 📰 News Monitor":
    st.header("📰 News Monitor")
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Enter Ticker(s) (comma separated)", "AAPL, TSLA")
    with col2:
        hours = st.number_input("Lookback Hours", min_value=1, max_value=168, value=24)
    if st.button("Run News Scanner"):
        run_script(["python3", "trader-news/news.py", "--tickers", ticker.replace(" ", ""), "--hours", str(hours)])

# --- 2. Pelosi Tracker ---
elif module == "2. 🕵️ Pelosi Tracker":
    st.header("🕵️ Congressional Trade Tracker")
    member = st.text_input("Member Name", "pelosi")
    if st.button("Fetch Disclosures"):
        run_script(["python3", "trader-pelosi/ptr.py", "index", "--member", member])

# --- 3. Chart Scanner ---
elif module == "3. 📊 Chart Scanner":
    st.header("📊 Chart Scanner")
    scan_type = st.selectbox("Scan Type", ["orb (Opening Range Breakout)", "daily (Pre-market setups)", "universe (All ~5,900 stocks)"])
    if st.button("Start Scan"):
        if scan_type == "orb":
            run_script(["python3", "trader-scanner/scan.py", "orb", "--at", "10:15"])
        elif scan_type == "daily":
            run_script(["python3", "trader-scanner/scan.py", "daily"])
        else:
            st.info("Scanning the full universe may take several minutes.")
            run_script(["python3", "trader-scanner/scan.py", "universe"])

# --- 4. Entry Timer ---
elif module == "4. ⏱️ Entry Timer":
    st.header("⏱️ Entry Timer")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Ticker to Watch", "TSLA")
    with col2:
        setup = st.selectbox("Setup Type", ["orb", "flag", "bounce"])
    if st.button("Check Entry Trigger"):
        run_script(["python3", "trader-entry/entry.py", "check", ticker, "--setup", setup])

# --- 5. Exit Planner ---
elif module == "5. 🎯 Exit Planner":
    st.header("🎯 Exit Planner")
    col1, col2 = st.columns(2)
    with col1:
        stop_type = st.selectbox("Stop Loss Type", ["or-mid", "fixed", "atr"])
    with col2:
        target_type = st.selectbox("Target Type", ["1R", "2R", "fixed"])
    if st.button("Generate Exit Plan"):
        run_script(["python3", "trader-exit/exit.py", "plan", "--stop", stop_type, "--target", target_type, "--write"])

# --- 6. Time Machine Simulator ---
elif module == "6. ⏳ Time Machine Simulator":
    st.header("⏳ Time Machine Simulator")
    st.warning("⚠️ This simulation replays a trade setup 10,000 times and may take 15-30 seconds.")
    if st.button("Run Time Machine Simulation"):
        run_script(["python3", "trader-timemachine/timemachine.py", "run", "--write"])

# --- 7. Budget Manager ---
elif module == "7. ⚖️ Budget Manager":
    st.header("⚖️ Budget Manager")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Total Budget ($)", value=5000)
    with col2:
        max_loss = st.number_input("Max Loss per Trade ($)", value=50)
    if st.button("Calculate Position Sizes"):
        run_script(["python3", "trader-budget/size.py", "--budget", str(budget), "--write"])

# --- 8. Risk Manager ---
elif module == "8. 🛡️ Risk Manager":
    st.header("🛡️ Risk Manager")
    st.info("Ensure `trader/orders.json` has been generated by the Budget Manager first.")
    if st.button("Run Risk Check"):
        run_script(["python3", "trader-risk/check.py"])

# --- 9. Order Executor ---
elif module == "9. 🏦 Order Executor":
    st.header("🏦 Order Executor (Paper Trading)")
    st.warning("⚠️ This is set to PAPER TRADING by default. No real money is used.")
    if st.button("Show Pending Tickets"):
        run_script(["python3", "trader-broker/ticket.py", "show"])

# --- 10. Price Alerts ---
elif module == "10. 🔔 Price Alerts":
    st.header("🔔 Price Alerts")
    action = st.selectbox("Alert Action", ["add --from-plan", "check"])
    if st.button("Manage Alerts"):
        if action == "add --from-plan":
            run_script(["python3", "trader-alerts/alerts.py", "add", "--from-plan"])
        else:
            run_script(["python3", "trader-alerts/alerts.py", "check"])

# --- 11. Earnings Analyst ---
elif module == "11. 📑 Earnings Analyst":
    st.header("📑 Earnings Analyst")
    ticker = st.text_input("Enter Ticker for Earnings Analysis", "AAPL")
    if st.button("Analyze Earnings"):
        run_script(["python3", "trader-analyst/facts.py", ticker])

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Built with Streamlit • Powered by your GitHub Repository • Not Financial Advice</p>", unsafe_allow_html=True)
