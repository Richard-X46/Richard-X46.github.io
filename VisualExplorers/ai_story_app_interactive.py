import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import os

st.set_page_config(layout="wide")

# --- Load Data ---
salary_df = pd.read_csv('Datasets/AVG_salaries_based_on_prof.csv')
enroll_df = pd.read_csv('Datasets/PG_students_enrollment.csv')

st.title('Visual Explorers: The AI Economy Story (Interactive)')
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
    st.image('https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&w=400&h=400&q=80', caption='Jiya Sharma (AI Engineer, Woman)')
    st.markdown('''
    <span style="color:#1f77b4;"><b>Jiya Sharma</b></span><br>
    <i>AI Engineer, GTA (Woman)</i><br>
    "My job is secure, my pay is good, and I keep learning new things. AI is opening doors for me."
    ''', unsafe_allow_html=True)
with col2:
    st.image('https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=facearea&w=400&h=400&q=80', caption='Chris Anderson (Logistics Supervisor, Man)')
    st.markdown('''
    <span style="color:#ff7f0e;"><b>Chris Anderson</b></span><br>
    <i>Logistics Supervisor (Man)</i><br>
    "I see more robots at work, but my pay isn't rising. I'm worried about the future."
    ''', unsafe_allow_html=True)
st.markdown('---')
# --- Monthly Expenses Bar Graph ---
st.header('Monthly Expenses in Toronto/Durham (2025)')
# Example data (replace with real data if available)
expense_data = pd.DataFrame({
    'Category': ['Rent (1BR)', 'Groceries', 'Transit', 'Utilities', 'Internet', 'Leisure', 'Other'],
    'Jiya (AI/Tech)': [2200, 400, 156, 120, 70, 200, 150],
    'Chris (Logistics)': [1800, 400, 156, 120, 70, 100, 100]
})
expense_data = expense_data.set_index('Category')
fig_exp, ax_exp = plt.subplots(figsize=(8,4))
expense_data.plot(kind='bar', ax=ax_exp, color=['#1f77b4', '#ff7f0e'])
ax_exp.set_ylabel('Monthly Cost ($)')
ax_exp.set_title('Estimated Monthly Expenses (Toronto/Durham, 2025)')
ax_exp.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig_exp)
st.caption('Source: [Toronto Cost of Living](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)')
st.markdown('---')

# --- Income Gap Line Graph ---
st.header('Income Gap: Jiya vs. Chris')
ai_mask = salary_df['North American Industry Classification System (NAICS)'].str.contains('Information|Professional|Scientific|Technical', case=False, na=False)
chris_mask = salary_df['North American Industry Classification System (NAICS)'].str.contains('Business|Logistics|Warehousing|Transportation|Trade', case=False, na=False)
ai_group = salary_df[ai_mask].groupby('REF_DATE')['VALUE'].mean()
chris_group = salary_df[chris_mask].groupby('REF_DATE')['VALUE'].mean()
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

# --- Interactive Geo Scatter for Enrollment (Simulated) ---
st.header('Student Enrollment in AI/Tech vs. Business Across Canada')
# More realistic mapping: major universities/cities and their known strengths
geo_data = pd.DataFrame({
    'lat': [43.6629, 45.5048, 49.2606, 53.5232, 45.4215, 51.0447, 46.4746, 48.4634, 43.7735, 43.2609],
    'lon': [-79.3957, -73.5772, -123.2460, -113.5263, -75.6972, -114.0719, -80.5449, -123.3117, -79.3345, -79.9192],
    'enrollment': [3200, 2500, 2100, 1800, 1700, 1600, 1200, 900, 800, 700],
    'course': [
        'AI/Tech', 'AI/Tech', 'AI/Tech', 'AI/Tech', 'Business', 'Business', 'Business', 'Business', 'AI/Tech', 'Business'
    ],
    'city': [
        'Toronto (UofT)', 'Montreal (McGill)', 'Vancouver (UBC)', 'Edmonton (UAlberta)',
        'Ottawa (uOttawa)', 'Calgary (UCalgary)', 'Waterloo (Laurier)', 'Victoria (UVic)',
        'Scarborough (UTSC)', 'Hamilton (McMaster)'
    ]
})
color_map = {'AI/Tech': '#1f77b4', 'Business': '#ff7f0e'}
fig3 = px.scatter_geo(
    geo_data,
    lat='lat', lon='lon',
    color='course',
    size='enrollment',
    hover_name='city',
    projection='natural earth',
    color_discrete_map=color_map,
    title='Student Enrollment in AI/Tech vs. Business by Major University/City',
    size_max=30,
    labels={'course': 'Field'})

fig3.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig3.update_layout(legend_title_text='Field', legend=dict(x=0.85, y=0.95))
st.plotly_chart(fig3, use_container_width=True)
st.caption('Bubble size = number of enrollments. Blue: AI/Tech, Orange: Business. Data mapped to major Canadian universities/cities.')
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
