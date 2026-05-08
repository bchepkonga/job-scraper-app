import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import datetime

# --- 1. PAGE CONFIG & UI THEME ---
st.set_page_config(
    page_title="Visa Job Intel | Global Talent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional "Startup" Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0E1117; }
    
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1F2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #FF4B4B;
    }
    
    /* Support Card Styling */
    .support-card {
        background-color: #111827;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
        margin-bottom: 15px;
    }
    
    /* Titles */
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Wallet Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENCE FUNCTIONS ---
def get_niches():
    return {
        # --- TECHNOLOGY (HIGH SALARY) ---
        "🤖 AI & Machine Learning": "AI Engineer OR Machine Learning OR LLM OR NLP",
        "🐍 Backend Engineering": "Python OR Go OR Node.js OR Backend OR Java OR C#",
        "🎨 Frontend & Fullstack": "React OR TypeScript OR Fullstack OR Vue OR Angular",
        "📱 Mobile Development": "iOS OR Android OR Flutter OR React Native OR Swift",
        "☁️ DevOps & Cloud": "DevOps OR SRE OR Kubernetes OR AWS OR Azure OR Cloud",
        "🛡️ Cybersecurity": "Security Engineer OR SOC OR Pentester OR Infosec",
        "📊 Data Intelligence": "Data Engineer OR Data Scientist OR Big Data OR BI",
        "🧪 QA & Testing": "QA Engineer OR Test Automation OR SDET",

        # --- HEALTHCARE (HIGHEST VOLUME SPONSORSHIP) ---
        "🏥 Nursing & Care": "Nurse OR Nursing OR RGN OR 'Care Assistant' OR 'Elderly Care'",
        "🩺 Medical Specialists": "Doctor OR Physician OR Surgeon OR 'Medical Officer'",
        "🔬 Clinical Research": "Clinical Research OR Pharma OR 'Lab Technician'",

        # --- ENGINEERING & GREEN ENERGY ---
        "⚙️ Mechanical Engineering": "Mechanical Engineer OR Automotive OR Manufacturing",
        "⚡ Electrical Engineering": "Electrical Engineer OR Electronics OR Power Systems",
        "🏗️ Civil & Construction": "Civil Engineer OR 'Structural Engineer' OR 'Project Manager Construction'",
        "🌱 Renewable Energy": "Solar OR Wind OR Sustainability OR 'Green Energy'",

        # --- BUSINESS, FINANCE & SALES ---
        "💰 Finance & Accounting": "Accountant OR 'Financial Analyst' OR Auditor OR Fintech",
        "📈 Marketing & Growth": "Digital Marketing OR SEO OR 'Growth Hacker' OR 'Brand Manager'",
        "🤝 International Sales": "'Account Executive' OR 'Sales Manager' OR 'Business Development'",
        "👥 HR & Recruitment": "'HR Manager' OR Recruiter OR 'Talent Acquisition'",

        # --- OPERATIONS & BLUE COLLAR (HIGH DEMAND) ---
        "📦 Logistics & Supply Chain": "Logistics OR 'Supply Chain' OR Warehouse OR 'Operations Manager'",
        "👨‍🍳 Hospitality & Culinary": "Chef OR 'Hotel Manager' OR 'Pastry Chef' OR Hospitality",
        "🛠️ Skilled Trades": "Electrician OR Welder OR 'CNC Operator' OR Mechanic"
    }

def score_job(description):
    if not description or not isinstance(description, str): return 0
    desc = description.lower()
    score = 0
    # Weighted Scoring System
    if any(x in desc for x in ["visa sponsorship", "sponsorship provided"]): score += 50
    if any(x in desc for x in ["relocation package", "relocation assistance", "moving support"]): score += 30
    if any(x in desc for x in ["blue card", "work permit support"]): score += 20
    return min(score, 100)

