import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import os
import base64
import streamlit.components.v1 as components
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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")

# Set white background
# st.markdown(
#     """
#     <style>
#         .stApp {
#             background-color: black;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# --- Load Data ---
salary_df = pd.read_csv("Datasets/AVG_salaries_based_on_prof.csv")
enroll_df = pd.read_csv("Datasets/PG_students_enrollment.csv")

st.title("Visual Explorers - The AI Economy Story")

# --- AI Divide PDFs directly under title ---
ai_divide_pdfs = [
    "The AI Divide in GTA-1.pdf",
    "The AI Divide in GTA-2.pdf",
]

for pdf_path in ai_divide_pdfs:
    if os.path.exists(pdf_path):
        try:
            pages = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=1)
            st.image(
                pages[0],
                # caption=f"AI Divide: {os.path.basename(pdf_path)}",
                # use_column_width=True,
            )
        except Exception as e:
            st.warning(f"Could not render {pdf_path}: {e}")
    else:
        st.info(f"File not found: {pdf_path}")




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
### Bar graph

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
    # st.plotly_chart(fig3, use_container_width=False)
    # st.caption(
    #     "Bubble size = number of enrollments. Blue: AI/Tech, Orange: Business. Data: StatCan, latest available year per province."
    # )
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
    st.caption(
        "Side-by-side comparison of AI/Tech and Business enrollment by province."
    )
else:
    st.warning(
        "⚠️ No enrollment data found. Check if the 'Datasets/PG Enrollment by Province' folder contains CSV files for each province."
    )

st.markdown("---")


##### foliunm mapp
st.header("Interactive Map: AI/Tech vs Business Enrollment by Province (Folium)")

if not enroll_df_geo.empty and len(enroll_df_geo) > 0:
    map_center = [56, -96]
    folium_map = folium.Map(location=map_center, zoom_start=4, tiles="OpenStreetMap")

    stream_colors = {"AI/Tech": "#0057b8", "Business": "#e66101"}

    # Diagonal offset: AI/Tech northeast, Business southwest
    offset_dict = {
        "AI/Tech": (0.18, 0.18),  # lat, lon offset for AI/Tech
        "Business": (-0.18, -0.18),  # lat, lon offset for Business
    }

    for _, row in enroll_df_geo.iterrows():
        lat_offset, lon_offset = offset_dict.get(row["Stream"], (0, 0))
        folium.CircleMarker(
            location=[row["lat"] + lat_offset, row["lon"] + lon_offset],
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

    # Legend (dark background)
    from branca.element import MacroElement
    from jinja2 import Template

    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="position: fixed; bottom: 50px; left: 50px; width: 240px; height: 80px; z-index:9999; font-size:16px; background: #222; border:2px solid #0057b8; border-radius:8px; padding: 12px;">
    <b style="color:white;">Legend</b><br>
    <span style="color:#0057b8; font-weight:bold;">&#9679;</span> <span style="color:white;">AI/Tech (northeast offset)</span><br>
    <span style="color:#e66101; font-weight:bold;">&#9679;</span> <span style="color:white;">Business (southwest offset)</span>
    </div>
    {% endmacro %}
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    folium_map.get_root().add_child(legend)

    st_data = st_folium(folium_map, width=1200, height=700)
    st.caption(
        "Circle size = enrollment. Blue: AI/Tech (northeast offset), Orange: Business (southwest offset). Click or hover for details."
    )
    st.markdown("---")
else:
    st.warning(
        "⚠️ No enrollment data found. Check if the 'Datasets/PG Enrollment by Province' folder contains CSV files for each province."
    )


##### --------- enrollment by province section end


st.markdown(
    """
### We follow two young professionals

<span style="font-size:1.2em;"></span>
- <span style="color:#1f77b4;"><b>Jiya Sharma</b></span>: AI Engineer, secure and growing in the tech sector.
- <span style="color:#ff7f0e;"><b>Chris Anderson</b></span>: Logistics supervisor, facing job insecurity as automation rises.
""",
    unsafe_allow_html=True,
)


# --- Personas ---
st.header("Meet the Personas")
col1, col2 = st.columns(2)
with col1:
    st.image(
        "jiya.jpg",
        caption="Jiya Sharma (AI Engineer, Woman)",
    )
    st.markdown(
        """
    <span style="color:#1f77b4;"><b>Jiya Sharma</b></span><br>
    <i>AI Engineer, GTA (Woman)</i><br>
    "My job is secure, my pay is good, and I keep learning new things. AI is opening doors for me."
    """,
        unsafe_allow_html=True,
    )
with col2:
    st.image(
        "chris.jpg",
        caption="Chris Anderson (Logistics Supervisor, Man)",
    )
    st.markdown(
        """
    <span style="color:#ff7f0e;"><b>Chris Anderson</b></span><br>
    <i>Logistics Supervisor (Man)</i><br>
    "I see more robots at work, but my pay isn't rising. I'm worried about the future."
    """,
        unsafe_allow_html=True,
    )
st.markdown("---")




# --- AI Divide PDF for Slide 6 ---
pdf_path = "The AI Divide in GTA-7.pdf"
if os.path.exists(pdf_path):
    try:
        pages = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)
        st.image(pages[0],
        #  caption="AI Divide: daily reality for Jiya vs Chris",
          use_container_width=True)
    except Exception as e:
        st.warning(f"Could not render {pdf_path}: {e}")
