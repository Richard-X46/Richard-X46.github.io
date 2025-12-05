import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import os

# --- Load Data ---
salary_df = pd.read_csv('Datasets/AVG_salaries_based_on_prof.csv')
enroll_df = pd.read_csv('Datasets/PG_students_enrollment.csv')
income_xlsx = 'Datasets/2024 Income Scenarios - with Canada Mortgage and Housing Corporation Average Market Rent.xlsx'
if os.path.exists(income_xlsx):
    income_df = pd.read_excel(income_xlsx, engine='openpyxl')
else:
    income_df = None

st.title('Visual Explorers: The AI Economy Story (Advanced)')
st.markdown('''
## Will the AI economy in the GTA/Durham Region create a significant and rapid wealth gap?

<span style="font-size:1.2em;">We follow two young professionals:</span>
- <span style="color:#1f77b4;"><b>Jiya Sharma</b></span>: AI Engineer, secure and growing in the tech sector.
- <span style="color:#ff7f0e;"><b>Chris Anderson</b></span>: Logistics supervisor, facing job insecurity as automation rises.
''', unsafe_allow_html=True)

# --- Infographic Section ---
st.markdown('---')
st.subheader('Infographic: The AI Economy at a Glance')
if os.path.exists('infograph.pdf'):
    try:
        images = convert_from_path('infograph.pdf', dpi=150, first_page=1, last_page=1)
        st.image(images[0], caption='AI Economy Infographic', use_column_width=True)
    except Exception as e:
        st.warning(f'Could not display infographic: {e}')
else:
    st.info('Infographic not found.')
st.markdown('---')

# --- Personas ---
st.header('Meet the Personas')
col1, col2 = st.columns(2)
with col1:
    st.markdown('''
    <span style="color:#1f77b4;"><b>Jiya Sharma</b></span><br>
    <i>AI Engineer, GTA</i><br>
    "My job is secure, my pay is good, and I keep learning new things. AI is opening doors for me."
    ''', unsafe_allow_html=True)
with col2:
    st.markdown('''
    <span style="color:#ff7f0e;"><b>Chris Anderson</b></span><br>
    <i>Logistics Supervisor</i><br>
    "I see more robots at work, but my pay isn't rising. I'm worried about the future."
    ''', unsafe_allow_html=True)
st.markdown('---')

# --- Income Gap Line Graph ---
st.header('Income Gap: Jiya vs. Chris')
st.markdown('''
<span style="color:#1f77b4;"><b>Jiya</b></span>: AI/Tech roles (Information, Professional, Scientific, Technical)<br>
<span style="color:#ff7f0e;"><b>Chris</b></span>: Logistics/Business/Admin roles
''', unsafe_allow_html=True)

# Filter and group for both personas
ai_mask = salary_df['North American Industry Classification System (NAICS)'].str.contains('Information|Professional|Scientific|Technical', case=False, na=False)
chris_mask = salary_df['North American Industry Classification System (NAICS)'].str.contains('Business|Logistics|Warehousing|Transportation|Trade', case=False, na=False)

ai_group = salary_df[ai_mask].groupby('REF_DATE')['VALUE'].mean()
chris_group = salary_df[chris_mask].groupby('REF_DATE')['VALUE'].mean()

# Reduce x-axis density
interval = max(1, len(ai_group)//8)
ai_group = ai_group.iloc[::interval]
chris_group = chris_group.reindex(ai_group.index)

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(ai_group.index, ai_group.values, marker='o', color='#1f77b4', label='Jiya (AI/Tech)')
ax.plot(chris_group.index, chris_group.values, marker='o', color='#ff7f0e', label='Chris (Business/Admin)')
ax.set_ylabel('Average Hourly Wage ($)')
ax.set_xlabel('Date')
ax.set_title('Income Gap Over Time')
ax.legend()
ax.grid(True, alpha=0.2)
ax.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig)
st.caption('Source: [StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.html)')
st.markdown('---')

# --- Education Enrollment Comparison ---
st.header('Upskilling: Education Trends')
st.markdown('''
<span style="color:#1f77b4;"><b>Jiya</b></span>: Mathematics, Computer & Information Sciences<br>
<span style="color:#ff7f0e;"><b>Chris</b></span>: Business, Management & Public Administration
''', unsafe_allow_html=True)

