import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")


st.markdown(
    """
    <style>
    /* Make dropdown checkboxes smaller */
    .stMultiSelect div[data-baseweb="menu"] {
        font-size: 1px !important;  /* Smaller text inside dropdown */
    }
    /* Reduce the height of dropdown options */
    .stMultiSelect div[data-baseweb="option"] {
        min-height: 1px !important;  /* Reduce option height */
        padding: 1px 1px !important;  /* Less padding inside */
    }
    /* Make selected option boxes (red tags) smaller */
    .stMultiSelect div[data-baseweb="tag"] {
        font-size: 1px !important;  
        padding: 1px 1px !important;  
        height: 1px !important;  
        line-height: 1px !important;
        border-radius: 1px !important;  
    }
    </style>
    """,
    unsafe_allow_html=True,
)


df = pd.read_csv("cleaned_ufo_sightings.csv")


df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')


df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')


df = df[df['country'] == "us"]


state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

df['state'] = df['state'].str.upper().map(state_mapping)

shape_mapping = {
    'light': 'Light', 
    'flash': 'Light',
    'flare': 'Light',
    'fireball': 'Round',
    'circle': 'Round',
    'sphere': 'Round',
    'disk': 'Round',
    'oval': 'Round',
    'egg': 'Round',
    'round': 'Round',
    'cylinder': 'Cylindrical',
    'cigar': 'Cylindrical',
    'cone': 'Cylindrical',
    'triangle': 'Triangular',
    'delta': 'Triangular',
    'pyramid': 'Triangular',
    'diamond': 'Triangular',
    'chevron': 'Triangular',
    'formation': 'Multiple Objects',
    'changing': 'Multiple Objects',
    'changed': 'Multiple Objects',
    'rectangle': 'Rectangular',
    'cross': 'Cross',
    'hexagon': 'Hexagon',
    'crescent': 'Crescent',
    'teardrop': 'Teardrop',
    'unknown': 'Other',
    'other': 'Other'
}

df['shape'] = df['shape'].map(shape_mapping).fillna(df['shape'])


def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)} sec"
    else:
        return f"{round(seconds / 60, 2)} min"

df["Duration"] = df["duration (seconds)"].apply(format_duration)


st.title("UFO Sightings in the US")


st.sidebar.header("Filter UFO Sightings")


state_options = df['state'].dropna().unique().tolist()
state_selection = st.sidebar.multiselect("Select State", options=state_options, default=state_options if state_options else [])


df_filtered = df[df['state'].isin(state_selection)]


df_filtered = df_filtered.reset_index(drop=True)
df_filtered['id'] = df_filtered.index + 1  


color_map = {
    'Light': 'rgb(200, 0, 0)',  # Dark Red
    'Round': 'rgb(0, 0, 139)',  # Dark Blue
    'Cylindrical': 'rgb(0, 128, 0)',  # Dark Green
    'Triangular': 'rgb(128, 0, 128)',  # Dark Purple
    'Multiple Objects': 'rgb(255, 165, 0)',  # Dark Orange
    'Rectangular': 'rgb(255, 0, 255)',  # Dark Magenta
    'Cross': 'rgb(0, 0, 0)',  # Black
    'Hexagon': 'rgb(0, 100, 0)',  # Dark Green
    'Crescent': 'rgb(255, 69, 0)',  # Dark Orange Red
    'Teardrop': 'rgb(0, 139, 139)',  # Dark Cyan
    'Other': 'rgb(169, 169, 169)'  # Dark Grey
}


st.subheader("UFO Sightings Map (Hover to see details)")

fig = px.scatter_mapbox(
    df_filtered,
    lat="latitude",
    lon="longitude",
    hover_name="city",
    hover_data={
        "city": True,
        "state": True,
        "shape": True,
        "Duration": True,
        "comments": True
    },
    color="shape",
    color_discrete_map=color_map, 
    mapbox_style="open-street-map",
    zoom=2.5,
    height=600,
    width=800
)


fig.update_traces(marker=dict(size=6, opacity=0.7, allowoverlap=True))

st.plotly_chart(fig, use_container_width=True)
