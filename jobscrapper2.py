import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import plotly.express as px
import urllib.parse
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Visa Job Intel Global | Professional Search",
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

# --- 3. THE 40 GLOBAL NICHES ENGINE ---
def get_expanded_niches():
    return {
        # --- TECHNOLOGY & SOFTWARE ---
        "🤖 ARTIFICIAL INTELLIGENCE": "('AI Engineer' OR 'Machine Learning' OR 'NLP' OR 'LLM' OR 'Computer Vision')",
        "🐍 PYTHON & BACKEND": "(Python OR Django OR Flask OR FastAPI OR 'Backend Developer' OR 'Node.js')",
        "🎨 FRONTEND & UI/UX": "(React OR Vue OR TypeScript OR 'Frontend Engineer' OR 'UI/UX Designer')",
        "☁️ CLOUD & DEVOPS": "(DevOps OR SRE OR Kubernetes OR AWS OR Azure OR GCP OR 'Cloud Engineer')",
        "🛡️ CYBERSECURITY": "('Security Engineer' OR 'Pentester' OR 'SOC Analyst' OR 'Cyber Security' OR 'Information Security')",
        "📊 DATA SCIENCE & BI": "('Data Scientist' OR 'Data Engineer' OR 'Big Data' OR 'PowerBI' OR 'Business Intelligence')",
        "📱 MOBILE DEVELOPMENT": "(Swift OR Kotlin OR Flutter OR 'React Native' OR 'iOS Developer' OR 'Android Developer')",
        "🎮 GAME DEVELOPMENT": "(Unity OR 'Unreal Engine' OR 'C++' OR 'Game Designer' OR '3D Artist')",
        "🧪 QA & TESTING": "('QA Engineer' OR 'Software Tester' OR 'Automation Engineer' OR 'SDET')",
        "📦 PRODUCT MANAGEMENT": "('Product Manager' OR 'Product Owner' OR 'Technical Program Manager')",
        
        # --- MEDICAL & HEALTHCARE ---
        "🏥 NURSING & CARE": "('Registered Nurse' OR 'RGN' OR 'Care Assistant' OR 'Healthcare Assistant' OR 'Midwife')",
        "🩺 MEDICAL SPECIALISTS": "(Doctor OR Physician OR Surgeon OR 'General Practitioner' OR 'Radiologist')",
        "🦷 DENTAL & ORAL": "(Dentist OR 'Dental Hygienist' OR 'Orthodontist' OR 'Dental Technician')",
        "🧪 LAB & PHARMA": "('Biomedical Scientist' OR 'Lab Technician' OR 'Pharmacist' OR 'Drug Safety')",
        "🧠 PSYCHOLOGY & THERAPY": "('Psychologist' OR 'Psychotherapist' OR 'Mental Health Worker' OR 'Counselor')",
        "🐾 VETERINARY": "('Veterinarian' OR 'Vet Surgeon' OR 'Vet Nurse' OR 'Veterinary Technician')",
        "🦾 PHYSIOTHERAPY": "('Physiotherapist' OR 'Occupational Therapist' OR 'Sports Therapist')",
        
        # --- ENGINEERING & INDUSTRIAL ---
        "⚙️ MECHANICAL ENG": "('Mechanical Engineer' OR 'Automotive Engineer' OR 'Robotics' OR 'Manufacturing Engineer')",
        "🏗️ CIVIL & STRUCTURAL": "('Civil Engineer' OR 'Structural Engineer' OR 'Architect' OR 'BIM Manager')",
        "🌱 RENEWABLE ENERGY": "('Solar Engineer' OR 'Wind Turbine Tech' OR 'Sustainability Manager' OR 'ESG')",
        "🛠️ ELECTRICAL ENG": "('Electrical Engineer' OR 'PLC Programmer' OR 'Electrician' OR 'Control Systems')",
        "💎 MINING & GEOLOGY": "('Mining Engineer' OR 'Geologist' OR 'Drilling Engineer' OR 'Mineralogist')",
        "🏭 INDUSTRIAL MGMT": "('Plant Manager' OR 'Operations Manager' OR 'Production Supervisor')",
        
        # --- BUSINESS, FINANCE & LAW ---
        "💰 FINANCE & ACCOUNTING": "(Accountant OR Auditor OR 'Financial Analyst' OR 'Tax Specialist' OR 'CPA')",
        "🤝 SALES & BD": "('Account Executive' OR 'Sales Manager' OR 'Business Development' OR 'Partnerships')",
        "⚖️ LEGAL & COMPLIANCE": "('Legal Counsel' OR 'Compliance Officer' OR 'Lawyer' OR 'Paralegal')",
        "📈 MARKETING & SEO": "('Digital Marketing' OR 'SEO Specialist' OR 'Growth Hacker' OR 'Content Strategist')",
        "👥 HUMAN RESOURCES": "('HR Manager' OR 'Recruiter' OR 'Talent Acquisition' OR 'HRBP')",
        "🏢 REAL ESTATE": "('Property Manager' OR 'Quantity Surveyor' OR 'Real Estate Analyst')",
        
        # --- EDUCATION & SOCIAL ---
        "🏫 EDUCATION & ESL": "('Teacher' OR 'Professor' OR 'ESL Instructor' OR 'Tutor' OR 'Lecturer')",
        "🌍 NGO & DEVELOPMENT": "('Program Manager' OR 'Humanitarian Worker' OR 'International Development')",
        "🏠 SOCIAL WORK": "('Social Worker' OR 'Child Protection' OR 'Case Manager')",
        
        # --- TRADES & SERVICES ---
        "⚒️ SKILLED TRADES": "(Welder OR Plumber OR Carpenter OR Mason OR 'CNC Machinist' OR 'Mechanic')",
        "👨‍🍳 CULINARY & CHEFS": "(Chef OR 'Pastry Chef' OR 'Sous Chef' OR 'Head Cook')",
        "🏨 HOSPITALITY MGMT": "('Hotel Manager' OR 'Restaurant Manager' OR 'F&B Manager')",
        "🚚 LOGISTICS & SUPPLY": "('Supply Chain' OR 'Warehouse Manager' OR 'Logistics Coordinator')",
        
        # --- SPECIALIZED TRANSPORT ---
        "🚢 MARITIME & SHIPPING": "('Marine Engineer' OR 'Deck Officer' OR 'Vessel Manager')",
        "✈️ AVIATION": "('Aircraft Mechanic' OR 'Pilot' OR 'Aerospace Engineer' OR 'Avionics')",
        "🏎️ MOTORSPORTS": "('Race Engineer' OR 'Performance Engineer' OR 'Motorsport Technician')",
        
        # --- CREATIVE & MEDIA ---
        "🎥 VIDEO & ANIMATION": "('Video Editor' OR 'Motion Designer' OR 'Animator' OR 'VFX Artist')",
        "✍️ COPYWRITING": "('Technical Writer' OR 'Copywriter' OR 'Content Creator')"
    }