else:
    st.info(f"File not found: {pdf_path}")


### Graphs for the right pane of the scrolly section


# Graph 1: Average Salaries Over Time


file = "Datasets/AVG_salaries_based_on_prof.csv"
df = pd.read_csv(file)

# Convert REF_DATE to datetime
df["REF_DATE"] = pd.to_datetime(df["REF_DATE"], format="%Y-%m")
df["REF_DATE_STR"] = df["REF_DATE"].dt.strftime("%Y-%m")

# filter for specific industries if needed
industries_of_interest = ["Transportation and warehousing [48-49]","Professional, scientific and technical services [54,541]"]
df = df[df["North American Industry Classification System (NAICS)"].isin(industries_of_interest)]

# Sort by date for proper animation
df = df.sort_values("REF_DATE")

# Create cumulative data for each frame
frames_data = []
for date in df["REF_DATE_STR"].unique():
    frame_df = df[df["REF_DATE_STR"] <= date].copy()
    frame_df["frame"] = date
    frames_data.append(frame_df)

df_animated = pd.concat(frames_data, ignore_index=True)

# Animated line plot with cumulative data
fig = px.line(
    df_animated,
    x="REF_DATE",
    y="VALUE",
    color="North American Industry Classification System (NAICS)",
    animation_frame="frame",
    markers=True,
    title="Tech vs Logistics: Wage Gap Over Time",
    labels={
        "VALUE": "Average Hourly Wage (CAD)",
        "REF_DATE": "Date",
        "North American Industry Classification System (NAICS)": "Industry"
    },
    range_y=[df["VALUE"].min() * 0.95, df["VALUE"].max() * 1.05],
    color_discrete_map={
        "Professional, scientific and technical services [54,541]": "#1f77b4",  # Blue for Jiya
        "Transportation and warehousing [48-49]": "#ff7f0e"  # Orange for Chris
    }
)

fig.update_layout(
    height=400, 
    width=600, 
    showlegend=False,
    xaxis_range=[df["REF_DATE"].min(), df["REF_DATE"].max()],
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(color='#262730'),
    # Control animation speed here
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 100, "redraw": True},
                                "fromcurrent": True, 
                                "transition": {"duration": 50}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }]
)

# Set default animation speed
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 50

# Convert to HTML for embedding in scrolly
chart_html = fig.to_html(include_plotlyjs='cdn', div_id="wage-chart", config={'displayModeBar': False})



# graph 2: Education Enrollment Trends

# Create enrollment chart for board 3 (Plotly)
jiya_field = 'Mathematics, computer and information sciences [7]'
chris_field = 'Business, management and public administration [5]'
jiya_enroll = enroll_df[enroll_df['Field of study'] == jiya_field].copy()
chris_enroll = enroll_df[enroll_df['Field of study'] == chris_field].copy()

# Create Plotly figure
fig_enroll = px.line(
    title="Education Enrollment Trends: Tech vs Business",
    labels={"value": "Enrollment", "REF_DATE": "Academic Year"}
)

# Add traces manually for better control
fig_enroll.add_scatter(
    x=jiya_enroll['REF_DATE'], 
    y=jiya_enroll['VALUE'],
    mode='lines+markers',
    name='Math/CS (Jiya)',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=6)
)

fig_enroll.add_scatter(
    x=chris_enroll['REF_DATE'], 
    y=chris_enroll['VALUE'],
    mode='lines+markers',
    name='Business (Chris)',
    line=dict(color='#ff7f0e', width=2),
    marker=dict(size=6)
)

fig_enroll.update_layout(
    height=400,
    width=600,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(color='#262730'),
    xaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
    yaxis=dict(showgrid=True, gridcolor='#e0e0e0', rangemode='tozero')
)

enroll_chart_html = fig_enroll.to_html(include_plotlyjs='cdn', div_id="enroll-chart", config={'displayModeBar': False})



# Graph 3: AI complementary and exposure effects 
import plotly.graph_objects as go

# Jiya and Chris AI exposure data points
personas_aioe = {
    'Jiya (AI Engineer)': {
        'category': 'Computer and information systems professionals',
        'aioe': 6.5877,
        'complementarity': 0.5513,
        'color': '#1f77b4'
    },
    'Chris (Logistics Supervisor)': {
        'category': 'Sales and service supervisors',
        'aioe': 6.0866,
        'complementarity': 0.604,
        'color': '#ff7f0e'
    }
}

# Calculate median values for quadrant lines
median_aioe = 6.0758
median_comp = 0.5953

# Create figure with flipped axes (AIOE on x, complementarity on y)
fig_aioe = go.Figure()

# Add quadrant background rectangles (flipped)
fig_aioe.add_shape(type="rect", x0=5.0, y0=median_comp, x1=median_aioe, y1=0.75,
              fillcolor="rgba(200,255,200,0.2)", line_width=0, layer="below")
fig_aioe.add_shape(type="rect", x0=median_aioe, y0=median_comp, x1=7.0, y1=0.75,
              fillcolor="rgba(255,255,200,0.2)", line_width=0, layer="below")
fig_aioe.add_shape(type="rect", x0=5.0, y0=0.5, x1=median_aioe, y1=median_comp,
              fillcolor="rgba(230,230,230,0.2)", line_width=0, layer="below")
