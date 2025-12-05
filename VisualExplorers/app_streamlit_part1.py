import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import os
import altair as alt
import folium
from streamlit_folium import st_folium
import os
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --- Load Data ---
salary_df = pd.read_csv("Datasets/AVG_salaries_based_on_prof.csv")
enroll_df = pd.read_csv("Datasets/PG_students_enrollment.csv")

# st.title("Visual Explorers: The AI Economy Story (Interactive)")
# st.markdown(
#     """
# ## Will the AI economy in the GTA/Durham Region create a significant and rapid wealth gap?

# <span style="font-size:1.2em;">We follow two young professionals:</span>
# - <span style="color:#1f77b4;"><b>Jiya Sharma</b></span>: AI Engineer, secure and growing in the tech sector.
# - <span style="color:#ff7f0e;"><b>Chris Anderson</b></span>: Logistics supervisor, facing job insecurity as automation rises.
# """,
#     unsafe_allow_html=True,
# )

# # --- Infographic Section ---

# st.markdown("---")


# --- Folium Interactive Map ---
if "enroll_df_geo" in locals() or "enroll_df_geo" in globals():
    st.header("Interactive Map: Enrollment by Province (Folium)")
    

    # Center of Canada
    map_center = [56, -96]
    folium_map = folium.Map(location=map_center, zoom_start=4, tiles="cartodbpositron")
    # Color mapping
    stream_colors = {"AI/Tech": "#0057b8", "Business": "#e66101"}
    # Add circle markers for each province and stream
    for _, row in enroll_df_geo.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=max(6, min(row["Enrollment"] / 1000, 25)),
            color=stream_colors.get(row["Stream"], "gray"),
            fill=True,
            fill_color=stream_colors.get(row["Stream"], "gray"),
            fill_opacity=0.8,
            popup=(
                f"<b>Province:</b> {row['Province']}<br>"
                f"<b>City:</b> {row['City']}<br>"
                f"<b>Field:</b> {row['Stream']}<br>"
                f"<b>Enrollment:</b> {int(row['Enrollment']):,}"
            ),
            tooltip=f"{row['Province']} - {row['Stream']}: {int(row['Enrollment']):,}",
        ).add_to(folium_map)
    # Add a legend manually
    from branca.element import MacroElement
    from jinja2 import Template

    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 70px; z-index:9999; font-size:16px; background: white; border:2px solid #ccc; border-radius:8px; padding: 10px;">
    <b>Legend</b><br>
    <span style="color:#0057b8; font-weight:bold;">&#9679;</span> AI/Tech<br>
    <span style="color:#e66101; font-weight:bold;">&#9679;</span> Business
    </div>
    {% endmacro %}
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    folium_map.get_root().add_child(legend)
    st_data = st_folium(folium_map, width=1200, height=600)
    st.caption(
        "Circle size = enrollment. Click or hover for details. Blue: AI/Tech, Orange: Business."
    )
    st.markdown("---")



st.subheader("Infographic: The AI Economy at a Glance")
# if os.path.exists("infograph.pdf"):
#     try:
#         images = convert_from_path("infograph.pdf", dpi=150, first_page=1, last_page=1)
#         st.image(images[0], caption="AI Economy Infographic", use_column_width=True)
#     except Exception as e:
#         st.warning(f"Could not display infographic: {e}")
# else:
#     st.info("Infographic not found.")
# st.markdown("---")