# --- 4. GLOBAL SCORING ENGINE ---
def score_visa_intel(description, location):
    if not description or pd.isna(description): return 5
    d, l = str(description).lower(), str(location).lower()
    score = 0
    # Core Keywords
    if any(x in d for x in ["visa sponsorship", "sponsorship provided", "sponsorship available", "visa support"]): score += 50
    if "relocation" in d: score += 15
    # Global Legal Scopes
    if "uk" in l and any(x in d for x in ["skilled worker", "cos", "tier 2"]): score += 35
    if "usa" in l and "h1b" in d: score += 35
    if "canada" in l and "lmia" in d: score += 35
    if "blue card" in d: score += 30
    return min(score, 100)

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_global_data(niche, loc, limit):
    try:
        data = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"], 
            search_term=f"{niche} AND (sponsorship OR relocation)", 
            location=loc, 
            results_wanted=limit, 
            hours_old=168, 
            linkedin_fetch_description=True
        )
        if not data.empty:
            data['visa_score'] = data.apply(lambda x: score_visa_intel(x.get('description', ''), x.get('location', '')), axis=1)
            return data.sort_values(by="visa_score", ascending=False).reset_index(drop=True)
    except Exception as e:
        st.error(f"Search failed: {e}")
    return pd.DataFrame()

