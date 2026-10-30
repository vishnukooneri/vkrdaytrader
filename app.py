import streamlit as st
import subprocess
import os

# Page Configuration
st.set_page_config(page_title="VKR Day Trader OS", page_icon="📈", layout="wide")

# Custom CSS for a sleek, dark trading terminal look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border: 1px solid #4a4b57; }
    .stButton > button { background-color: #3861fb; color: white; border: none; font-weight: bold; }
    .stButton > button:hover { background-color: #2a4bd8; }
    code { background-color: #1e1e1e !important; color: #16c784 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 VKR Day Trader Command Center")
st.markdown("Run the original 11 Python trading algorithms directly from your browser.")

# Sidebar Navigation
st.sidebar.header("🛠️ Algorithm Modules")
module = st.sidebar.radio("Select a Tool:", [
    "📰 News Monitor",
    "🕵️ Pelosi Tracker",
    "⚖️ Budget & Risk Manager",
    "⏳ Time Machine Simulator",
    "📊 Chart Scanner"
])

st.sidebar.markdown("---")
st.sidebar.markdown("💡 *Tip: Use `.NS` for Indian stocks (e.g., RELIANCE.NS)*")

# Helper function to run Python scripts
def run_script(command_list):
    with st.spinner(f"Executing {command_list[1]}..."):
        try:
            # Run the script from the repository
            result = subprocess.run(
                command_list, 
                capture_output=True, 
                text=True, 
                timeout=30,
                cwd=os.getcwd() # Ensure it runs in the repo root
            )
            if result.stdout:
                st.success("✅ Execution Successful!")
                st.code(result.stdout, language="bash")
            if result.stderr:
                st.warning("⚠️ Warnings/Errors:")
                st.code(result.stderr, language="bash")
            if not result.stdout and not result.stderr:
                st.info("Script ran successfully but produced no console output.")
        except subprocess.TimeoutExpired:
            st.error("⏱️ The script took too long to run (Timeout > 30s).")
        except Exception as e:
            st.error(f"❌ Failed to run script: {str(e)}")

# --- Module 1: News Monitor ---
if module == "📰 News Monitor":
    st.header("📰 News Monitor")
    st.markdown("Tracks breaking news and 8-K filings for specific tickers.")
    col1, col2 = st.columns([1, 1])
    with col1:
        ticker = st.text_input("Enter Ticker(s) (comma separated):", "AAPL, TSLA")
    with col2:
        hours = st.number_input("Lookback Hours:", min_value=1, max_value=168, value=24)
    
    if st.button("Run News Scanner"):
        tickers_clean = ticker.replace(" ", "")
        run_script(["python3", "trader-news/news.py", "--tickers", tickers_clean, "--hours", str(hours)])

# --- Module 2: Pelosi Tracker ---
elif module == "🕵️ Pelosi Tracker":
    st.header("🕵️ Congressional Trade Tracker")
    st.markdown("Reads stock-trade disclosures from the House Clerk.")
    member = st.text_input("Member Name (e.g., pelosi, mcconnell):", "pelosi")
    
    if st.button("Fetch Disclosures"):
        run_script(["python3", "trader-pelosi/ptr.py", "index", "--member", member])

# --- Module 3: Budget & Risk ---
elif module == "⚖️ Budget & Risk Manager":
    st.header("⚖️ Budget & Risk Manager")
    st.markdown("Sizes positions and checks against risk limits.")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("Total Budget ($):", value=5000)
        max_loss = st.number_input("Max Loss per Trade ($):", value=50)
    with col2:
        st.markdown("*(Ensure `trader/orders.json` and `trader/config.json` are configured in the repo)*")
    
    if st.button("Run Budget Sizer"):
        run_script(["python3", "trader-budget/size.py", "--budget", str(budget), "--write"])
        st.markdown("---")
        run_script(["python3", "trader-risk/check.py"])

# --- Module 4: Time Machine ---
elif module == "⏳ Time Machine Simulator":
    st.header("⏳ Time Machine Simulator")
    st.markdown("Replays a trade setup 10,000 times to calculate historical odds.")
    ticker = st.text_input("Enter Ticker for Simulation:", "TSLA")
    st.warning("⚠️ This simulation may take 15-30 seconds to process 10,000 iterations.")
    
    if st.button("Run Time Machine"):
        run_script(["python3", "trader-timemachine/timemachine.py", "run", "--write"])

# --- Module 5: Chart Scanner ---
elif module == "📊 Chart Scanner":
    st.header("📊 Chart Scanner")
    st.markdown("Scans thousands of charts for setups (ORB, flags, oversold bounces).")
    scan_type = st.selectbox("Scan Type:", ["orb (Opening Range Breakout)", "daily (Pre-market setups)", "universe (All ~5,900 stocks)"])
    
    if st.button("Start Scan"):
        if scan_type == "orb":
            run_script(["python3", "trader-scanner/scan.py", "orb", "--at", "10:15"])
        elif scan_type == "daily":
            run_script(["python3", "trader-scanner/scan.py", "daily"])
        else:
            st.info("Scanning the full universe may take several minutes. Check the output below.")
            run_script(["python3", "trader-scanner/scan.py", "universe"])

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built with Streamlit • Powered by your GitHub Repository • Not Financial Advice</p>", unsafe_allow_html=True)
