import streamlit as st
import pandas as pd
from jobspy import scrape_jobs
import datetime

# --- SETTINGS ---
st.set_page_config(page_title="Global Talent Intel 2026", layout="wide", page_icon="🌍")

# Custom CSS for a professional "Business Intelligence" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INTELLIGENCE DATA ---
@st.cache_data
def get_high_demand_niches():
    return {
        "AI & Machine Learning": "AI Engineer OR Machine Learning OR LLM OR NLP",
        "Backend Engineering": "Python OR Go OR Node.js OR Java",
        "Frontend & Fullstack": "React OR Vue OR TypeScript OR Fullstack",
        "Data & Analytics": "Data Engineer OR Data Scientist OR Analytics",
        "Cloud & DevOps": "DevOps OR Site Reliability OR AWS OR Kubernetes",
        "Cybersecurity": "Security Engineer OR Pentester OR SOC"
    }

def score_job_sponsorship(description):
    """The 'Brain' of the app: Analyzes how likely a visa is granted."""
    if not description or not isinstance(description, str): return 0
    desc = description.lower()
    
    score = 0
    # Tier 1: Definite Keywords
    if any(x in desc for x in ["visa sponsorship", "sponsorship provided", "work permit support"]): score += 50
    # Tier 2: Relocation Keywords
    if any(x in desc for x in ["relocation package", "relocation assistance", "moving to", "relocation support"]): score += 30
    # Tier 3: Policy Keywords
    if any(x in desc for x in ["blue card", "international candidates", "visa assistance"]): score += 20
    
    return min(score, 100)

# --- CORE ENGINE ---
@st.cache_data(show_spinner="🕵️ Scanning European Job Markets...", ttl=3600)
def run_intel_engine(niche_query, location, limit):
    # This query format maximizes "Relocation" results
    full_query = f"({niche_query}) AND (sponsorship OR relocation OR 'blue card')"
    
    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=full_query,
            location=location,
            results_wanted=limit,
            hours_old=168, # 1 week old for more variety
            linkedin_fetch_description=True
        )
        if not jobs.empty:
            jobs['sponsorship_score'] = jobs['description'].apply(score_job_sponsorship)
            # Filter out jobs with 0 score to keep quality high
            jobs = jobs[jobs['sponsorship_score'] > 0]
            return jobs.sort_values(by="sponsorship_score", ascending=False)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Search Interrupted: {e}")
        return pd.DataFrame()

# --- UI LAYOUT ---
st.title("🚀 Niche Job Intelligence")
st.subheader("Foreigner-Friendly Tech Leads in Europe")

with st.sidebar:
    st.header("1. Choose Your Niche")
    niche_dict = get_high_demand_niches()
    selected_niche = st.selectbox("Market Segment", list(niche_dict.keys()))
    
    st.header("2. Location")
    loc = st.text_input("Target City/Country", "Europe")
    
    st.header("3. Volume")
    job_count = st.slider("Leads to Fetch", 10, 100, 30)
    
    search_trigger = st.button("Generate Intelligence Report", use_container_width=True)

if search_trigger:
    data = run_intel_engine(niche_dict[selected_niche], loc, job_count)
    
    if not data.empty:
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total High-Intent Leads", len(data))
        with m2:
            high_prob = len(data[data['sponsorship_score'] >= 70])
            st.metric("High Probability (Visa)", high_prob)
        with m3:
            # Simple logic to find big names
            top_tier = ["Google", "Amazon", "Zalando", "Booking.com", "Meta", "Revolut", "Spotify"]
            verified = len(data[data['company'].isin(top_tier)])
            st.metric("Top Tier Employers", verified)

        # Main Data View
        st.divider()
        st.subheader("Verified Leads List")
        
        # Formatting for display
        df_display = data[['sponsorship_score', 'title', 'company', 'location', 'job_url']].copy()
        df_display['sponsorship_score'] = df_display['sponsorship_score'].apply(lambda x: f"{x}% Match")
        
        st.dataframe(df_display, width="stretch", hide_index=True)

        # Download Component
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Lead List (CSV)",
            data=csv,
            file_name=f"{selected_niche}_leads.csv",
            mime='text/csv',
        )

        # AI Email Assistant
        st.divider()
        st.subheader("✉️ Smart Outreach Draft")
        target_job = st.selectbox("Select a lead for email generation:", data['title'] + " @ " + data['company'])
        
        if target_job:
            row = data[data['title'] + " @ " + data['company'] == target_job].iloc[0]
            email_body = f"""Subject: Application for {row['title']} - [Your Name]

Dear Hiring Team at {row['company']},

I am reaching out regarding your {row['title']} opening in {row['location']}. 
I was specifically drawn to your company's openness to international talent. 

My expertise in {selected_niche} aligns with your requirements, and I would value the 
opportunity to contribute to your team. I would require relocation/visa support 
and noticed this is something your company provides.

Best regards,
[Your Name]"""
            st.text_area("Copy and send:", email_body, height=200)

    else:
        st.warning("No high-probability leads found. Try changing your Market Segment or expanding your Location.")

# --- FOOTER ---
st.markdown("---")
st.caption("Intelligence System powered by Python & JobSpy. Focused on EU Work Visa & Blue Card markets.")

# --- SIDEBAR SUPPORT SECTION ---
st.sidebar.markdown("---")
st.sidebar.header("☕ Support the Project")
st.sidebar.write("If this tool helped you find a job lead, consider sending a small token to keep the servers running and the scraper updated!")

# PayPal
st.sidebar.subheader("💳 PayPal")
st.sidebar.write("bensonchepkonga@gmail.com")

# Bitcoin
st.sidebar.subheader("₿ Bitcoin (BTC)")
st.sidebar.code("bc1qgcqn5affp67zxalsyfnrzjl7g6ne0fuspweyh6v93zff5dkmjjaq9jx0cj", language="text")

# USDT (ERC20/BEP20)
st.sidebar.subheader("💵 USDT")
st.sidebar.code("0x8a9b66289f819dccfc7f77b219d5e30747e40da9", language="text")

# Pi Network
st.sidebar.subheader("π Pi Network")
st.sidebar.code("MALYJFJ5SVD45FBWN2GT4IW67SEZ3IBOFSBSPUFCWV427NBNLG3PWAAAAAAAAASUBBWCC", language="text")

st.sidebar.markdown("---")
st.sidebar.caption("Thank you for your support! 🙏")