fig_aioe.add_shape(type="rect", x0=median_aioe, y0=0.5, x1=7.0, y1=median_comp,
              fillcolor="rgba(255,200,200,0.2)", line_width=0, layer="below")

# Add quadrant dividing lines
fig_aioe.add_vline(x=median_aioe, line_dash="dash", line_color="gray", opacity=0.5)
fig_aioe.add_hline(y=median_comp, line_dash="dash", line_color="gray", opacity=0.5)

# Add persona data points
for name, data in personas_aioe.items():
    fig_aioe.add_trace(go.Scatter(
        x=[data['aioe']],
        y=[data['complementarity']],
        mode='markers+text',
        name=name,
        marker=dict(size=20, color=data['color'], line=dict(width=2, color='white')),
        text=[name.split('(')[0].strip()],
        textposition="top center",
        textfont=dict(size=12, color=data['color'], family='Inter'),
        hovertemplate=f"<b>{name}</b><br>" +
                      f"Category: {data['category']}<br>" +
                      f"AI Exposure: {data['aioe']:.2f}<br>" +
                      f"Complementarity: {data['complementarity']:.2f}<br>" +
                      "<extra></extra>"
    ))

# Add quadrant labels
fig_aioe.add_annotation(x=5.5, y=0.68, text="Low Risk<br>(Stable)", 
                   showarrow=False, font=dict(size=9, color="green"), opacity=0.6)
fig_aioe.add_annotation(x=6.6, y=0.68, text="Opportunity<br>(AI Enhances)", 
                   showarrow=False, font=dict(size=9, color="#228B22"), opacity=0.6)
fig_aioe.add_annotation(x=5.5, y=0.54, text="Less Affected", 
                   showarrow=False, font=dict(size=9, color="gray"), opacity=0.6)
fig_aioe.add_annotation(x=6.6, y=0.54, text="High Risk<br>(AI Replaces)", 
                   showarrow=False, font=dict(size=9, color="red"), opacity=0.6)

# Update layout
fig_aioe.update_layout(
    title="AI Impact: Complementarity vs Exposure",
    xaxis_title="AI Occupational Exposure (AIOE)",
    yaxis_title="Complementarity Index",
    xaxis=dict(range=[5.0, 7.0], showgrid=True, gridcolor='lightgray'),
    yaxis=dict(range=[0.5, 0.75], showgrid=True, gridcolor='lightgray'),
    height=400,
    width=600,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Inter, sans-serif', color='#262730'),
    showlegend=False
)

aioe_chart_html = fig_aioe.to_html(include_plotlyjs='cdn', div_id="aioe-chart", config={'displayModeBar': False})



# Graph 4: Training Pathways and ROI for Board 5
# Create realistic training cost and salary data

training_options = pd.DataFrame({
    'Option': ['Online Courses\n(Coursera/edX)', 'Community College\nCertificate', 'Employer\nSponsored', 'Government\nSubsidized'],
    'Cost': [300, 3500, 0, 500],
    'Duration_months': [3, 6, 4, 5]
})

# Salary progression data (conservative estimates)
years = [0, 1, 2, 3, 5]
salary_without_training = [58000, 59500, 61000, 62500, 65000]  # Modest growth
salary_with_training = [58000, 64000, 69000, 73000, 78000]  # 15-20% boost after training

salary_df_training = pd.DataFrame({
    'Year': years,
    'Without AI Training': salary_without_training,
    'With AI Training': salary_with_training
})

# Create combined figure with subplots

fig_training = make_subplots(
    rows=2, cols=1,
    row_heights=[0.4, 0.6],
    subplot_titles=('Accessible Training Options', 'Career Impact: 5-Year Salary Projection'),
    vertical_spacing=0.15
)