jiya_field = 'Mathematics, computer and information sciences [7]'
chris_field = 'Business, management and public administration [5]'
jiya_enroll = enroll_df[enroll_df['Field of study'] == jiya_field].set_index('REF_DATE')['VALUE']
chris_enroll = enroll_df[enroll_df['Field of study'] == chris_field].set_index('REF_DATE')['VALUE']

fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.plot(jiya_enroll.index, jiya_enroll.values, marker='o', color='#1f77b4', label='Jiya Field (Math/CS)')
ax2.plot(chris_enroll.index, chris_enroll.values, marker='o', color='#ff7f0e', label='Chris Field (Business)')
ax2.set_ylabel('Enrollment')
ax2.set_xlabel('Academic Year')
ax2.set_title('Enrollment Trends by Field')
ax2.legend()
ax2.grid(True, alpha=0.2)
ax2.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig2)
st.caption('Source: [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)')
st.markdown('---')

# --- Income Scenarios Visualization ---
st.header('Income Scenarios: Affordability & Housing')
if income_df is not None:
    cols = income_df.columns
    # Try to find numeric columns for income and rent
    income_col = next((c for c in cols if 'income' in c.lower()), cols[0])
    rent_col = next((c for c in cols if 'rent' in c.lower()), cols[1])
    persona_col = next((c for c in cols if 'persona' in c.lower() or 'scenario' in c.lower()), None)
    # Clean up column names for plotting
    def clean_col(col):
        return col.replace(':', '').replace('"', '').strip()
    income_col_clean = clean_col(income_col)
    rent_col_clean = clean_col(rent_col)
    if income_col != income_col_clean:
        income_df = income_df.rename(columns={income_col: income_col_clean})
    if rent_col != rent_col_clean:
        income_df = income_df.rename(columns={rent_col: rent_col_clean})
    income_col = income_col_clean
    rent_col = rent_col_clean
    if persona_col:
        personas = income_df[persona_col].unique()
        for persona in personas:
            sub = income_df[income_df[persona_col] == persona]
            fig3, ax3 = plt.subplots(figsize=(6,3))
            ax3.bar(sub[income_col], sub[rent_col], color='#1f77b4', alpha=0.7)
            ax3.set_ylabel('Rent ($)')
            ax3.set_xlabel('Income ($)')
            ax3.set_title(f'{persona}: Income vs. Rent')
            ax3.set_ylim(bottom=0)
            st.pyplot(fig3)
            st.caption(f"{persona}: Income vs. Rent")
    else:
        fig3, ax3 = plt.subplots(figsize=(6,3))
        ax3.bar(income_df[income_col], income_df[rent_col], color='#1f77b4', alpha=0.7)
        ax3.set_ylabel('Rent ($)')
        ax3.set_xlabel('Income ($)')
        ax3.set_title('Income vs. Rent (all scenarios)')
        ax3.set_ylim(bottom=0)
        st.pyplot(fig3)
        st.caption("Income vs. Rent (all scenarios)")
    st.caption('Source: Canada Mortgage and Housing Corporation')
else:
    st.info('Income scenario data not found.')
st.markdown('---')

# --- Pull Quotes & Links ---
st.header('What the Experts Say')
st.markdown('''
> "AI is both hurting and helping the next generation of workers."  
<span style="font-size:0.9em;">- [The Globe and Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)</span>

> "The jobs that will fall first as AI takes over the workplace."  
<span style="font-size:0.9em;">- [Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)</span>

> "Is artificial intelligence to blame for Amazon job cuts?"  
<span style="font-size:0.9em;">- [Al Jazeera](https://www.aljazeera.com/news/2025/10/28/is-artificial-intelligence-to-blame-for-amazon-job-cuts)</span>
''', unsafe_allow_html=True)
st.markdown('---')

# --- Conclusion ---
st.header('The Future: A Call to Action')
st.markdown('''
This story shows why learning new skills for AI jobs is more important than ever. Some people move ahead, while others risk being left behind. The future in Durham and the GTA depends on which skills young people have — and those struggling most will find it harder to keep up, unless they get help.

---

**Explore the links and data above. Scroll to see how Jiya and Chris's paths diverge in the AI economy.**

- [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)
- [AI jobs domain - StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.htm)
- [Cost of Living in Toronto](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)
- [The IMF report on AI and jobs](https://stefanbauschard.substack.com/p/the-imf-report-on-ai-and-jobs-is)
- [AI and Jobs: Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)
- [AI and Young Wages: Globe & Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)
''')
