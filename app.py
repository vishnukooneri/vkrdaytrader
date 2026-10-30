import streamlit as st
import subprocess
import os
import json

# Page Configuration
st.set_page_config(page_title="VKR Day Trader OS", page_icon="📈", layout="wide")

# Custom CSS for a sleek, dark trading terminal look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input { background-color: #262730; color: white; border: 1px solid #4a4b57; }
    .stButton > button { background-color: #3861fb; color: white; border: none; font-weight: bold; width: 100%; }
    .stButton > button:hover { background-color: #2a4bd8; }
    .stSelectbox > div > div > select { background-color: #262730; color: white; border: 1px solid #4a4b57; }
    code { background-color: #1e1e1e !important; color: #16c784 !important; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 VKR Day Trader Command Center")
st.markdown("Run all 11 original Python trading algorithms directly from your browser.")

# Sidebar Navigation (ALL 11 MODULES)
st.sidebar.header("🛠️ Algorithm Modules")
module = st.sidebar.radio("Select a Tool:", [
    "1. 📰 News Monitor",
    "2. 🕵️ Pelosi Tracker",
    "3. 📊 Chart Scanner",
    "4. ⏱️ Entry Timer",
    "5. 🎯 Exit Planner",
    "6. ⏳ Time Machine Simulator",
    "7. ⚖️ Budget Manager",
    "8. 🛡️ Risk Manager",
    "9. 🏦 Order Executor (Broker)",
    "10. 🔔 Price Alerts",
    "11. 📑 Earnings Analyst"
])

st.sidebar.markdown("---")
st.sidebar.markdown("💡 *Tip: Use `.NS` for Indian stocks (e.g., RELIANCE.NS)*")
st.sidebar.markdown("⚠️ *All trades default to paper trading.*")

# Helper function to run Python scripts
def run_script(command_list):
    with st.spinner(f"Executing {command_list[1]}..."):
        try:
            result = subprocess.run(
                command_list, 
                capture_output=True, 
                text=True, 
                timeout=45, # Increased timeout for heavier scripts like Time Machine
                cwd=os.getcwd()
            )
            if result.stdout:
                st.success("✅ Execution Successful!")
                st.code(result.stdout, language="bash")
            if result.stderr:
                st.warning("⚠️ Warnings/Errors:")
                st.code(result.stderr, language="bash")
            if not result.stdout and not result.stderr:
                st.info("Script ran successfully but produced no console output (check generated JSON files in repo).")
        except subprocess.TimeoutExpired:
            st.error("⏱️ The script took too long to run (Timeout > 45s).")
        except Exception as e:
            st.error(f"❌ Failed to run script: {str(e)}")

# --- 1. News Monitor ---
if module == "1. 📰 News Monitor":
    st.header("📰 News Monitor")
    st.markdown("Tracks breaking news and 8-K filings for specific tickers.")
    col1, col2 = st.columns([2, 1])
    with col1:
        ticker = st.text_input("Enter Ticker(s) (comma separated):", "AAPL, TSLA")
    with col2:
        hours = st.number_input("Lookback Hours:", min_value=1, max_value=168, value=24)
    if st.button("Run News Scanner"):
        tickers_clean = ticker.replace(" ", "")
        run_script(["python3", "trader-news/news.py", "--tickers", tickers_clean, "--hours", str(hours)])

# --- 2. Pelosi Tracker ---
elif module == "2. 🕵️ Pelosi Tracker":
    st.header("🕵️ Congressional Trade Tracker")
    st.markdown("Reads stock-trade disclosures from the House Clerk.")
    member = st.text_input("Member Name (e.g., pelosi, mcconnell):", "pelosi")
    if st.button("Fetch Disclosures"):
        run_script(["python3", "trader-pelosi/ptr.py", "index", "--member", member])

# --- 3. Chart Scanner ---
elif module == "3. 📊 Chart Scanner":
    st.header("📊 Chart Scanner")
    st.markdown("Scans charts for setups: opening-range breakouts, flags, oversold bounces.")
    scan_type = st.selectbox("Scan Type:", ["orb (Opening Range Breakout)", "daily (Pre-market setups)", "universe (All ~5,900 stocks)"])
    if st.button("Start Scan"):
        if scan_type == "orb":
            run_script(["python3", "trader-scanner/scan.py", "orb", "--at", "10:15"])
        elif scan_type == "daily":
            run_script(["python3", "trader-scanner/scan.py", "daily"])
        else:
            st.info("Scanning the full universe may take several minutes. Check the output below.")
            run_script(["python3", "trader-scanner/scan.py", "universe"])

# --- 4. Entry Timer ---
elif module == "4. ⏱️ Entry Timer":
    st.header("⏱️ Entry Timer")
    st.markdown("Watches a setup bar by bar and tells you the moment to get in.")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Ticker to Watch:", "TSLA")
    with col2:
        setup = st.selectbox("Setup Type:", ["orb", "flag", "bounce"])
    if st.button("Check Entry Trigger"):
        run_script(["python3", "trader-entry/entry.py", "check", ticker, "--setup", setup])

# --- 5. Exit Planner ---
elif module == "5. 🎯 Exit Planner":
    st.header("🎯 Exit Planner")
    st.markdown("Sets your stop and target before you enter, so you know when to get out.")
    col1, col2 = st.columns(2)
    with col1:
        stop_type = st.selectbox("Stop Loss Type:", ["or-mid", "fixed", "atr"])
    with col2:
        target_type = st.selectbox("Target Type:", ["1R", "2R", "fixed"])
    if st.button("Generate Exit Plan"):
        run_script(["python3", "trader-exit/exit.py", "plan", "--stop", stop_type, "--target", target_type, "--write"])

# --- 6. Time Machine Simulator ---
elif module == "6. ⏳ Time Machine Simulator":
    st.header("⏳ Time Machine Simulator")
    st.markdown("Replays a trade setup 10,000 times to calculate historical odds before you risk a dollar.")
    st.warning("⚠️ This simulation may take 15-30 seconds to process 10,000 iterations.")
    if st.button("Run Time Machine Simulation"):
        run_script(["python3", "trader-timemachine/timemachine.py", "run", "--write"])

# --- 7. Budget Manager ---
elif module == "7. ⚖️ Budget Manager":
    st.header("⚖️ Budget Manager")
    st.markdown("Sizes every position to your budget and your max loss per trade.")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Total Budget ($):", value=5000)
    with col2:
        max_loss = st.number_input("Max Loss per Trade ($):", value=50)
    if st.button("Calculate Position Sizes"):
        run_script(["python3", "trader-budget/size.py", "--budget", str(budget), "--write"])

# --- 8. Risk Manager ---
elif module == "8. 🛡️ Risk Manager":
    st.header("🛡️ Risk Manager")
    st.markdown("Checks every proposed trade against your limits and stops anything over them.")
    st.info("Ensure `trader/orders.json` has been generated by the Budget Manager first.")
    if st.button("Run Risk Check"):
        run_script(["python3", "trader-risk/check.py"])

# --- 9. Order Executor (Broker) ---
elif module == "9. 🏦 Order Executor":
    st.header("🏦 Order Executor (Paper Trading)")
    st.markdown("Shows approved orders. Requires your explicit 'yes' to execute via Alpaca paper account.")
    st.warning("⚠️ This is set to PAPER TRADING by default. No real money is used.")
    if st.button("Show Pending Tickets"):
        run_script(["python3", "trader-broker/ticket.py", "show"])

# --- 10. Price Alerts ---
elif module == "10. 🔔 Price Alerts":
    st.header("🔔 Price Alerts")
    st.markdown("Rings when a price, a stop, a target, or the opening bell hits.")
    action = st.selectbox("Alert Action:", ["add --from-plan", "check"])
    if st.button("Manage Alerts"):
        if action == "add --from-plan":
            run_script(["python3", "trader-alerts/alerts.py", "add", "--from-plan"])
        else:
            run_script(["python3", "trader-alerts/alerts.py", "check"])

# --- 11. Earnings Analyst ---
elif module == "11. 📑 Earnings Analyst":
    st.header("📑 Earnings Analyst")
    st.markdown("Reads earnings reports and sums up what changed (Revenue, EPS, Margins).")
    ticker = st.text_input("Enter Ticker for Earnings Analysis:", "AAPL")
    if st.button("Analyze Earnings"):
        run_script(["python3", "trader-analyst/facts.py", ticker])

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built with Streamlit • Powered by your GitHub Repository • Not Financial Advice</p>", unsafe_allow_html=True)
