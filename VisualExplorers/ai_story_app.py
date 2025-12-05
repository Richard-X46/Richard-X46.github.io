import streamlit as st
import pandas as pd

# --- Load Data ---
salary_df = pd.read_csv('Datasets/AVG_salaries_based_on_prof.csv')
enroll_df = pd.read_csv('Datasets/PG_students_enrollment.csv')

# --- Story Introduction ---
st.title('Visual Explorers: The AI Economy Story')
st.markdown('''
## Will the AI economy in the GTA/Durham Region create a significant and rapid wealth gap?

We follow two young professionals:
- **Jiya Sharma**: AI Engineer, secure and growing in the tech sector.
- **Chris Anderson**: Logistics supervisor, facing job insecurity as automation rises.

---
''')

# --- Jiya's Story ---
st.header('Jiya: Riding the AI Wave')
st.markdown('''
Jiya uses her data science skills and works with AI every day. Her job is safe, her pay is good, and her company keeps offering new ways to learn and grow. Jiya feels she can plan her future and is excited about new opportunities that digital jobs provide.

[AI jobs domain - StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.htm)
''')

# --- Salary Trends (AI-complementary) ---
st.subheader('Salary Trends: AI-Complementary Roles')
ai_roles = salary_df[salary_df['North American Industry Classification System (NAICS)'].str.contains('Information|Professional|Scientific|Technical', case=False, na=False)]
st.line_chart(ai_roles.groupby('REF_DATE')['VALUE'].mean())

# --- Chris's Story ---
st.header('Chris: Facing Automation')
st.markdown('''
Chris works as a supervisor at a logistics company. His job does not use much AI, and he sees computers and robots doing more of the work around him. His pay doesn’t go up, and he’s worried about losing his job. It’s getting harder for Chris to pay for rent and save money. He feels stuck and wishes there were affordable programs that could help him learn new, useful skills.

[Cost of Living in Toronto](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)
''')

# --- Salary Trends (Non-AI) ---
st.subheader('Salary Trends: Non-AI Roles')
non_ai_roles = salary_df[~salary_df['North American Industry Classification System (NAICS)'].str.contains('Information|Professional|Scientific|Technical', case=False, na=False)]
st.line_chart(non_ai_roles.groupby('REF_DATE')['VALUE'].mean())

# --- Enrollment Trends ---
st.header('Upskilling: Who is Preparing for the Future?')
st.markdown('''
Both Jiya and Chris want to adapt. Jiya looks for advanced training to keep her edge as AI spreads. Chris looks for simple, low-cost classes and certificates that might help him switch to a better job before the gap between those with and without AI skills grows even wider.
''')

fields = ['Business, management and public administration [5]', 'Physical and life sciences and technologies [6]']
for field in fields:
    field_data = enroll_df[enroll_df['Field of study'] == field]
    st.line_chart(field_data.set_index('REF_DATE')['VALUE'], height=200)
    st.caption(f"Enrollment in {field}")

# --- Conclusion ---
st.header('The Future: A Call to Action')
st.markdown('''
This story shows why learning new skills for AI jobs is more important than ever. Some people move ahead, while others risk being left behind. The future in Durham and the GTA depends on which skills young people have — and those struggling most will find it harder to keep up, unless they get help.

---

**Explore the links and data above. Scroll to see how Jiya and Chris's paths diverge in the AI economy.**

- [AI and Jobs: Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)
- [AI and Young Wages: Globe & Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)
''')
