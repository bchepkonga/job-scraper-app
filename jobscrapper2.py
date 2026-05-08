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

# --- 2. ADVANCED STYLING (Glassmorphism & Professional UI) ---
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Custom Card Styling */
    .job-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    .selected-card {
        border-left: 5px solid #FF4B4B !important;
        background: rgba(255, 75, 75, 0.05) !important;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
    }
    
    /* Badges */
    .visa-badge {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Sidebar Wallet Styling */
    .payment-container {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3b82f6;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA INTELLIGENCE LOGIC ---
def get_niches():
    return {
        "🤖 AI & Data Science": "AI Engineer OR Machine Learning OR LLM OR 'Data Scientist'",
        "🐍 Backend & Systems": "Python OR Go OR Node.js OR Backend OR Java OR Rust",
        "🎨 Frontend & Web": "React OR TypeScript OR Fullstack OR Vue OR 'Web Developer'",
        "☁️ DevOps & Cloud": "DevOps OR SRE OR Kubernetes OR AWS OR Azure OR 'Cloud Architect'",
        "🛡️ Cybersecurity": "Security Engineer OR SOC OR Pentester OR 'Cyber Security'",
        "🏥 Nursing & Medical": "Nurse OR Nursing OR Doctor OR Physician OR Surgeon",
        "⚙️ Engineering": "Mechanical OR Automotive OR Electrical OR 'Civil Engineer'",
        "🛠️ Skilled Trades": "Electrician OR Welder OR Mechanic OR Plumber OR Chef",
        "💰 Finance & Business": "Accountant OR 'Financial Analyst' OR Auditor OR 'Sales Manager'"
    }

def score_job_visa(description, location):
    if not description or not isinstance(description, str): return 0
    desc = description.lower()
    loc = location.lower()
    score = 0
    
    # Global Keywords
    if any(x in desc for x in ["visa sponsorship", "sponsorship provided"]): score += 50
    if any(x in desc for x in ["relocation package", "relocation assistance"]): score += 30
    
    # Country-Specific Logic (The 10/10 factor)
    if any(x in loc for x in ["uk", "united kingdom"]) and any(x in desc for x in ["skilled worker", "cos", "tier 2"]): score += 20
    if any(x in loc for x in ["us", "usa", "america"]) and "h1b" in desc: score += 20
    if "canada" in loc and "lmia" in desc: score += 20
    if any(x in loc for x in ["germany", "europe", "eu"]) and "blue card" in desc: score += 20
    if "australia" in loc and "482" in desc: score += 20
    
    return min(score, 100)

@st.cache_data(show_spinner="🕵️ Scanning Global Markets...", ttl=3600)
def fetch_data(niche_query, location, limit):
    # Expanded query to catch worldwide visa terms
    search_query = f"({niche_query}) AND (sponsorship OR relocation OR 'blue card' OR 'h1b' OR 'lmia' OR 'cos')"
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"],
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
        st.error(f"Search Error: {e}")
        return pd.DataFrame()

# --- 4. SIDEBAR ---
# --- SIDEBAR (CONTROLS & PATRON SECTION) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534651.png", width=80)
    st.title("Search Control")
    
    # ... (Your existing niche/loc/limit inputs here) ...
    niches = get_niches()
    selected_niche = st.selectbox("Market Sector", list(niches.keys()))
    loc = st.text_input("Region", "Global (USA, UK, Europe, Canada)")
    job_count = st.slider("Scrape Depth", 10, 100, 30)
    
    run_btn = st.button("🚀 Find Sponsored Jobs", use_container_width=True, type="primary")

    st.markdown("---")
    
    # --- NEW PATRON SECTION ---
    st.markdown("### ❤️ Support the Mission")
    st.write("This engine is free and independent. Your support helps keep the data fresh for job seekers worldwide.")

    # PayPal Button Style
    st.markdown(f'''
        <a href="https://www.paypal.com/paypalme/YOUR_LINK_HERE" target="_blank" style="text-decoration: none;">
            <div style="background-color: #ffdd00; color: #000000; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 10px;">
                ☕ Buy Me a Coffee (PayPal)
            </div>
        </a>
    ''', unsafe_allow_html=True)

    # Bitcoin QR Code Section
    with st.expander("₿ Donate with Bitcoin"):
        btc_address = "bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj"
        st.write("Scan to contribute:")
        # Generates a real QR code using a public API
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={btc_address}"
        st.image(qr_url, caption="Scan with your BTC Wallet", use_container_width=True)
        st.code(btc_address, language="text")

    # Other Crypto
    with st.expander("💵 Other Crypto (USDT/PI)"):
        st.caption("USDT (ERC20/BEP20)")
        st.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9", language="text")
        st.caption("PI Network")
        st.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC", language="text")

    st.markdown("---")
    st.caption("Built to empower global talent. Every contribution makes a difference.")
# --- 5. MAIN DISPLAY ---
st.title("🌍 Visa Job Intelligence Global")
st.markdown("#### Real-time Monitoring of Sponsorship Opportunities Worldwide.")

if run_btn or 'data' in st.session_state:
    if run_btn:
        st.session_state.data = fetch_data(niches[selected_niche], loc, job_count)
    
    data = st.session_state.data

    if not data.empty:
        # Tabbed View
        tab1, tab2 = st.tabs(["🔥 Intelligence Feed", "📊 Market Analytics"])
        
        with tab1:
            # Stats Header
            c1, c2, c3 = st.columns(3)
            c1.metric("Leads Found", len(data))
            c2.metric("High Match (70%+)", len(data[data['visa_score'] >= 70]))
            c3.metric("Geography", loc[:15])

            # Search within results
            search_query = st.text_input("🔍 Filter results (e.g. 'Senior', 'Remote', 'London')...")
            filtered_data = data[data.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

            # Keyboard Shortcut Injection
            if target_idx < len(filtered_data):
                url = filtered_data.iloc[target_idx]['job_url']
                components.html(f"""
                    <script>
                    window.parent.document.addEventListener('keydown', function(e) {{
                        if (e.ctrlKey && e.key === 'Enter') {{ window.open('{url}', '_blank'); }}
                    }});
                    </script>
                """, height=0)

            # Display Cards
            for idx, row in filtered_data.iterrows():
                is_selected = "selected-card" if idx == target_idx else ""
                st.markdown(f"""
                    <div class="job-card {is_selected}">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="visa-badge">🔥 {row['visa_score']}% VISA MATCH</span>
                            <span style="color: #64748b; font-size: 12px;">Lead #{idx}</span>
                        </div>
                        <h3 style="margin-top: 10px; color: white;">{row['title']}</h3>
                        <div style="color: #94a3b8;">🏢 {row['company']} | 📍 {row['location']}</div>
                        <div style="margin-top: 15px;">
                            <a href="{row['job_url']}" target="_blank">
                                <button style="background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">View Intelligence</button>
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.subheader("📍 Regional Hotspots")
            # Create a simple bar chart of locations
            loc_counts = data['location'].value_counts().head(10).reset_index()
            fig = px.bar(loc_counts, x='location', y='count', color='count', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Intelligence Export")
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Full CSV Report", csv, "visa_intel.csv", use_container_width=True)

    else:
        st.warning("No high-intent leads found. Try a broader search.")

else:
    st.info("👈 Enter a market niche and location in the sidebar to begin scanning.")
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

st.markdown("---")
st.caption("© 2026 Visa Job Intel Pro | Global Talent Mobility Engine | bchepkonga Business Solutions")