# Top chart: Training costs
fig_training.add_trace(
    go.Bar(
        x=training_options['Option'],
        y=training_options['Cost'],
        marker=dict(
            color=['#ff7f0e', '#ff9f4a', '#4CAF50', '#81C784'],
            line=dict(color='white', width=2)
        ),
        text=['$' + str(int(c)) for c in training_options['Cost']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Cost: $%{y:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=1, col=1
)

# Bottom chart: Salary progression
fig_training.add_trace(
    go.Scatter(
        x=salary_df_training['Year'],
        y=salary_df_training['Without AI Training'],
        mode='lines+markers',
        name='Without AI Training',
        line=dict(color='#cccccc', width=3, dash='dash'),
        marker=dict(size=8, color='#999999'),
    ),
    row=2, col=1
)

fig_training.add_trace(
    go.Scatter(
        x=salary_df_training['Year'],
        y=salary_df_training['With AI Training'],
        mode='lines+markers',
        name='With AI Training',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=10, color='#ff7f0e', line=dict(width=2, color='white')),
    ),
    row=2, col=1
)

# Add ROI annotation
fig_training.add_annotation(
    x=5, y=78000,
    text=f"<b>+${78000-65000:,}</b><br>over 5 years",
    showarrow=True,
    arrowhead=2,
    arrowcolor='#ff7f0e',
    ax=-60, ay=-40,
    font=dict(size=11, color='#ff7f0e', family='Inter'),
    row=2, col=1
)

# Update axes
fig_training.update_xaxes(title_text="", row=1, col=1, showgrid=False)
fig_training.update_yaxes(title_text="Cost ($)", row=1, col=1, showgrid=True, gridcolor='#f0f0f0')
fig_training.update_xaxes(title_text="Years After Training", row=2, col=1, showgrid=True, gridcolor='#f0f0f0')
fig_training.update_yaxes(title_text="Annual Salary ($)", row=2, col=1, showgrid=True, gridcolor='#f0f0f0', tickformat='$,.0f')

# Update layout
fig_training.update_layout(
    height=600,
    width=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(size=11, family='Inter')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Inter, sans-serif', color='#262730'),
    margin=dict(t=80, b=60, l=60, r=40)
)


#### upskilling graph for board 5

# Graph 4: Upskilling Pathways for Chris (Logistics + AI)

upskill_options = pd.DataFrame({
    'Option': [
        'Coursera/edX\nAI for Logistics',
        'Community College\nCertificate',
        'Industry Bootcamp\n(AI+Supply Chain)',
        'Employer Sponsored\nTraining',
        'Government Subsidized\nProgram',
        'Weekend Upskilling\nWorkshops'
    ],
    'Cost': [350, 3200, 1800, 200, 500, 250],
    'Duration (months)': [2, 6, 3, 2, 4, 1]
})


fig_upskill = go.Figure(
    data=[
        go.Bar(
            x=upskill_options['Option'],
            y=upskill_options['Cost'],
            marker=dict(
                color=['#ff7f0e', '#4CAF50', '#81C784', '#2196F3', '#FFD43B', '#A259F7'],
                line=dict(color='white', width=2)
            ),
            text=[f"${c:,}" for c in upskill_options['Cost']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Cost: $%{y:,.0f}<br>Duration: %{customdata} months<extra></extra>',
            customdata=upskill_options['Duration (months)'],
            showlegend=False
        )
    ]
)

fig_upskill.update_layout(
    title="Upskilling Pathways for Chris: Logistics + AI",
    xaxis_title=None,  # Remove x-axis title
    yaxis_title="Cost ($)",
    height=400,
    width=600,
    font=dict(family="Inter, sans-serif", color="#262730"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=60, b=60, l=60, r=40),
    xaxis=dict(showticklabels=False),  # Hide x-axis tick labels
)

fig_upskill.update_xaxes(tickangle=0)  # Horizontal labels

# st.plotly_chart(fig_upskill, use_container_width=False)




training_chart_html = fig_upskill.to_html(
    include_plotlyjs="cdn", div_id="training-chart", config={"displayModeBar": False}
)






# End of board graphs








# Function to encode images as base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Encode toronto_jobs.png for board 1
toronto_jobs_path = "toronto_jobs.png"
if os.path.exists(toronto_jobs_path):
    toronto_jobs_encoded = encode_image(toronto_jobs_path)
    toronto_jobs_img = f'<img src="data:image/png;base64,{toronto_jobs_encoded}" style="max-width:100%; height:auto; margin-top:1.5rem; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1);" />'
else:
    toronto_jobs_img = '<p style="color:red;">toronto_jobs.png not found</p>'
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# board images (update with actual filenames)
boards_folder = "static/boards"
board_images = [
    # "board_title.png",
    "board1.png",  # GTA & Durham region
    # right pane has text and top cities with gen ai mentioned in jobs - indeed data

    "board2.png",  # Jiya is confident and seeking jobs in AI
    # right pane has education enrollment trend plotly

    "board3.png",  # she wants to up skill to stay ahead
    # right pane has quad chart of aioe and complementarity skills for jiya and chris

    "board4.png",  # christ works in logistics and faces automation risk and financial stress
    # right pane has chart of wage gap animation


    "board5.png",  # Chris needs AI training to transition to stable career path
    # right pane -- training pathways and ROI plotly

]


# Encode images as base64 data URLs
board_data_urls = []
for img in board_images:
    img_path = os.path.join(boards_folder, img)
    if os.path.exists(img_path):
        encoded = encode_image(img_path)
        board_data_urls.append(f"data:image/png;base64,{encoded}")
    else:
        st.error(f"Image not found: {img_path}")

# Build image tags for JS to swap in (as a JS array of strings)
board_img_tags_js = "[{}]".format(
    ",".join(
        [
            f"\"<img src='{url}' style='max-width:95%; max-height:95%; border-radius:10px; box-shadow:0 2px 8px #bbb;' />\""
            for url in board_data_urls
        ]
    )
)


scrolly_html = f"""
    <div id="scrolly" style="display: flex; flex-direction: row; gap: 2rem; align-items: flex-start;">
    <div class="sticky-thing" style="position: sticky; top: 10vh; width: 40vw; height: 70vh; background: #ffffff; border-radius: 12px; box-shadow: 0 2px 8px #ccc; display: flex; align-items: center; justify-content: center;">
        <div id="board" style="width: 90%; height: 90%; text-align: center;"><img src="{board_data_urls[0] if board_data_urls else ''}" style="max-width:95%; max-height:95%; border-radius:10px; box-shadow:0 2px 8px #bbb;" /></div>
    </div>
    <div class="steps" style="width: 55vw; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
        <div class="step" data-step="0" style="min-height: 100vh; padding: 2rem; opacity: 0.3; transition: opacity 0.3s;">
            <h2>The GTA is shaping to be the hub of AI transformation in Canada</h2>
            <p>The GTA and Durham Region are at the center of Canada's AI economy transformation.</p>
            {toronto_jobs_img}
            <ul style="margin-top: 1.5rem; text-align: left; line-height: 1.8; color: #333;">
                <li><strong>Toronto leads the nation</strong> with 0.32% of all job postings mentioning generative AI</li>
                <li><strong>Nearly 3x higher</strong> than the next closest city (Vancouver at 0.22%)</li>
                <li><strong>Growing AI ecosystem</strong> drives demand for skilled professionals like Jiya</li>
                <li><strong>Regional advantage:</strong> GTA and Durham Region positioned as Canada's AI hub</li>
            </ul>
        </div>

        <div class="step" data-step="1" style="min-height: 100vh; padding: 2rem; opacity: 0.3; transition: opacity 0.3s;">
            <h2>Jiya: Confident & Growing</h2>
            <p>Jiya is actively seeking AI jobs, confident in her skills and the opportunities ahead.</p>
            {enroll_chart_html}
            <ul style="margin-top: 1.5rem; text-align: left; line-height: 1.8; color: #333;">
                <li><strong>High demand for AI skills:</strong> Over 15,000 AI-related job postings in the GTA in 2024, with demand growing 40% year-over-year</li>
                <li><strong>Competitive salaries:</strong> Entry-level AI roles starting at $75,000-$90,000, significantly above the median graduate salary</li>
                <li><strong>Multiple pathways:</strong> Opportunities across tech companies, startups, financial services, healthcare, and government sectors</li>
                <li><strong>Skills translate to security:</strong> Machine learning, data science, and AI engineering skills remain in demand even during economic uncertainty</li>
                <li><strong>Growing field diversity:</strong> AI roles expanding beyond traditional tech into creative industries, education, and public services</li>
            </ul>
        </div>
        
        <div class="step" data-step="2" style="min-height: 100vh; padding: 2rem; opacity: 0.3; transition: opacity 0.3s;">
            <h2>There are a range of Complementary exposure effects in AI</h2>
            <p>Both Jiya and Chris experience different impacts and opportunities in the AI economy.</p>
            <div style="margin-top: 2rem;">
                {aioe_chart_html}
            </div>
            <ul style="margin-top: 1.5rem; text-align: left; line-height: 1.8; color: #333;">
                <li><strong>Jiya's position:</strong> High AI exposure (6.59) with lower complementarity (0.55) - she builds and controls AI systems</li>
                <li><strong>Chris's position:</strong> High AI exposure (6.09) with higher complementarity (0.60) - AI can enhance his supervisory work with proper training</li>
                <li><strong>The opportunity gap:</strong> Both face high AI exposure, but Chris's higher complementarity means training could help him thrive</li>
            </ul>
        </div>
        <div class="step" data-step="3" style="min-height: 100vh; padding: 2rem; opacity: 0.3; transition: opacity 0.3s;">
            <h2>Chris: Facing Uncertainty</h2>
            <p>Chris works in logistics and faces automation risks and growing financial stress.</p>
            <div style="margin-top: 2rem;">
                {chart_html}
            </div>
                  <ul style="margin-top: 1.5rem; text-align: left; line-height: 1.8; color: #333;">
                <li><strong>Wage growth is slow:</strong> Chris's income lags behind tech roles, widening the gap over time.</li>
                <li><strong>Job insecurity:</strong> Automation and AI adoption in logistics increase risks for supervisors.</li>
                <li><strong>Cost of living pressures:</strong> Rising rent and expenses make it harder for Chris to save.</li>
                <li><strong>Upskilling is critical:</strong> Without new skills, Chris risks being left behind in the AI economy.</li>
            </ul>


        </div>

        <div class="step" data-step="4" style="min-height: 100vh; padding: 2rem; opacity: 0.3; transition: opacity 0.3s;">
            <h2>Chris: Needs AI Training</h2>
            <p>Chris needs accessible AI training to transition to a more stable career path.</p>
            <div style="margin-top: 2rem;">
                {training_chart_html}
            </div>
            <ul style="margin-top: 1.5rem; text-align: left; line-height: 1.8; color: #333;">
                <li><strong>Training is affordable:</strong> Options range from $200 (employer/government) to $3,200 for comprehensive certificates</li>
                <li><strong>Real financial impact:</strong> AI-trained supervisors can earn $13,000+ more over 5 years</li>
                <li><strong>Quick payback:</strong> Most programs pay for themselves within 1-2 years through salary increases</li>
                <li><strong>Accessible pathways:</strong> Part-time, online, and subsidized options available across Ontario</li>
            </ul>

</div>

<script src="https://unpkg.com/intersection-observer"></script>
<script src="https://unpkg.com/scrollama"></script>
<script>
    const boardImgs = {board_img_tags_js};
    const scroller = scrollama();
    scroller
        .setup({{ step: '.step', offset: 0.5 }})
        .onStepEnter(response => {{
            // Remove active class from all steps
            document.querySelectorAll('.step').forEach(el => el.classList.remove('is-active'));
            // Add active class to current step
            response.element.classList.add('is-active');
            // Update board image
            updateBoard(response.index);
        }})
        .onStepExit(response => {{
            response.element.classList.remove('is-active');
        }});
    
    function updateBoard(step) {{
        const board = document.getElementById('board');
        if (boardImgs[step]) {{
            board.innerHTML = boardImgs[step];
        }}
    }}
    
    // Handle window resize
    window.addEventListener('resize', scroller.resize);
</script>

<style>
    .step.is-active {{
        opacity: 1 !important;
        background: #e6f0fa;
    }}
</style>
"""

components.html(scrolly_html, height=1200, scrolling=True)


# # --- Infographic Section ---
# st.markdown("---")
# st.subheader("Infographic: The AI Economy at a Glance")
# if os.path.exists("infograph.pdf"):
#     try:
#         images = convert_from_path("infograph.pdf", dpi=150, first_page=1, last_page=1)
#         st.image(images[0], caption="AI Economy Infographic", use_column_width=True)
#     except Exception as e:
#         st.warning(f"Could not display infographic: {e}")
# else:
#     st.info("Infographic not found.")
# st.markdown("---")

# # --- Monthly Expenses Bar Graph ---
# st.header("Monthly Expenses in Toronto/Durham (2025)")
# # Example data (replace with real data if available)
# expense_data = pd.DataFrame(
#     {
#         "Category": [
#             "Rent (1BR)",
#             "Groceries",
#             "Transit",
#             "Utilities",
#             "Internet",
#             "Leisure",
#             "Other",
#         ],
#         "Jiya (AI/Tech)": [2200, 400, 156, 120, 70, 200, 150],
#         "Chris (Logistics)": [1800, 400, 156, 120, 70, 100, 100],
#     }
# )
# expense_data = expense_data.set_index("Category")
# fig_exp, ax_exp = plt.subplots(figsize=(8, 4))
# expense_data.plot(kind="bar", ax=ax_exp, color=["#1f77b4", "#ff7f0e"])
# ax_exp.set_ylabel("Monthly Cost ($)")
# ax_exp.set_title("Estimated Monthly Expenses (Toronto/Durham, 2025)")
# ax_exp.set_ylim(bottom=0)
# plt.xticks(rotation=30)
# st.pyplot(fig_exp)
# st.caption(
#     "Source: [Toronto Cost of Living](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)"
# )
# st.markdown("---")

# # --- Income Gap Line Graph ---
# st.header("Income Gap: Jiya vs. Chris")
# ai_mask = salary_df[
#     "North American Industry Classification System (NAICS)"
# ].str.contains("Information|Professional|Scientific|Technical", case=False, na=False)
# chris_mask = salary_df[
#     "North American Industry Classification System (NAICS)"
# ].str.contains(
#     "Business|Logistics|Warehousing|Transportation|Trade", case=False, na=False
# )
# ai_group = salary_df[ai_mask].groupby("REF_DATE")["VALUE"].mean()
# chris_group = salary_df[chris_mask].groupby("REF_DATE")["VALUE"].mean()
# interval = max(1, len(ai_group) // 8)
# ai_group = ai_group.iloc[::interval]
# chris_group = chris_group.reindex(ai_group.index)
# fig, ax = plt.subplots(figsize=(8, 4))
# ax.plot(
#     ai_group.index, ai_group.values, marker="o", color="#1f77b4", label="Jiya (AI/Tech)"
# )
# ax.plot(
#     chris_group.index,
#     chris_group.values,
#     marker="o",
#     color="#ff7f0e",
#     label="Chris (Business/Admin)",
# )
# ax.set_ylabel("Average Hourly Wage ($)")
# ax.set_xlabel("Date")
# ax.set_title("Income Gap Over Time")
# ax.legend()
# ax.grid(True, alpha=0.2)
# ax.set_ylim(bottom=0)
# plt.xticks(rotation=30)
# st.pyplot(fig)
# st.caption(
#     "Source: [StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.html)"
# )
st.markdown("---")

# # --- Education Enrollment Comparison ---
# st.header("Upskilling: Education Trends")
# jiya_field = "Mathematics, computer and information sciences [7]"
# chris_field = "Business, management and public administration [5]"
# jiya_enroll = enroll_df[enroll_df["Field of study"] == jiya_field].set_index(
#     "REF_DATE"
# )["VALUE"]
# chris_enroll = enroll_df[enroll_df["Field of study"] == chris_field].set_index(
#     "REF_DATE"
# )["VALUE"]
# fig2, ax2 = plt.subplots(figsize=(8, 4))
# ax2.plot(
#     jiya_enroll.index,
#     jiya_enroll.values,
#     marker="o",
#     color="#1f77b4",
#     label="Jiya Field (Math/CS)",
# )
# ax2.plot(
#     chris_enroll.index,
#     chris_enroll.values,
#     marker="o",
#     color="#ff7f0e",
#     label="Chris Field (Business)",
# )
# ax2.set_ylabel("Enrollment")
# ax2.set_xlabel("Academic Year")
# ax2.set_title("Enrollment Trends by Field")
# ax2.legend()
# ax2.grid(True, alpha=0.2)
# ax2.set_ylim(bottom=0)
# plt.xticks(rotation=30)
# st.pyplot(fig2)
# st.caption(
#     "Source: [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)"
# )
# # st.markdown("---")

# # --- Interactive Geo Scatter for Enrollment (Simulated) ---
# st.header("Student Enrollment in AI/Tech vs. Business Across Canada")
# # More realistic mapping: major universities/cities and their known strengths
# geo_data = pd.DataFrame(
#     {
#         "lat": [
#             43.6629,
#             45.5048,
#             49.2606,
#             53.5232,
#             45.4215,
#             51.0447,
#             46.4746,
#             48.4634,
#             43.7735,
#             43.2609,
#         ],
#         "lon": [
#             -79.3957,
#             -73.5772,
#             -123.2460,
#             -113.5263,
#             -75.6972,
#             -114.0719,
#             -80.5449,
#             -123.3117,
#             -79.3345,
#             -79.9192,
#         ],
#         "enrollment": [3200, 2500, 2100, 1800, 1700, 1600, 1200, 900, 800, 700],
#         "course": [
#             "AI/Tech",
#             "AI/Tech",
#             "AI/Tech",
#             "AI/Tech",
#             "Business",
#             "Business",
#             "Business",
#             "Business",
#             "AI/Tech",
#             "Business",
#         ],
#         "city": [
#             "Toronto (UofT)",
#             "Montreal (McGill)",
#             "Vancouver (UBC)",
#             "Edmonton (UAlberta)",
#             "Ottawa (uOttawa)",
#             "Calgary (UCalgary)",
#             "Waterloo (Laurier)",
#             "Victoria (UVic)",
#             "Scarborough (UTSC)",
#             "Hamilton (McMaster)",
#         ],
#     }
# )
# color_map = {"AI/Tech": "#1f77b4", "Business": "#ff7f0e"}
# fig3 = px.scatter_geo(
#     geo_data,
#     lat="lat",
#     lon="lon",
#     color="course",
#     size="enrollment",
#     hover_name="city",
#     projection="natural earth",
#     color_discrete_map=color_map,
#     title="Student Enrollment in AI/Tech vs. Business by Major University/City",
#     size_max=30,
#     labels={"course": "Field"},
# )
# fig3.update_traces(marker=dict(line=dict(width=1, color="DarkSlateGrey")))
# fig3.update_layout(legend_title_text="Field", legend=dict(x=0.85, y=0.95))
# st.plotly_chart(fig3, use_container_width=True)
# st.caption(
#     "Bubble size = number of enrollments. Blue: AI/Tech, Orange: Business. Data mapped to major Canadian universities/cities."
# )
# st.markdown("---")


# # --- Pull Quotes & Links ---
# st.header("What the Experts Say")
# st.markdown(
#     """
# > "AI is both hurting and helping the next generation of workers."  
# <span style="font-size:0.9em;">- [The Globe and Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)</span>

# > "The jobs that will fall first as AI takes over the workplace."  
# <span style="font-size:0.9em;">- [Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)</span>
# """,
#     unsafe_allow_html=True,
# )




# # --- Folium Interactive Map ---
# if "enroll_df_geo" in locals() or "enroll_df_geo" in globals():
#     st.header("Interactive Map: Enrollment by Province (Folium)")

#     # Center of Canada
#     map_center = [56, -96]
#     folium_map = folium.Map(location=map_center, zoom_start=4, tiles="cartodbpositron")
#     # Color mapping
#     stream_colors = {"AI/Tech": "#0057b8", "Business": "#e66101"}
#     # Add circle markers for each province and stream
#     for _, row in enroll_df_geo.iterrows():
#         folium.CircleMarker(
#             location=[row["lat"], row["lon"]],
#             radius=max(6, min(row["Enrollment"] / 1000, 25)),
#             color=stream_colors.get(row["Stream"], "gray"),
#             fill=True,
#             fill_color=stream_colors.get(row["Stream"], "gray"),
#             fill_opacity=0.8,
#             popup=(
#                 f"<b>Province:</b> {row['Province']}<br>"
#                 f"<b>City:</b> {row['City']}<br>"
#                 f"<b>Field:</b> {row['Stream']}<br>"
#                 f"<b>Enrollment:</b> {int(row['Enrollment']):,}"
#             ),
#             tooltip=f"{row['Province']} - {row['Stream']}: {int(row['Enrollment']):,}",
#         ).add_to(folium_map)
#     # Add a legend manually
#     from branca.element import MacroElement
#     from jinja2 import Template

#     legend_html = """
#     {% macro html(this, kwargs) %}
#     <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 70px; z-index:9999; font-size:16px; background: white; border:2px solid #ccc; border-radius:8px; padding: 10px;">
#     <b>Legend</b><br>
#     <span style="color:#0057b8; font-weight:bold;">&#9679;</span> AI/Tech<br>
#     <span style="color:#e66101; font-weight:bold;">&#9679;</span> Business
#     </div>
#     {% endmacro %}
#     """
#     legend = MacroElement()
#     legend._template = Template(legend_html)
#     folium_map.get_root().add_child(legend)
#     st_data = st_folium(folium_map, width=1200, height=600)
#     st.caption(
#         "Circle size = enrollment. Click or hover for details. Blue: AI/Tech, Orange: Business."
#     )
#     st.markdown("---")


# st.subheader("Infographic: The AI Economy at a Glance")
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


# affordability crisis section from pdf

# --- AI Divide PDF for Slide 6 ---
pdf_path_6 = "The AI Divide in GTA-6.pdf"
if os.path.exists(pdf_path_6):
    try:
        pages = convert_from_path(pdf_path_6, dpi=150, first_page=1, last_page=1)
        st.image(pages[0], caption="AI Divide: Slide 6", use_container_width=True)
    except Exception as e:
        st.warning(f"Could not render {pdf_path_6}: {e}")
else:
    st.info(f"File not found: {pdf_path_6}")







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
st.pyplot(fig_exp,use_container_width=False)
st.caption(
    "Source: [Toronto Cost of Living](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)"
)
st.markdown("---")
# --- Monthly Expenses Bar Graph --- //////////////////////////////////////


# # --- Income Gap Line Graph ---
# st.header("Income Gap: Jiya vs. Chris")
# ai_mask = salary_df[
#     "North American Industry Classification System (NAICS)"
# ].str.contains("Information|Professional|Scientific|Technical", case=False, na=False)
# chris_mask = salary_df[
#     "North American Industry Classification System (NAICS)"
# ].str.contains(
#     "Business|Logistics|Warehousing|Transportation|Trade", case=False, na=False
# )
# ai_group = salary_df[ai_mask].groupby("REF_DATE")["VALUE"].mean()
# chris_group = salary_df[chris_mask].groupby("REF_DATE")["VALUE"].mean()
# interval = max(1, len(ai_group) // 8)
# ai_group = ai_group.iloc[::interval]
# chris_group = chris_group.reindex(ai_group.index)
# fig, ax = plt.subplots(figsize=(8, 4))
# ax.plot(
#     ai_group.index, ai_group.values, marker="o", color="#1f77b4", label="Jiya (AI/Tech)"
# )
# ax.plot(
#     chris_group.index,
#     chris_group.values,
#     marker="o",
#     color="#ff7f0e",
#     label="Chris (Business/Admin)",
# )
# ax.set_ylabel("Average Hourly Wage ($)")
# ax.set_xlabel("Date")
# ax.set_title("Income Gap Over Time")
# ax.legend()
# ax.grid(True, alpha=0.2)
# ax.set_ylim(bottom=0)
# plt.xticks(rotation=30)
# st.pyplot(fig)
# st.caption(
#     "Source: [StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.html)"
# )
# st.markdown("---")

# # --- Education Enrollment Comparison ---
# st.header("Upskilling: Education Trends")
# jiya_field = "Mathematics, computer and information sciences [7]"
# chris_field = "Business, management and public administration [5]"
# jiya_enroll = enroll_df[enroll_df["Field of study"] == jiya_field].set_index(
#     "REF_DATE"
# )["VALUE"]
# chris_enroll = enroll_df[enroll_df["Field of study"] == chris_field].set_index(
#     "REF_DATE"
# )["VALUE"]
# fig2, ax2 = plt.subplots(figsize=(8, 4))
# ax2.plot(
#     jiya_enroll.index,
#     jiya_enroll.values,
#     marker="o",
#     color="#1f77b4",
#     label="Jiya Field (Math/CS)",
# )
# ax2.plot(
#     chris_enroll.index,
#     chris_enroll.values,
#     marker="o",
#     color="#ff7f0e",
#     label="Chris Field (Business)",
# )
# ax2.set_ylabel("Enrollment")
# ax2.set_xlabel("Academic Year")
# ax2.set_title("Enrollment Trends by Field")
# ax2.legend()
# ax2.grid(True, alpha=0.2)
# ax2.set_ylim(bottom=0)
# plt.xticks(rotation=30)
# st.pyplot(fig2)
# st.caption(
#     "Source: [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)"
# )
# st.markdown("---")



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

# # --- Conclusion ---
# st.header("The Future: A Call to Action")
# st.markdown("""
# This story shows why learning new skills for AI jobs is more important than ever. Some people move ahead, while others risk being left behind. The future in Durham and the GTA depends on which skills young people have — and those struggling most will find it harder to keep up, unless they get help.

# ---

# **Explore the links and data above. Scroll to see how Jiya and Chris's paths diverge in the AI economy.**

# - [PG Student Enrollment Stats](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3710001101)
# - [AI jobs domain - StatCan](https://www150.statcan.gc.ca/n1/pub/11f0019m/11f0019m2024005-eng.htm)
# - [Cost of Living in Toronto](https://open.toronto.ca/dataset/cost-of-living-in-toronto-for-low-income-households/)
# - [The IMF report on AI and jobs](https://stefanbauschard.substack.com/p/the-imf-report-on-ai-and-jobs-is)
# - [AI and Jobs: Forbes](https://www.forbes.com/sites/jackkelly/2025/04/25/the-jobs-that-will-fall-first-as-ai-takes-over-the-workplace/)
# - [AI and Young Wages: Globe & Mail](https://www.theglobeandmail.com/business/article-how-ai-is-both-hurting-and-helping-the-next-generation-of-workers/)
# """)


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

### final slide 


# --- AI Divide PDF for Slide 6 ---
pdf_path = "The Adaptation Trap.pdf"
if os.path.exists(pdf_path):
    try:
        pages = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)
        st.image(
            pages[0],
            caption="AI Divide: daily reality for Jiya vs Chris",
            use_container_width=True,
        )
    except Exception as e:
        st.warning(f"Could not render {pdf_path}: {e}")
else:
    st.info(f"File not found: {pdf_path}")


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