# # --- Personas ---
# st.header("Meet the Personas")
# col1, col2 = st.columns(2)
# with col1:
#     st.image(
#         "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&w=400&h=400&q=80",
#         caption="Jiya Sharma (AI Engineer, Woman)",
#     )
#     st.markdown(
#         """
#     <span style="color:#1f77b4;"><b>Jiya Sharma</b></span><br>
#     <i>AI Engineer, GTA (Woman)</i><br>
#     "My job is secure, my pay is good, and I keep learning new things. AI is opening doors for me."
#     """,
#         unsafe_allow_html=True,
#     )
# with col2:
#     st.image(
#         "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=facearea&w=400&h=400&q=80",
#         caption="Chris Anderson (Logistics Supervisor, Man)",
#     )
#     st.markdown(
#         """
#     <span style="color:#ff7f0e;"><b>Chris Anderson</b></span><br>
#     <i>Logistics Supervisor (Man)</i><br>
#     "I see more robots at work, but my pay isn't rising. I'm worried about the future."
#     """,
#         unsafe_allow_html=True,
#     )
# st.markdown("---")
# --- Monthly Expenses Bar Graph ---
st.header("Monthly Expenses in Toronto/Durham (2025)")
# Example data (replace with real data if available)
expense_data = pd.DataFrame(
    {
        "Category": [
            "Rent (1BR)",
            "Groceries",
            "Transit",
            "Utilities",
            "Internet",
            "Leisure",
            "Other",
        ],
        "Jiya (AI/Tech)": [2200, 400, 156, 120, 70, 200, 150],
        "Chris (Logistics)": [1800, 400, 156, 120, 70, 100, 100],
    }
)
expense_data = expense_data.set_index("Category")
fig_exp, ax_exp = plt.subplots(figsize=(8, 4))
expense_data.plot(kind="bar", ax=ax_exp, color=["#1f77b4", "#ff7f0e"])
ax_exp.set_ylabel("Monthly Cost ($)")
ax_exp.set_title("Estimated Monthly Expenses (Toronto/Durham, 2025)")
ax_exp.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig_exp)
st.caption(
    "Source: [Toronto Cost of Living](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)"
)
st.markdown("---")
# --- Monthly Expenses Bar Graph --- //////////////////////////////////////


# --- Income Gap Line Graph ---
st.header("Income Gap: Jiya vs. Chris")
ai_mask = salary_df[
    "North American Industry Classification System (NAICS)"
].str.contains("Information|Professional|Scientific|Technical", case=False, na=False)
chris_mask = salary_df[
    "North American Industry Classification System (NAICS)"
].str.contains(
    "Business|Logistics|Warehousing|Transportation|Trade", case=False, na=False
)
ai_group = salary_df[ai_mask].groupby("REF_DATE")["VALUE"].mean()
chris_group = salary_df[chris_mask].groupby("REF_DATE")["VALUE"].mean()
interval = max(1, len(ai_group) // 8)
ai_group = ai_group.iloc[::interval]
chris_group = chris_group.reindex(ai_group.index)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(
    ai_group.index, ai_group.values, marker="o", color="#1f77b4", label="Jiya (AI/Tech)"
)
ax.plot(
    chris_group.index,
    chris_group.values,
    marker="o",
    color="#ff7f0e",
    label="Chris (Business/Admin)",
)
ax.set_ylabel("Average Hourly Wage ($)")
ax.set_xlabel("Date")
ax.set_title("Income Gap Over Time")
ax.legend()
ax.grid(True, alpha=0.2)
ax.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig)
st.caption(
    "Source: [StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.html)"
)
st.markdown("---")

# --- Education Enrollment Comparison ---
st.header("Upskilling: Education Trends")
jiya_field = "Mathematics, computer and information sciences [7]"
chris_field = "Business, management and public administration [5]"
jiya_enroll = enroll_df[enroll_df["Field of study"] == jiya_field].set_index(
    "REF_DATE"
)["VALUE"]
chris_enroll = enroll_df[enroll_df["Field of study"] == chris_field].set_index(
    "REF_DATE"
)["VALUE"]
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(
    jiya_enroll.index,
    jiya_enroll.values,
    marker="o",
    color="#1f77b4",
    label="Jiya Field (Math/CS)",
)
ax2.plot(
    chris_enroll.index,
    chris_enroll.values,
    marker="o",
    color="#ff7f0e",
    label="Chris Field (Business)",
)
ax2.set_ylabel("Enrollment")
ax2.set_xlabel("Academic Year")
ax2.set_title("Enrollment Trends by Field")
ax2.legend()
ax2.grid(True, alpha=0.2)
ax2.set_ylim(bottom=0)
plt.xticks(rotation=30)
st.pyplot(fig2)
st.caption(
    "Source: [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)"
)
st.markdown("---")

# --- Interactive Geo Scatter for AI/Tech vs Business Enrollment by Province ---
st.header("AI/Tech vs Business Student Enrollment Across Canada (by Province)")


province_coords = {
    "Ontario": (43.6532, -79.3832, "Toronto"),
    "Quebec": (46.8139, -71.2082, "Quebec City"),
    "British Columbia": (48.4284, -123.3656, "Victoria"),
    "Alberta": (53.5461, -113.4938, "Edmonton"),
    "Manitoba": (49.8951, -97.1384, "Winnipeg"),
    "Saskatchewan": (50.4452, -104.6189, "Regina"),
    "Nova Scotia": (44.6488, -63.5752, "Halifax"),
    "New Brunswick": (45.9636, -66.6431, "Fredericton"),
    "Newfoundland": (47.5615, -52.7126, "St. John's"),
    "Prince Edward Island": (46.2382, -63.1311, "Charlottetown"),
}

