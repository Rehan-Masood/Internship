import re
import sqlite3
import time
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="ScrapePulse — Web Scraping & Tech Market Intelligence",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; }
    .stButton>button { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: #000; font-weight: bold; border: none; border-radius: 6px; }
    </style>
""",
    unsafe_allow_html=True,
)

DB_FILE = "scrapepulse.db"


def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            tech_stack TEXT,
            source TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(title, company)
        )
    """)
  conn.commit()
  conn.close()


init_db()


# --- SCRAPING ENGINE ---
class JobScraperEngine:

  def __init__(self):
    self.headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    self.tech_keywords = [
        "Python",
        "React",
        "Node.js",
        "SQL",
        "Docker",
        "AWS",
        "FastAPI",
        "Flask",
        "Django",
        "TypeScript",
        "PostgreSQL",
        "MongoDB",
    ]

  def extract_skills(self, text):
    found_skills = []
    for tech in self.tech_keywords:
      pattern = r"\b" + re.escape(tech) + r"\b"
      if re.search(pattern, text, re.IGNORECASE):
        found_skills.append(tech)
    return ", ".join(found_skills) if found_skills else "General / Unspecified"

  def scrape_jobs_remoteok(self):
    url = "https://remoteok.com/remote-dev-jobs"
    scraped_data = []

    try:
      response = requests.get(url, headers=self.headers, timeout=10)
      if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr", class_="job")

        for row in rows[:15]:  # Process top 15 jobs
          title_elem = row.find("h2", itemprop="title")
          company_elem = row.find("h3", itemprop="name")
          location_elem = row.find("div", class_="location")

          title = title_elem.text.strip() if title_elem else "Software Engineer"
          company = company_elem.text.strip() if company_elem else "Tech Firm"
          location = (
              location_elem.text.strip() if location_elem else "Remote"
          )

          # Extract text for skills
          row_text = row.get_text()
          skills = self.extract_skills(row_text)

          scraped_data.append({
              "title": title,
              "company": company,
              "location": location,
              "tech_stack": skills,
              "source": "RemoteOK",
          })
      return scraped_data
    except Exception as e:
      st.error(f"Scraping Error: {e}")
      return []


# --- MAIN APPLICATION DASHBOARD ---
st.sidebar.title("🕷️ ScrapePulse.Studio")
st.sidebar.caption("Web Scraping & Tech Stack Intelligence Engine")

st.title("⚡ Tech Stack Intelligence & Web Scraping Engine")
st.write(
    "Extract live tech jobs, profile demanded software stacks, and store"
    " unstructured HTML into SQLite."
)

col_actions, col_space = st.columns([1, 2])
with col_actions:
  if st.button("🚀 Trigger Live Web Scraping Engine"):
    with st.spinner("Connecting to live job boards & parsing HTML..."):
      engine = JobScraperEngine()
      results = engine.scrape_jobs_remoteok()

      if results:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        saved_count = 0
        for item in results:
          try:
            cursor.execute(
                """
                            INSERT INTO job_postings (title, company, location, tech_stack, source)
                            VALUES (?, ?, ?, ?, ?)
                        """,
                (
                    item["title"],
                    item["company"],
                    item["location"],
                    item["tech_stack"],
                    item["source"],
                ),
            )
            saved_count += 1
          except sqlite3.IntegrityError:
            pass  # Avoid duplicate entries
        conn.commit()
        conn.close()

        st.success(
            f"Successfully scraped {len(results)} jobs ({saved_count} new"
            " records stored in SQLite)!"
        )

# --- ANALYTICS & METRICS SECTION ---
conn = sqlite3.connect(DB_FILE)
df_jobs = pd.read_sql_query(
    "SELECT * FROM job_postings ORDER BY id DESC", conn
)
conn.close()

if not df_jobs.empty:
  st.markdown("---")

  # Metric Cards
  c1, c2, c3 = st.columns(3)
  c1.metric("Total Scraped Jobs", len(df_jobs))
  c2.metric("Unique Companies", df_jobs["company"].nunique())

  # Top Tech Stack Frequency Analysis
  all_skills = []
  for skills_str in df_jobs["tech_stack"].dropna():
    for skill in skills_str.split(", "):
      if skill != "General / Unspecified":
        all_skills.append(skill)

  top_skill = (
      pd.Series(all_skills).mode()[0] if all_skills else "Python / SQL"
  )
  c3.metric("Most Demanded Skill", top_skill)

  st.markdown("---")

  col_left, col_right = st.columns(2)

  with col_left:
    st.subheader("📊 Most In-Demand Tech Stacks")
    if all_skills:
      skill_counts = pd.Series(all_skills).value_counts().reset_index()
      skill_counts.columns = ["Technology", "Demand Count"]

      fig_skills = px.bar(
          skill_counts,
          x="Technology",
          y="Demand Count",
          color="Demand Count",
          color_continuous_scale="Viridis",
          title="Frequency of Required Skills in Scraped Jobs",
      )
      st.plotly_chart(fig_skills, use_container_width=True)
    else:
      st.info("Trigger a live scrape to analyze tech stack demands.")

  with col_right:
    st.subheader("📋 Scraped Dataset Audit Trail")
    st.dataframe(
        df_jobs[["title", "company", "location", "tech_stack", "scraped_at"]],
        use_container_width=True,
    )
else:
  st.info("No data in SQLite database. Click the button above to start scraping!")