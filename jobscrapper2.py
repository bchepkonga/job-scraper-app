import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import plotly.express as px
import urllib.parse
import streamlit.components.v1 as components
import datetime
import streamlit as st

# --- PI NETWORK VERIFICATION HACK ---
# This checks if the bot is looking for the key and displays it if so
try:
    if "validation-key" in st.query_params:
        st.write("88b9688ea5c20c51f8d05e697ef86df8350b99482ba6f4ee0a7ea6952b15528b26da850b144273ab1433ba6faac8c59993bb2748b0c282a991b1e97fc49a3bb2")
        st.stop()
except:
    pass
def pi_sdk_integration():
    # This script initializes the Pi SDK inside the Pi Browser
    pi_js_code = """
    <script src="https://sdk.minepi.com/pi-sdk.js"></script>
    <script>
        const Pi = window.Pi;
        Pi.init({ version: "2.0", sandbox: true }); // Set sandbox: false for production

        async function authPi() {
            try {
                const scopes = ['username', 'payments'];
                const auth = await Pi.authenticate(scopes, onIncompletePaymentFound);
                console.log("Logged in as: " + auth.user.username);
            } catch (err) {
                console.error(err);
            }
        }

        function onIncompletePaymentFound(payment) {
            console.log("Incomplete payment found", payment);
        };

        authPi();
    </script>
    """
    components.html(pi_js_code, height=0)

# Run the integration
pi_sdk_integration()
# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Visa Job Intel Global | Sponsorship Search Engine",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE INITIALIZATION (Prevents NameErrors & Data Loss) ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'target_idx' not in st.session_state:
    st.session_state.target_idx = 0