@st.cache_data(show_spinner="🕵️ Scanning European Markets...", ttl=3600)
def fetch_job_intelligence(niche_query, location, limit):
    # Advanced boolean query for high-intent results
    search_query = f"({niche_query}) AND (sponsorship OR relocation OR 'blue card')"
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=search_query,
            location=location,
            results_wanted=limit,
            hours_old=168, 
            linkedin_fetch_description=True
        )
        if not jobs.empty:
            jobs['visa_score'] = jobs['description'].apply(score_job)
            return jobs[jobs['visa_score'] > 0].sort_values(by="visa_score", ascending=False)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Scraper Error: {e}")
        return pd.DataFrame()

# --- 3. SIDEBAR (CONTROLS & PAYMENTS) ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1454165833767-027ffea9e77b?auto=format&fit=crop&q=80&w=300", 
             caption="Visa Job Intelligence Engine", use_container_width=True)
    
    st.header("🔍 Search Intel")
    niches = get_niches()
    # Use Pills for a modern mobile look if available, else Selectbox
    try:
        selected_niche = st.pills("Market Niche", options=list(niches.keys()), default="🐍 Backend Engineering")
    except:
        selected_niche = st.selectbox("Market Niche", list(niches.keys()))
        
    loc = st.text_input("Target Location", "Europe")
    job_count = st.slider("Leads Volume", 10, 100, 30)
    
    run_btn = st.button("Generate Intel Report", use_container_width=True, type="primary")

    # --- PAYMENT SECTION ---
    st.markdown("---")
    st.markdown("### ☕ Support My Work")
    st.caption("If this tool helps your career, consider a small token to keep the servers live!")
    
    st.markdown('<div class="support-card"><b>💳 PayPal:</b><br>bensonchepkonga@gmail.com</div>', unsafe_allow_html=True)
    
    st.write("₿ **Bitcoin (BTC)**")
    st.code("bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj", language="text")
    
    st.write("💵 **USDT (ERC20/BEP20)**")
    st.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9", language="text")
    
    st.write("π **Pi Network**")
    st.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC", language="text")

# --- 4. MAIN CONTENT AREA ---
st.title("🌍 Visa Job Intelligence Dashboard")
st.markdown("##### Real-time monitoring of European companies providing Visa & Relocation Support.")

if run_btn:
    data = fetch_job_intelligence(niches[selected_niche], loc, job_count)
    
    if not data.empty:
        # Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Active Leads", len(data))
        col2.metric("High Match (70%+)", len(data[data['visa_score'] >= 70]))
        col3.metric("Niche Priority", selected_niche.split()[0])

        # Data View
        st.divider()
        st.subheader("📊 High-Probability Opportunities")
        
        # Display DataFrame
        display_df = data[['visa_score', 'title', 'company', 'location', 'date_posted', 'job_url']].copy()
        display_df['visa_score'] = display_df['visa_score'].apply(lambda x: f"🔥 {x}% Match")
        
        st.dataframe(display_df, width=1200, hide_index=True)

        # Download Component
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Lead List (CSV)",
            data=csv,
            file_name=f"{selected_niche}_visa_leads.csv",
            mime='text/csv',
            use_container_width=True
        )

        # Smart Outreach
        st.divider()
        st.subheader("✉️ Application Intelligence")
        target = st.selectbox("Draft outreach for:", data['title'] + " at " + data['company'])
        if target:
            row = data[data['title'] + " at " + data['company'] == target].iloc[0]
            draft = f"Subject: Application for {row['title']} - [Your Name]\n\nDear {row['company']} Team,\n\nI am a skilled professional in {selected_niche} and I am very interested in your open role in {row['location']}. I noticed your company's commitment to international talent and sponsorship, which aligns perfectly with my relocation goals..."
            st.text_area("Tailored Email Draft:", draft, height=200)

    else:
        st.warning("No high-intent leads found in this niche today. Try expanding your location or niche segment.")

else:
    # Landing Page Info
    st.info("👈 Use the sidebar to select your tech niche and location to begin.")
    st.image("https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=1000", 
             caption="The future of global hiring.", use_container_width=True)

st.markdown("---")
st.caption("© 2026 Visa Job Intel Engine | Built with Python & Streamlit")