enrollment_points = []
folder = "Datasets/PG Enrollment by Province"

# Check if folder exists
if not os.path.exists(folder):
    st.warning(f"⚠️ Folder '{folder}' not found. Skipping enrollment geo map.")
    enroll_df_geo = pd.DataFrame()  # Empty DataFrame
else:
    for prov, (lat, lon, city) in province_coords.items():
        file_path = os.path.join(folder, f"{prov}.csv")
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                for field, stream in [
                    ("Mathematics, computer and information sciences [7]", "AI/Tech"),
                    ("Business, management and public administration [5]", "Business"),
                ]:
                    sub_df = df[df["Field of study"] == field]
                    if not sub_df.empty:
                        latest = sub_df.sort_values("REF_DATE").iloc[-1]
                        enrollment_points.append(
                            {
                                "Province": prov,
                                "City": city,
                                "lat": lat,
                                "lon": lon,
                                "Year": latest["REF_DATE"],
                                "Enrollment": latest["VALUE"],
                                "Stream": stream,
                            }
                        )
            except Exception as e:
                st.warning(f"⚠️ Could not read {file_path}: {e}")

    enroll_df_geo = pd.DataFrame(enrollment_points)

# Only show plots if data exists
if not enroll_df_geo.empty and len(enroll_df_geo) > 0:
    # --- Enhanced Wide Scatter Geo Plot ---
    fig3 = px.scatter_geo(
        enroll_df_geo,
        lat="lat",
        lon="lon",
        size="Enrollment",
        hover_name="City",
        text="Province",
        projection="natural earth",
        title="Latest Enrollment by Province: AI/Tech (blue) vs Business (orange)",
        size_max=60,
        color="Stream",
        color_discrete_map={"AI/Tech": "#0057b8", "Business": "#e66101"},
        scope="north america",
        center={"lat": 56, "lon": -96},
        labels={"Enrollment": "Enrollment"},
    )
    fig3.update_traces(marker=dict(line=dict(width=2, color="black"), opacity=0.85))
    fig3.update_layout(
        geo=dict(
            lataxis_range=[40, 70],
            lonaxis_range=[-140, -50],
            projection_scale=2.5,
            center={"lat": 56, "lon": -96},
            showland=True,
            landcolor="rgb(243, 243, 243)",
        ),
        width=1200,
        height=700,
        legend_title_text="Field",
        font=dict(size=16),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig3, use_container_width=False)
    st.caption(
        "Bubble size = number of enrollments. Blue: AI/Tech, Orange: Business. Data: StatCan, latest available year per province."
    )
    st.markdown("---")

    # --- Grouped Bar Chart for Enrollment by Province ---
    st.header("Enrollment Comparison by Province")
    import plotly.graph_objects as go

    bar_data = (
        enroll_df_geo.pivot(index="Province", columns="Stream", values="Enrollment")
        .fillna(0)
        .astype(int)
    )
    bar_data = bar_data.loc[province_coords.keys()]  # keep order
    fig_bar = go.Figure()
    fig_bar.add_trace(
        go.Bar(
            x=bar_data.index,
            y=bar_data["AI/Tech"],
            name="AI/Tech",
            marker_color="#0057b8",
            text=bar_data["AI/Tech"],
            textposition="outside",
        )
    )
    fig_bar.add_trace(
        go.Bar(
            x=bar_data.index,
            y=bar_data["Business"],
            name="Business",
            marker_color="#e66101",
            text=bar_data["Business"],
            textposition="outside",
        )
    )
    fig_bar.update_layout(
        barmode="group",
        title="Latest Enrollment: AI/Tech vs Business by Province",
        xaxis_title="Province",
        yaxis_title="Enrollment",
        width=1200,
        height=600,
        font=dict(size=16),
        legend_title_text="Field",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig_bar.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_bar, use_container_width=False)
    st.caption("Side-by-side comparison of AI/Tech and Business enrollment by province.")
else:
    st.warning("⚠️ No enrollment data found. Check if the 'Datasets/PG Enrollment by Province' folder contains CSV files for each province.")

st.markdown("---")

