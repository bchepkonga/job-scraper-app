import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import plotly.express as px
import datetime
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Visa Job Intel Global | Sponsorship Search Engine",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL INITIALIZATION (Fixes NameErrors) ---
if 'target_idx' not in st.session_state:
    st.session_state.target_idx = 0

# --- 3. PREMIUM UI STYLING ---
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    
    /* Job Card Glassmorphism */
    .job-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 15px; margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: #3b82f6; transform: translateY(-3px);
    }
    .selected-card {
        border-left: 6px solid #FF4B4B !important;
        background: rgba(255, 75, 75, 0.07) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Metrics Row */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 12px;
    }
    
    /* Badge */
    .visa-badge {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white; padding: 4px 14px; border-radius: 50px;
        font-size: 12px; font-weight: bold;
    }
    
    /* Donation Styling */
    .donate-btn {
        background: #ffdd00; color: #000; padding: 12px;
        border-radius: 10px; text-align: center; font-weight: bold;
        text-decoration: none; display: block; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. THE COMPLETE GLOBAL NICHES ---
def get_niches():
    return {
        # TECH
        "🤖 AI & Machine Learning": "AI Engineer OR Machine Learning OR LLM OR NLP",
        "🐍 Backend & Python": "Python OR Go OR Node.js OR Backend OR Java",
        "🎨 Frontend & Web": "React OR TypeScript OR Fullstack OR Vue",
        "☁️ DevOps & SRE": "DevOps OR SRE OR Kubernetes OR AWS OR Azure",
        "🛡️ Cybersecurity": "Security Engineer OR SOC OR Pentester",
        "📊 Data & Analytics": "Data Engineer OR Data Scientist OR Big Data",
        
        # HEALTHCARE
        "🏥 Nursing & Care": "Nurse OR Nursing OR RGN OR 'Care Assistant'",
        "🩺 Medical Specialists": "Doctor OR Physician OR Surgeon",
        
        # ENGINEERING
        "⚙️ Mechanical/Auto": "Mechanical Engineer OR Automotive OR Manufacturing",
        "🏗️ Civil & Structural": "Civil Engineer OR 'Structural Engineer'",
        "🌱 Renewable Energy": "Solar OR Wind OR Sustainability",
        
        # SKILLED TRADES
        "👨‍🍳 Culinary & Hotels": "Chef OR 'Hotel Manager' OR 'Pastry Chef'",
        "🛠️ Trades: Welder/Electrician": "Electrician OR Welder OR Mechanic OR Plumber",
        "📦 Logistics": "Logistics OR 'Supply Chain' OR Warehouse",
        
        # CORPORATE
        "💰 Finance & Audit": "Accountant OR 'Financial Analyst' OR Auditor",
        "🤝 International Sales": "'Account Executive' OR 'Sales Manager'"
    }

# --- 5. THE ULTIMATE SCORING ENGINE ---
def score_job_visa(description, location):
    if not description or not isinstance(description, str): return 0
    desc = description.lower()
    loc = str(location).lower()
    score = 0
    
    # 1. High Intent Keywords (Universal)
    if any(x in desc for x in ["visa sponsorship", "sponsorship provided", "sponsorship available"]): score += 50
    if any(x in desc for x in ["relocation package", "relocation assistance", "moving support"]): score += 20
    
    # 2. Country Specific Intelligence
    # UK Logic
    if any(x in loc for x in ["uk", "united kingdom", "london"]):
        if any(x in desc for x in ["skilled worker", "cos ", "tier 2"]): score += 30
    # USA Logic
    if any(x in loc for x in ["us", "usa", "america", "states"]):
        if "h1b" in desc: score += 30
    # Canada Logic
    if "canada" in loc and "lmia" in desc: score += 30
    # EU Logic
    if any(x in loc for x in ["germany", "berlin", "netherlands", "europe", "eu"]):
        if "blue card" in desc: score += 30
        
    return min(score, 100)

@st.cache_data(show_spinner="🛰️ Scanning Global Markets...", ttl=3600)
def fetch_data(niche_query, location, limit):
    # Stabilized site list (Glassdoor is currently unstable for global queries)
    sites = ["linkedin", "indeed"]
    search_query = f"({niche_query}) AND (sponsorship OR relocation OR 'visa' OR 'h1b' OR 'lmia' OR 'cos')"
    try:
        jobs = scrape_jobs(
            site_name=sites,
            search_term=search_query,
            location=location,
            results_wanted=limit,
            hours_old=168, 
            linkedin_fetch_description=True
        )
        if not jobs.empty:
            jobs['visa_score'] = jobs.apply(lambda x: score_job_visa(x['description'], x['location']), axis=1)
            return jobs[jobs['visa_score'] > 30].sort_values(by="visa_score", ascending=False).reset_index(drop=True)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Search Engine Sync Issue: {e}")
        return pd.DataFrame()

# --- 6. SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=80)
    st.title("Global Search")
    
    niches = get_niches()
    selected_niche = st.selectbox("Market Sector", list(niches.keys()))
    
    # Using specific locations improves scraper success
    loc_input = st.text_input("Target Region", "London, UK")
    job_count = st.slider("Scrape Depth", 10, 100, 30)
    
    st.markdown("### ⌨️ Lead Navigation")
    # Store target_idx in session state to prevent NameError
    st.session_state.target_idx = st.number_input("Target Lead #", min_value=0, max_value=job_count-1, value=0)
    st.caption("Press **Ctrl + Enter** to apply to the targeted lead.")

    run_btn = st.button("🚀 Run Intelligence Report", use_container_width=True, type="primary")

    st.divider()
    
    # --- PATRON & DONATION SECTION ---
    st.markdown("### ❤️ Support the Mission")
    st.write("Help keep this global engine free and independent.")

    st.markdown(f'''
        <a href="https://www.paypal.com/paypalme/bchepkonga" target="_blank" class="donate-btn">
            ☕ Buy Me a Coffee (PayPal)
        </a>
    ''', unsafe_allow_html=True)

    with st.expander("₿ Bitcoin Donation (QR Code)"):
        btc_addr = "bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={btc_addr}"
        st.image(qr_url, caption="Scan with BTC Wallet", use_container_width=True)
        st.code(btc_addr, language="text")

    with st.expander("💵 Other Crypto (USDT/PI)"):
        st.caption("USDT (ERC20/BEP20)")
        st.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9", language="text")
        st.caption("PI Network")
        st.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC", language="text")

# --- 7. MAIN DISPLAY ---
st.title("🌍 Visa Job Intelligence Dashboard")
st.markdown("##### Monitoring companies providing Visa Sponsorship & Relocation worldwide.")

if run_btn or 'data' in st.session_state:
    if run_btn:
        st.session_state.data = fetch_data(niches[selected_niche], loc_input, job_count)
    
    data = st.session_state.get('data', pd.DataFrame())

    if not data.empty:
        # Metrics
        st.balloons()
        m1, m2, m3 = st.columns(3)
        m1.metric("Leads Identified", len(data))
        m2.metric("High Probability (70%+)", len(data[data['visa_score'] >= 70]))
        m3.metric("Scanned Location", loc_input)

        # Tabs
        tab_feed, tab_stats = st.tabs(["🔥 Opportunities Feed", "📊 Market Trends"])
        
        with tab_feed:
            search_filter = st.text_input("🔍 Quick Filter (e.g. 'Senior', 'Remote')")
            filtered = data[data.apply(lambda r: search_filter.lower() in str(r).lower(), axis=1)]

            # Shortcode Logic
            if st.session_state.target_idx < len(filtered):
                url = filtered.iloc[st.session_state.target_idx]['job_url']
                components.html(f"""
                    <script>
                    window.parent.document.addEventListener('keydown', function(e) {{
                        if (e.ctrlKey && e.key === 'Enter') {{ window.open('{url}', '_blank'); }}
                    }});
                    </script>
                """, height=0)

            # Cards
            for idx, row in filtered.iterrows():
                is_selected = "selected-card" if idx == st.session_state.target_idx else ""
                st.markdown(f"""
                    <div class="job-card {is_selected}">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="visa-badge">🔥 {row['visa_score']}% VISA MATCH</span>
                            <span style="color:#64748b; font-size:12px;">Lead #{idx}</span>
                        </div>
                        <h3 style="color:white; margin-top:10px;">{row['title']}</h3>
                        <div style="color:#94a3b8; font-size:14px;">🏢 {row['company']} | 📍 {row['location']}</div>
                        <div style="margin-top:15px; display:flex; justify-content: space-between; align-items:center;">
                            <a href="{row['job_url']}" target="_blank" style="text-decoration:none;">
                                <button style="background:#3b82f6; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-weight:bold;">Apply Now</button>
                            </a>
                            {f'<span style="color:#3b82f6; font-size:12px; font-weight:bold;">🎯 TARGETED: Press Ctrl+Enter</span>' if idx == st.session_state.target_idx else ''}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with tab_stats:
            st.subheader("📍 Regional Distribution")
            fig = px.pie(data, names='location', values='visa_score', hole=0.3, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📥 Export Intelligence")
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Download Leads (CSV)", csv, "visa_intel.csv", "text/csv", use_container_width=True)

    else:
        st.warning("No high-intent leads found. Try a specific city or different niche.")

else:
    st.info("👈 Use the sidebar to begin your intelligence search.")
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

st.markdown("---")
st.caption("© 2026 Visa Job Intel Pro | bchepkonga Business Solutions")
