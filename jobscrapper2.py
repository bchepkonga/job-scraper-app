import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import plotly.express as px
import urllib.parse
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Visa Job Intel Global | Sponsorship Search",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PI NETWORK VERIFICATION (ROOT HACK) ---
if st.query_params.get("verify") == "true":
    st.text("88b9688ea5c20c51f8d05e697ef86df8350b99482ba6f4ee0a7ea6952b15528b26da850b144273ab1433ba6faac8c59993bb2748b0c282a991b1e97fc49a3bb2")
    st.stop()

# Modern Pi SDK Handshake
st.html("""
    <script src="https://sdk.minepi.com/pi-sdk.js"></script>
    <script>
        try {
            window.Pi.init({ version: "2.0", sandbox: true });
        } catch (e) { console.log("Standard Web View"); }
    </script>
""")

# --- 3. THE 100+ GLOBAL NICHES ENGINE ---
def get_expanded_niches():
    return {
        "🤖 ARTIFICIAL INTELLIGENCE": "('AI Engineer' OR 'Machine Learning' OR 'NLP' OR 'LLM' OR 'Computer Vision' OR 'Deep Learning')",
        "🐍 PYTHON & BACKEND": "(Python OR Django OR Flask OR FastAPI OR 'Backend Developer' OR 'Django Engineer')",
        "🎨 FRONTEND & UI/UX": "(React OR Vue OR TypeScript OR 'Frontend Engineer' OR 'UI/UX Designer' OR 'Figma')",
        "☁️ CLOUD & DEVOPS": "(DevOps OR SRE OR Kubernetes OR AWS OR Azure OR GCP OR 'Cloud Engineer')",
        "🛡️ CYBERSECURITY": "('Security Engineer' OR 'Pentester' OR 'SOC Analyst' OR 'Cyber Security' OR 'Ethical Hacker')",
        "📊 DATA SCIENCE": "('Data Scientist' OR 'Data Engineer' OR 'Big Data' OR 'PowerBI' OR 'Tableau')",
        "📱 MOBILE DEVELOPMENT": "(Swift OR Kotlin OR Flutter OR 'React Native' OR 'iOS Developer' OR 'Android Developer')",
        "🎮 GAME DEVELOPMENT": "(Unity OR 'Unreal Engine' OR 'C++' OR 'Game Designer' OR '3D Artist')",
        "🏥 NURSING & CARE": "('Registered Nurse' OR 'RGN' OR 'Care Assistant' OR 'Healthcare Assistant' OR 'Midwife')",
        "🩺 MEDICAL SPECIALISTS": "(Doctor OR Physician OR Surgeon OR 'General Practitioner' OR 'Radiologist' OR 'Dentist')",
        "🦷 DENTAL & ORAL": "(Dentist OR 'Dental Hygienist' OR 'Orthodontist' OR 'Dental Technician')",
        "🧪 LAB & RESEARCH": "('Lab Technician' OR 'Biomedical Scientist' OR 'Research Assistant' OR 'Chemist')",
        "⚙️ MECHANICAL ENG": "('Mechanical Engineer' OR 'Automotive Engineer' OR 'CAD Designer' OR 'Robotics')",
        "🏗️ CIVIL & STRUCTURAL": "('Civil Engineer' OR 'Structural Engineer' OR 'Architect' OR 'BIM Manager')",
        "🌱 RENEWABLE ENERGY": "('Solar Engineer' OR 'Wind Turbine Tech' OR 'Sustainability Manager' OR 'Green Energy')",
        "🛠️ ELECTRICAL ENG": "('Electrical Engineer' OR 'PLC Programmer' OR 'Electrician' OR 'Power Systems')",
        "⚒️ SKILLED TRADES": "(Welder OR Plumber OR Carpenter OR Mason OR 'CNC Machinist' OR 'Mechanic')",
        "📦 LOGISTICS & SUPPLY": "('Supply Chain' OR 'Warehouse Manager' OR 'Logistics Coordinator' OR 'Procurement')",
        "👨‍🍳 CULINARY & CHEFS": "(Chef OR 'Pastry Chef' OR 'Sous Chef' OR 'Cook' OR 'Kitchen Manager')",
        "💰 FINANCE & ACCOUNTING": "(Accountant OR Auditor OR 'Financial Analyst' OR 'Tax Specialist' OR 'CPA')",
        "🤝 SALES & BD": "('Account Executive' OR 'Sales Manager' OR 'Business Development' OR 'Partnerships')",
        "⚖️ LEGAL & COMPLIANCE": "('Legal Counsel' OR 'Compliance Officer' OR 'Lawyer' OR 'Paralegal')",
        "🏫 EDUCATION & ESL": "('Teacher' OR 'Professor' OR 'ESL Instructor' OR 'Tutor' OR 'Lecturer')",
        "🧪 BIOTECH & PHARMA": "('Clinical Research' OR 'Pharmacist' OR 'Biotechnologist' OR 'Drug Safety')",
        "🚜 AGRICULTURE": "('Agronomist' OR 'Farm Manager' OR 'Agricultural Engineer')",
        "🚢 MARITIME & SHIPPING": "('Marine Engineer' OR 'Deck Officer' OR 'Logistics Manager')",
        "✈️ AVIATION": "('Aircraft Mechanic' OR 'Pilot' OR 'Aerospace Engineer' OR 'Avionics')"
    }

