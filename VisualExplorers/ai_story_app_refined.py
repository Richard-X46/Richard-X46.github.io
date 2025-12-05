import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import os

st.set_page_config(layout="wide")

# --- Load Data ---
salary_df = pd.read_csv('Datasets/AVG_salaries_based_on_prof.csv')
enroll_df = pd.read_csv('Datasets/PG_students_enrollment.csv')

st.title('Visual Explorers: The AI Economy Story (Refined)')
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
    st.image('https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&w=400&h=400&q=80', caption='Jiya Sharma (AI Engineer)')
    st.markdown('''
    <span style="color:#1f77b4;"><b>Jiya Sharma</b></span><br>
    <i>AI Engineer, GTA</i><br>
    "My job is secure, my pay is good, and I keep learning new things. AI is opening doors for me."
    ''', unsafe_allow_html=True)
with col2:
    st.image('https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=facearea&w=400&h=400&q=80', caption='Chris Anderson (Logistics Supervisor)')
    st.markdown('''
    <span style="color:#ff7f0e;"><b>Chris Anderson</b></span><br>
    <i>Logistics Supervisor</i><br>
    "I see more robots at work, but my pay isn't rising. I'm worried about the future."
    ''', unsafe_allow_html=True)
st.markdown('---')

# --- Toronto/Durham Cost of Living Bar Graph ---
st.header('Monthly Expenses in Toronto/Durham (2025)')
# Example data (replace with real data if available)
expense_data = pd.DataFrame({
    'Category': ['Rent (1BR)', 'Groceries', 'Transit', 'Utilities', 'Internet', 'Leisure', 'Other'],
    'Jiya (AI/Tech)': [2200, 400, 156, 120, 70, 200, 150],
    'Chris (Logistics)': [1800, 400, 156, 120, 70, 100, 100]
})
expense_data = expense_data.set_index('Category')
fig, ax = plt.subplots(figsize=(8,4))
expense_data.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_ylabel('Monthly Cost ($)')
ax.set_title('Estimated Monthly Expenses (Toronto/Durham, 2025)')
ax.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig)
st.caption('Source: [Toronto Cost of Living](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)')
st.markdown('---')

# --- Enrollment Geo Scatter (Simulated) ---
st.header('Where Are Students Enrolling?')
# Simulated geo data for illustration (replace with real geo data if available)
geo_data = pd.DataFrame({
    'lat': [43.6532, 43.8971, 43.7764, 43.9445, 43.8390, 43.7001, 43.8000, 43.9000],
    'lon': [-79.3832, -78.8658, -79.2318, -78.8929, -79.0000, -79.4000, -78.9500, -78.8000],
    'enrollment': [1200, 900, 800, 700, 600, 500, 400, 300],
    'stream': ['AI/Tech', 'AI/Tech', 'Business', 'Business', 'AI/Tech', 'Business', 'AI/Tech', 'Business']
})
color_map = {'AI/Tech': '#1f77b4', 'Business': '#ff7f0e'}
fig2, ax2 = plt.subplots(figsize=(8,5))
for stream in geo_data['stream'].unique():
    sub = geo_data[geo_data['stream'] == stream]
    ax2.scatter(sub['lon'], sub['lat'], s=sub['enrollment'], alpha=0.6, label=stream, color=color_map[stream], edgecolor='k')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.set_title('Student Enrollment by Field and Location (Simulated)')
ax2.legend()
st.pyplot(fig2)
st.caption('Bubble size = number of enrollments. Colors: AI/Tech (blue), Business (orange).')
st.markdown('---')

# --- Pull Quotes & Links ---
st.header('What the Experts Say')
st.markdown('''
> "AI is both hurting and helping the next generation of workers."  
<span style="font-size:0.9em;">- [The Globe and Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)</span>

> "The jobs that will fall first as AI takes over the workplace."  
<span style="font-size:0.9em;">- [Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)</span>
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