# --- Pull Quotes & Links ---
st.header("What the Experts Say")
st.markdown(
    """
> "AI is both hurting and helping the next generation of workers."  
<span style="font-size:0.9em;">- [The Globe and Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)</span>

> "The jobs that will fall first as AI takes over the workplace."  
<span style="font-size:0.9em;">- [Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)</span>
""",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Conclusion ---
st.header("The Future: A Call to Action")
st.markdown("""
This story shows why learning new skills for AI jobs is more important than ever. Some people move ahead, while others risk being left behind. The future in Durham and the GTA depends on which skills young people have — and those struggling most will find it harder to keep up, unless they get help.

---

**Explore the links and data above. Scroll to see how Jiya and Chris's paths diverge in the AI economy.**

- [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)
- [AI jobs domain - StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.htm)
- [Cost of Living in Toronto](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)
- [The IMF report on AI and jobs](https://stefanbauschard.substack.com/p/the-imf-report-on-ai-and-jobs-is)
- [AI and Jobs: Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)
- [AI and Young Wages: Globe & Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)
""")


# --- 1. Configuration & Data Models ---
st.set_page_config(layout="wide", page_title="AI Wealth Gap Simulator (10-Year)")

# Custom CSS for "Cinematic" Dark Mode feel
st.markdown(
    """
<style>
    .stApp { background-color: #0f172a; color: white; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stProgress > div > div > div > div { background-color: #4f46e5; }
    h1, h2, h3 { color: #e2e8f0; }
    .highlight-green { color: #34d399; font-weight: bold; }
    .highlight-red { color: #f87171; font-weight: bold; }
</style>
""",
    unsafe_allow_html=True,
)

REGIONAL_CONFIG = {
    "RENT_START_MONTHLY": 2650,
    "RENT_INFLATION": 0.03,  # 3% annual rent inflation
    "LIVING_EXPENSES_BASE": 2000,
    "EXPENSE_INFLATION": 0.025,
    "TAX_RATE_HIGH": 0.28,
    "TAX_RATE_LOW": 0.22,
}

PERSONAS = {
    "jiya": {
        "name": "Jiya",
        "role": "Junior AI Engineer",
        "start_salary": 88000,
        "growth_rate": 0.12,  # 12% High Leverage
        "color": "#10b981",
        "icon": "🚀",
    },
    "chris": {
        "name": "Chris",
        "role": "Logistics Coordinator",
        "start_salary": 52000,
        "growth_rate": 0.02,  # 2% Stagnation
        "upskill_rate": 0.10,  # 10% Growth if upskilled
        "color": "#f43f5e",
        "icon": "🛑",
    },
}

# --- 2. Logic & Calculations ---


def calculate_10_year_forecast(is_upskilled):
    """Generates a 10-year financial dataframe for both personas."""
    data = []

    # Jiya State
    j_salary = PERSONAS["jiya"]["start_salary"]
    j_wealth = 0

    # Chris State
    c_salary = PERSONAS["chris"]["start_salary"]
    c_wealth = 0

    rent = REGIONAL_CONFIG["RENT_START_MONTHLY"] * 12
    expenses = REGIONAL_CONFIG["LIVING_EXPENSES_BASE"] * 12

    for year in range(11):  # Year 0 to 10
        # 1. Calculate Net Worth / Savings for this year
        # Taxes
        j_tax = (
            REGIONAL_CONFIG["TAX_RATE_HIGH"]
            if j_salary > 100000
            else REGIONAL_CONFIG["TAX_RATE_LOW"]
        )
        c_tax = (
            REGIONAL_CONFIG["TAX_RATE_HIGH"]
            if c_salary > 100000
            else REGIONAL_CONFIG["TAX_RATE_LOW"]
        )

        j_net = j_salary * (1 - j_tax)
        c_net = c_salary * (1 - c_tax)

        # Disposable
        j_save = max(0, j_net - rent - expenses)
        c_save = max(0, c_net - rent - expenses)

        j_wealth += j_save
        c_wealth += c_save

        # 2. Append Data
        data.append(
            {
                "Year": year + 2025,
                "Timeline": f"Year {year}",
                "Jiya Income": round(j_salary),
                "Jiya Wealth": round(j_wealth),
                "Chris Income": round(c_salary),
                "Chris Wealth": round(c_wealth),
                "Gap": round(j_salary - c_salary),
                "Rent Annual": round(rent),
            }
        )

        # 3. Inflate for next year
        j_salary *= 1 + PERSONAS["jiya"]["growth_rate"]

        # Chris growth depends on upskilling
        c_rate = PERSONAS["chris"]["growth_rate"]
        if is_upskilled and year >= 1:
            c_rate = PERSONAS["chris"]["upskill_rate"]
        c_salary *= 1 + c_rate

        rent *= 1 + REGIONAL_CONFIG["RENT_INFLATION"]
        expenses *= 1 + REGIONAL_CONFIG["EXPENSE_INFLATION"]

    return pd.DataFrame(data)


# --- 3. Streamlit UI Layout ---

# HEADER
col1, col2 = st.columns([3, 1])
with col1:
    st.title("AI Wealth Gap Simulator 🇨🇦")
    st.markdown("### 10-Year Forecast: High-Leverage vs. Low-Leverage Careers")
    st.caption(
        f"Region: GTA/Durham | Baseline Rent: ${REGIONAL_CONFIG['RENT_START_MONTHLY']}/mo"
    )

with col2:
    # Upskill Toggle
    is_upskilled = st.checkbox(
        "🎓 Upskill Chris?",
        value=False,
        help="Apply AI certification to Chris's career path to see the impact.",
    )

# RUN SIMULATION
df = calculate_10_year_forecast(is_upskilled)

# KEY METRICS (YEAR 10 SNAPSHOT)
y10_data = df.iloc[10]
y10_gap = y10_data["Gap"]
y10_wealth_gap = y10_data["Jiya Wealth"] - y10_data["Chris Wealth"]

m1, m2, m3 = st.columns(3)
m1.metric(
    label="Year 10 Income Gap", value=f"${y10_gap:,.0f}", delta="Annual Difference"
)
m2.metric(
    label="Cumulative Wealth Gap",
    value=f"${y10_wealth_gap:,.0f}",
    delta="Asset Difference",
    delta_color="inverse",
)
m3.metric(
    label="Chris Rent Burden (Y10)",
    value=f"{(y10_data['Rent Annual'] / y10_data['Chris Income'] * 100):.1f}%",
    delta="of Gross Income",
    delta_color="inverse",
)

st.divider()

# CHARTS ROW
c1, c2 = st.columns([2, 1])

with c1:

    st.subheader("📈 10-Year Income Trajectory")

    # Transform data for Altair (Long format)
    chart_data = df.melt(
        "Year",
        value_vars=["Jiya Income", "Chris Income"],
        var_name="Persona",
        value_name="Income",
    )

    # Create Area/Line Chart
    chart = (
        alt.Chart(chart_data)
        .mark_line(strokeWidth=4)
        .encode(
            x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Income:Q", axis=alt.Axis(format="$,.0f")),
            color=alt.Color(
                "Persona",
                scale=alt.Scale(
                    domain=["Jiya Income", "Chris Income"],
                    range=["#10b981", "#f43f5e" if not is_upskilled else "#3b82f6"],
                ),
            ),
            tooltip=["Year", "Persona", "Income"],
        )
        .properties(height=350)
    )

    # Add Area
    area = chart.mark_area(opacity=0.3)
    st.altair_chart(area + chart, use_container_width=True)

with c2:
    st.subheader("💰 Net Worth Accumulation")
    st.markdown("Projected assets after rent & living expenses.")

    wealth_data = df[["Year", "Jiya Wealth", "Chris Wealth"]]
    st.bar_chart(
        wealth_data.set_index("Year"),
        color=["#10b981", "#f43f5e" if not is_upskilled else "#3b82f6"],
    )

# DATA TABLE (Future Outlook)
st.subheader("📅 Future Outlook Table")
display_cols = [
    "Timeline",
    "Jiya Income",
    "Chris Income",
    "Gap",
    "Jiya Wealth",
    "Chris Wealth",
]
st.dataframe(
    df[display_cols].style.format(
        {
            "Jiya Income": "${:,.0f}",
            "Chris Income": "${:,.0f}",
            "Gap": "${:,.0f}",
            "Jiya Wealth": "${:,.0f}",
            "Chris Wealth": "${:,.0f}",
        }
    ),
    use_container_width=True,
)

# FOOTER
st.info(
    "Data Sources: Salaries based on 2024 StatCan/Glassdoor proxies for 'Junior AI Engineer' vs 'Logistics Coordinator'. Rent based on Rentals.ca GTA averages."
)