# --- 3. PREMIUM UI STYLING (Glassmorphism & Mobile-Ready) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    
    /* Glassmorphism Job Cards */
    .job-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 16px; margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .job-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #3b82f6; transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .selected-card {
        border-left: 6px solid #FF4B4B !important;
        background: rgba(255, 75, 75, 0.08) !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.2);
    }
    
    /* Professional Badges & Metrics */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 12px;
    }
    .visa-badge {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white; padding: 5px 15px; border-radius: 50px;
        font-size: 11px; font-weight: 800; letter-spacing: 0.5px;
    }
    
    /* Navigation & Buttons */
    .stButton > button { width: 100%; border-radius: 10px !important; height: 48px; font-weight: bold; }
    .apply-btn {
        background: #3b82f6; color: white; border: none; padding: 12px 24px;
        border-radius: 8px; font-weight: bold; text-decoration: none; display: block;
        width: 100%; text-align: center;
    }
    
    /* Donation & Share UI */
    .donate-box {
        background: #ffdd00; color: black; padding: 12px; border-radius: 10px;
        text-align: center; font-weight: bold; text-decoration: none; display: block; margin-bottom: 10px;
    }
    .wa-btn {
        background: #25D366; color: white; padding: 15px; border-radius: 12px;
        text-align: center; font-weight: bold; text-decoration: none; display: block; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA LOGIC: 16 GLOBAL NICHES ---
def get_niches():
    return {
        "🤖 AI & Machine Learning": "AI Engineer OR Machine Learning OR LLM OR NLP",
        "🐍 Backend & Python": "Python OR Go OR Node.js OR Backend OR Java OR Rust",
        "🎨 Frontend & Web": "React OR TypeScript OR Fullstack OR Vue",
        "☁️ DevOps & Cloud": "DevOps OR SRE OR Kubernetes OR AWS OR Azure",
        "🛡️ Cybersecurity": "Security Engineer OR SOC OR Pentester OR 'Cyber Security'",
        "📊 Data Intelligence": "Data Engineer OR 'Big Data' OR 'Analytics Engineer'",
        "🏥 Nursing & Care": "Nurse OR Nursing OR RGN OR 'Care Assistant'",
        "🩺 Medical Specialists": "Doctor OR Physician OR Surgeon",
        "⚙️ Mechanical & Auto": "Mechanical Engineer OR Automotive OR Manufacturing",
        "🏗️ Civil & Structural": "Civil Engineer OR 'Structural Engineer' OR Architect",
        "👨‍🍳 Culinary & Hospitality": "Chef OR 'Hotel Manager' OR 'Pastry Chef'",
        "🛠️ Skilled Trades": "Electrician OR Welder OR Mechanic OR Plumber",
        "📦 Logistics & Supply": "Logistics OR 'Supply Chain' OR Warehouse",
        "💰 Finance & Audit": "Accountant OR 'Financial Analyst' OR Auditor",
        "🤝 International Sales": "'Account Executive' OR 'Sales Manager'",
        "⚖️ Legal & Compliance": "Lawyer OR 'Compliance Officer' OR 'Legal Counsel'"
    }

# --- 5. DATA LOGIC: GLOBAL SCORING ENGINE ---
def score_job_visa(description, location):
    if not description or not isinstance(description, str): return 0
    desc, loc = description.lower(), str(location).lower()
    score = 0
    
    # Universal Intent (+50)
    if any(x in desc for x in ["visa sponsorship", "sponsorship provided", "sponsorship available"]): score += 50
    if any(x in desc for x in ["relocation package", "relocation assistance"]): score += 20
    
    # Global Legal Frameworks (+30)
    # UK: Skilled Worker / CoS
    if any(x in loc for x in ["uk", "united kingdom", "london"]):
        if any(x in desc for x in ["skilled worker", "cos ", "tier 2"]): score += 30
    # USA: H1B
    if any(x in loc for x in ["us", "usa", "america"]) and "h1b" in desc: score += 30
    # Canada: LMIA
    if "canada" in loc and "lmia" in desc: score += 30
    # Europe: Blue Card
    if any(x in loc for x in ["germany", "europe", "eu", "netherlands"]) and "blue card" in desc: score += 30
    # Australia: 482/186
    if "australia" in loc and any(x in desc for x in ["482", "186"]): score += 30
        
    return min(score, 100)

@st.cache_data(show_spinner="🛰️ Scanning Global Markets...", ttl=3600)
def fetch_data(niche_query, location, limit):
    search_query = f"({niche_query}) AND (sponsorship OR relocation OR 'visa')"
    try:
        # Sites limited to LinkedIn/Indeed for stability
        jobs = scrape_jobs(site_name=["linkedin", "indeed"], search_term=search_query, location=location, results_wanted=limit, hours_old=168, linkedin_fetch_description=True)
        if not jobs.empty:
            jobs['visa_score'] = jobs.apply(lambda x: score_job_visa(x['description'], x['location']), axis=1)
            return jobs[jobs['visa_score'] > 30].sort_values(by="visa_score", ascending=False).reset_index(drop=True)
    except Exception as e:
        st.error(f"Engine Sync Error: {e}")
    return pd.DataFrame()

# --- 6. SIDEBAR CONTROL & FULL PAYMENT SUITE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=80)
    st.title("Global Control")
    
    niches = get_niches()
    selected_niche = st.selectbox("Market Sector", list(niches.keys()))
    loc_input = st.text_input("Target Region", "London, UK")
    job_count = st.slider("Search Depth", 10, 100, 30)
    
    st.divider()
    st.markdown("### ⌨️ Navigation")
    st.session_state.target_idx = st.number_input("Target Lead #", 0, 100, 0)
    st.caption("Press **Ctrl + Enter** to apply instantly.")

    run_btn = st.button("🚀 Run Intelligence", use_container_width=True, type="primary")

    st.divider()
    st.markdown("### ❤️ Support the Mission")
    
    # 1. PayPal
    st.markdown(f'''<a href="https://www.paypal.com/paypalme/bchepkonga" target="_blank" class="donate-box">☕ Buy Me a Coffee (PayPal)</a>''', unsafe_allow_html=True)
    
    # 2. Bitcoin with QR
    with st.expander("₿ Bitcoin (QR Code)"):
        btc_addr = "bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj"
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={btc_addr}")
        st.code(btc_addr, language="text")
        st.caption("Network: Bitcoin")

    # 3. USDT (Multi-chain)
    with st.expander("💵 USDT (Stablecoin)"):
        usdt_addr = "0x8a9b66289f819dccfc7f77b219d5e30747e40da9"
        st.write("**ERC20 / BEP20 / Polygon**")
        st.code(usdt_addr, language="text")

    # 4. Pi Network
    with st.expander("π Pi Network"):
        pi_addr = "MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC"
        st.code(pi_addr, language="text")
        st.caption("Send via Pi Browser Wallet")

    st.divider()
    with st.expander("📲 Mobile App Mode"):
        st.write("Chrome Menu > Add to Home Screen")

# --- 7. MAIN DASHBOARD ---
st.title("🌍 Visa Job Intelligence Dashboard")
st.markdown("##### Monitoring global companies providing Visa Sponsorship & Relocation.")

if run_btn or not st.session_state.data.empty:
    if run_btn:
        st.session_state.data = fetch_data(niches[selected_niche], loc_input, job_count)
    
    data = st.session_state.data

    if not data.empty:
        st.balloons()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Leads Identified", len(data))
        m2.metric("High Match (70%+)", len(data[data['visa_score'] >= 70]))
        m3.metric("Target Location", loc_input)

        tab_feed, tab_stats = st.tabs(["🔥 Opportunities Feed", "📊 Market Analytics"])
        
        with tab_feed:
            search_filter = st.text_input("🔍 Filter results...")
            filtered = data[data.apply(lambda r: search_filter.lower() in str(r).lower(), axis=1)]

            # Shortcut Engine
            if st.session_state.target_idx < len(filtered):
                url = filtered.iloc[st.session_state.target_idx]['job_url']
                components.html(f"""<script>window.parent.document.addEventListener('keydown', (e) => {{ if (e.ctrlKey && e.key === 'Enter') window.open('{url}', '_blank'); }});</script>""", height=0)

            for idx, row in filtered.iterrows():
                is_selected = "selected-card" if idx == st.session_state.target_idx else ""
                st.markdown(f"""
                    <div class="job-card {is_selected}">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="visa-badge">🔥 {row['visa_score']}% VISA MATCH</span>
                            <span style="color:#64748b; font-size:12px;">Lead #{idx}</span>
                        </div>
                        <h3 style="color:white; margin:15px 0 5px 0;">{row['title']}</h3>
                        <div style="color:#94a3b8; font-size:14px; margin-bottom:20px;">🏢 {row['company']} | 📍 {row['location']}</div>
                        <a href="{row['job_url']}" target="_blank" class="apply-btn">Apply Now</a>
                    </div>
                """, unsafe_allow_html=True)
        
        with tab_stats:
            st.plotly_chart(px.pie(data, names='location', values='visa_score', hole=0.3, template="plotly_dark"), use_container_width=True)
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", csv, "visa_intel.csv", "text/csv", use_container_width=True)

    else:
        st.warning("No high-intent leads found. Try a specific city like 'London' or 'Toronto'.")

else:
    st.info("👈 Use the sidebar to start your intelligence search.")
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

# --- 8. WHATSAPP SHARE FOOTER ---
st.divider()
wa_msg = urllib.parse.quote("Find Visa Sponsorship Jobs here: https://visa-job-intel.streamlit.app/")
st.markdown(f'<a href="https://wa.me/?text={wa_msg}" target="_blank" class="wa-btn">🟢 Share Intelligence via WhatsApp</a>', unsafe_allow_html=True)
st.caption("© 2026 Visa Job Intel Pro | bchepkonga Solutions")