# --- 5. UI STYLING ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .job-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px; border-radius: 16px; margin-bottom: 20px;
        transition: 0.3s;
    }
    .job-card:hover { border-color: #3b82f6; background: rgba(30, 41, 59, 1); }
    .visa-badge {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white; padding: 5px 15px; border-radius: 50px; font-size: 11px; font-weight: bold;
    }
    .apply-btn {
        display: block; width: 100%; background: #3b82f6; color: white !important;
        text-align: center; padding: 12px; border-radius: 8px; text-decoration: none;
        font-weight: bold; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/814/814513.png", width=80)
    st.title("Intel Settings")
    
    niches = get_expanded_niches()
    niche_key = st.selectbox("Select Niche", list(niches.keys()))
    loc_input = st.text_input("Target Location", "United Kingdom")
    depth = st.slider("Scrape Depth", 10, 100, 30)
    
    st.divider()
    min_score = st.slider("Minimum Visa Score Filter", 0, 100, 30)
    
    run_btn = st.button("🚀 Run Global Intel", type="primary", use_container_width=True)

    # SUPPORT SECTION
    st.divider()
    st.markdown("### ❤️ Support the Mission")
    
    pay_url = "https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=bensonchepkonga@gmail.com&item_name=Visa+Job+Intel+Support&currency_code=USD"
    st.markdown(f'<a href="{pay_url}" target="_blank" style="text-decoration:none;"><div style="background:#ffdd00; color:#000; padding:10px; border-radius:8px; text-align:center; font-weight:bold;">☕ Buy Me a Coffee</div></a>', unsafe_allow_html=True)

    with st.expander("₿ Crypto & Pi"):
        st.caption("Bitcoin (BTC)")
        st.code("bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj", language="text")
        st.caption("USDT (ERC20/BEP20)")
        st.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9", language="text")
        st.caption("Pi Network Wallet")
        st.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC", language="text")

# --- 7. MAIN DASHBOARD ---
st.title("🌍 Visa Job Intelligence Dashboard")
st.markdown(f"Current Intelligence: **{niche_key}** in **{loc_input}**")

if run_btn:
    with st.status("🕵️ Scanning International Markets...", expanded=True) as status:
        df = fetch_global_data(niches[niche_key], loc_input, depth)
        st.session_state.data = df
        status.update(label="Scanning Complete!", state="complete", expanded=False)

if 'data' in st.session_state and not st.session_state.data.empty:
    df = st.session_state.data
    # Post-scrape filtering
    filtered_df = df[df['visa_score'] >= min_score].copy()

    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Leads Found", len(filtered_df))
    m2.metric("High Match (>70%)", len(filtered_df[filtered_df['visa_score'] >= 70]))
    m3.metric("Scanned Locations", filtered_df['location'].nunique())

    tab1, tab2 = st.tabs(["🔥 Opportunities Feed", "📊 Market Analytics"])

    with tab1:
        if filtered_df.empty:
            st.warning("No jobs met your Score Filter. Try lowering the 'Min Visa Score' in the sidebar.")
        else:
            for idx, row in filtered_df.iterrows():
                st.markdown(f"""
                    <div class="job-card">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="visa-badge">🔥 {row['visa_score']}% VISA PROBABILITY</span>
                            <span style="color:#64748b; font-size:12px;">ID: {idx}</span>
                        </div>
                        <h2 style="color:white; margin:15px 0 5px 0; font-size:20px;">{row['title']}</h2>
                        <p style="color:#3b82f6; font-weight:bold; margin-bottom:2px;">{row['company']}</p>
                        <p style="color:#94a3b8; font-size:14px; margin-bottom:15px;">📍 {row['location']}</p>
                        <div style="color:#cbd5e1; font-size:14px; line-height:1.5;">{str(row['description'])[:300]}...</div>
                        <a href="{row['job_url']}" target="_blank" class="apply-btn">View Lead & Apply</a>
                    </div>
                """, unsafe_allow_html=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig_pie = px.pie(filtered_df, names='location', title="Geographic Distribution", template="plotly_dark", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            top_cos = filtered_df['company'].value_counts().nlargest(10).reset_index()
            fig_bar = px.bar(top_cos, x='count', y='company', orientation='h', title="Top Sponsoring Employers", template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Download Data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Intel Report (CSV)", csv, "visa_leads.csv", "text/csv", use_container_width=True)

else:
    if not run_btn:
        st.info("👈 Use the sidebar to select your niche and target country, then click 'Run Global Intel'.")

# --- FOOTER ---
st.divider()
wa_text = urllib.parse.quote("Found a tool for Visa Sponsorship jobs! 🌍 Check it out: https://visa-job-intel.streamlit.app/")
st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="text-decoration:none;"><div style="background:#25D366; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:bold;">🟢 Share Intel on WhatsApp</div></a>', unsafe_allow_html=True)
st.caption("© 2026 Visa Job Intel Pro | Developed by bchepkonga Solutions")