# --- 4. GLOBAL SCORING ENGINE ---
def score_visa_intel(description, location):
    if not description: return 0
    d, l = description.lower(), str(location).lower()
    score = 0
    # Core Keywords
    if any(x in d for x in ["visa sponsorship", "sponsorship provided", "sponsorship available"]): score += 50
    if "relocation" in d: score += 20
    # Global Legal Scopes
    if "uk" in l and any(x in d for x in ["skilled worker", "cos", "tier 2"]): score += 30
    if "usa" in l and "h1b" in d: score += 30
    if "canada" in l and "lmia" in d: score += 30
    if "blue card" in d: score += 30
    return min(score, 100)

@st.cache_data(show_spinner="🕵️ Scanning Global Markets...", ttl=3600)
def fetch_global_data(niche, loc, limit):
    try:
        data = scrape_jobs(site_name=["linkedin", "indeed"], search_term=f"{niche} AND (sponsorship OR relocation)", location=loc, results_wanted=limit, hours_old=168, linkedin_fetch_description=True)
        if not data.empty:
            data['visa_score'] = data.apply(lambda x: score_visa_intel(x['description'], x['location']), axis=1)
            return data[data['visa_score'] > 30].sort_values(by="visa_score", ascending=False).reset_index(drop=True)
    except: pass
    return pd.DataFrame()

# --- 5. UI STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    .job-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 16px; margin-bottom: 20px;
    }
    .selected-card { border-left: 6px solid #FF4B4B !important; background: rgba(255, 75, 75, 0.08) !important; }
    .visa-badge {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white; padding: 5px 15px; border-radius: 50px; font-size: 11px; font-weight: bold;
    }
    .donate-box {
        background: #ffdd00; color: #000; padding: 12px; border-radius: 10px;
        text-align: center; font-weight: bold; text-decoration: none; display: block; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=100) # Replaced deprecated width logic
    st.title("Search Control")
    niches = get_expanded_niches()
    niche_key = st.selectbox("Industry Niche", list(niches.keys()))
    loc_input = st.text_input("Target Location", "London, UK")
    depth = st.slider("Scrape Depth", 10, 50, 20)
    
    st.divider()
    if 'target_idx' not in st.session_state: st.session_state.target_idx = 0
    st.session_state.target_idx = st.number_input("Target Lead #", 0, 50, 0)
    
    # Modern width logic
    run_btn = st.button("🚀 Run Global Intel", type="primary", use_container_width=True)

    st.divider()
    st.markdown("### ❤️ Support Mission")
    st.markdown('<a href="https://www.paypal.com/paypalme/bchepkonga" target="_blank" class="donate-box">☕ PayPal</a>', unsafe_allow_html=True)
    with st.expander("₿ Bitcoin"):
        addr = "bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj"
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={addr}")
        st.code(addr)
    with st.expander("💵 USDT / π Pi"):
        st.caption("USDT (ERC20/BEP20)")
        st.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9")
        st.caption("Pi Wallet")
        st.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC")

# --- 7. MAIN DASHBOARD ---
st.title("🌍 Visa Job Intelligence Dashboard")

if run_btn or ('data' in st.session_state and not st.session_state.data.empty):
    if run_btn:
        st.session_state.data = fetch_global_data(niches[niche_key], loc_input, depth)
    
    df = st.session_state.data
    if not df.empty:
        if run_btn: st.balloons()
        
        t1, t2 = st.tabs(["🔥 Opportunities", "📊 Analytics"])
        
        with t1:
            # Shortcut Logic
            if st.session_state.target_idx < len(df):
                url = df.iloc[st.session_state.target_idx]['job_url']
                st.html(f"<script>window.parent.document.addEventListener('keydown', (e) => {{ if (e.ctrlKey && e.key === 'Enter') window.open('{url}', '_blank'); }});</script>")

            for idx, row in df.iterrows():
                sel = "selected-card" if idx == st.session_state.target_idx else ""
                st.markdown(f"""
                    <div class="job-card {sel}">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="visa-badge">🔥 {row['visa_score']}% MATCH</span>
                            <span style="color:#64748b; font-size:12px;">Lead #{idx}</span>
                        </div>
                        <h3 style="color:white; margin:10px 0;">{row['title']}</h3>
                        <p style="color:#94a3b8;">{row['company']} | {row['location']}</p>
                        <a href="{row['job_url']}" target="_blank" style="text-decoration:none;">
                            <button style="background:#3b82f6; color:white; border:none; padding:12px 24px; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">Apply Now</button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        with t2:
            st.plotly_chart(px.pie(df, names='location', values='visa_score', hole=0.3, template="plotly_dark"), use_container_width=True)
    else:
        st.warning("No sponsorship leads found. Try a specific city like 'Berlin' or 'Toronto'.")
else:
    st.info("👈 Use the sidebar to start your global search.")

st.divider()
wa = urllib.parse.quote("Find Visa Jobs: https://visa-job-intel.streamlit.app/")
st.markdown(f'<a href="https://wa.me/?text={wa}" target="_blank" style="background:#25D366; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:bold; display:block; text-decoration:none;">🟢 Share on WhatsApp</a>', unsafe_allow_html=True)
st.caption("© 2026 Visa Job Intel Pro | bchepkonga Solutions")
