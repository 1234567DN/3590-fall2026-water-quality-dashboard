"""Interactive Biscayne Bay water-quality dashboard.

Run locally with:
    streamlit run water_dashboard.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# Configuration and constants
# -----------------------------
DATA_FILE = Path(__file__).parent / "biscayneBay_waterquality.csv"
APP_TITLE = "Biscayne Bay Water Quality Explorer"

MEASURE_OPTIONS = {
    "Water temperature (°C)": "Temperature (c)",
    "Salinity (ppt)": "Salinity (ppt)",
    "Dissolved oxygen (mg/L)": "ODO mg/L",
    "pH": "pH",
    "Turbidity (NTU)": "Turbid+ NTU",
    "Chlorophyll (µg/L)": "Chl ug/L",
    "Depth (m)": "Total Water Column (m)",
}

PLOTLY_CONFIG = {"displaylogo": False, "responsive": True}


# -----------------------------
# Data functions
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data(source: str | Path) -> pd.DataFrame:
    """Load and lightly clean the dashboard data."""
    frame = pd.read_csv(source)
    frame.columns = frame.columns.str.strip()

    # The source includes a human-readable time string and a date string.
    # Converting them once makes filtering and chart labels predictable.
    if "Date" in frame:
        frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    if "Time hh:mm:ss" in frame:
        frame["Time of day"] = frame["Time hh:mm:ss"].astype(str)

    return frame


def numeric_columns(frame: pd.DataFrame) -> list[str]:
    """Return numeric columns suitable for user-selected charts."""
    excluded = {"Latitude", "Longitude"}
    return [
        column
        for column in frame.select_dtypes(include="number").columns
        if column not in excluded and frame[column].notna().any()
    ]


def format_number(value: float | int | None, digits: int = 2) -> str:
    """Format a metric value for a compact KPI card."""
    if value is None or pd.isna(value):
        return "—"
    return f"{value:,.{digits}f}"


def filter_data(
    frame: pd.DataFrame,
    date_range: tuple,
    parameter: str,
    min_value: float,
    max_value: float,
) -> pd.DataFrame:
    """Apply the sidebar's date and parameter filters."""
    filtered = frame.copy()
    if "Date" in filtered and date_range:
        start = pd.Timestamp(date_range[0])
        end = pd.Timestamp(date_range[-1])
        filtered = filtered[filtered["Date"].between(start, end)]

    if parameter in filtered:
        filtered = filtered[filtered[parameter].between(min_value, max_value)]
    return filtered


def plot_time_series(frame: pd.DataFrame, parameter: str, label: str):
    """Create the primary interactive time-series chart."""
    chart_data = frame[["Date", parameter]].dropna().sort_values("Date")
    figure = px.line(
        chart_data,
        x="Date",
        y=parameter,
        markers=True,
        title=f"{label} across survey observations",
        labels={"Date": "Survey date", parameter: label},
        template="plotly_white",
    )
    figure.update_layout(hovermode="x unified", legend_title_text="Measure")
    return figure


def plot_scatter(frame: pd.DataFrame):
    """Create a labeled relationship chart for temperature and salinity."""
    chart_data = frame[["Temperature (c)", "Salinity (ppt)", "Total Water Column (m)"]].dropna()
    return px.scatter(
        chart_data,
        x="Temperature (c)",
        y="Salinity (ppt)",
        color="Total Water Column (m)",
        color_continuous_scale="Viridis",
        title="Temperature and salinity relationship",
        labels={
            "Temperature (c)": "Temperature (°C)",
            "Salinity (ppt)": "Salinity (ppt)",
            "Total Water Column (m)": "Water column depth (m)",
        },
        template="plotly_white",
    )


def plot_map(frame: pd.DataFrame):
    """Create a geographic view of the recorded survey path."""
    chart_data = frame.dropna(subset=["Latitude", "Longitude", "Temperature (c)"])
    return px.scatter_map(
        chart_data,
        lat="Latitude",
        lon="Longitude",
        color="Temperature (c)",
        color_continuous_scale="Turbo",
        zoom=14,
        center={"lat": float(chart_data["Latitude"].mean()), "lon": float(chart_data["Longitude"].mean())},
        title="Survey observations across Biscayne Bay",
        labels={"Temperature (c)": "Temperature (°C)"},
        hover_data={"Latitude": ":.5f", "Longitude": ":.5f", "Temperature (c)": ":.2f"},
    )


# -----------------------------
# Page layout
# -----------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(APP_TITLE)
st.markdown(
    "Explore an autonomous survey of Biscayne Bay through interactive charts, "
    "summary statistics, and a geographic observation map."
)
st.caption("CIS 3590 • Interactive Data Visualization & App Development")

with st.sidebar:
    st.header("Dashboard controls")
    st.write("Use the controls below to focus the analysis on a date range and measurement.")
    uploaded_file = st.file_uploader(
        "Optional: upload another compatible CSV",
        type=["csv"],
        help="The uploaded file should include the same water-quality field names as the included dataset.",
    )

    try:
        data = load_data(uploaded_file) if uploaded_file is not None else load_data(DATA_FILE)
    except Exception as error:  # Friendly error for an incompatible upload.
        st.error(f"The file could not be loaded: {error}")
        st.stop()

    if "Date" in data and data["Date"].notna().any():
        dates = data["Date"].dropna()
        default_range = (dates.min().date(), dates.max().date())
        selected_dates = st.date_input("Survey date range", value=default_range)
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            date_range = selected_dates
        else:
            date_range = default_range
    else:
        date_range = ()

    st.divider()
    selected_label = st.selectbox("Primary measure", list(MEASURE_OPTIONS))
    selected_parameter = MEASURE_OPTIONS[selected_label]

    if selected_parameter not in data or not pd.api.types.is_numeric_dtype(data[selected_parameter]):
        st.error(f"The uploaded file does not contain numeric data for {selected_label}.")
        st.stop()

    parameter_values = data[selected_parameter].dropna()
    if parameter_values.empty:
        st.warning("No values are available for the selected measure.")
        st.stop()
    lower, upper = float(parameter_values.min()), float(parameter_values.max())
    value_range = st.slider(
        f"Filter {selected_label}",
        min_value=lower,
        max_value=upper,
        value=(lower, upper),
        help="Drag the handles to keep only observations in this value range.",
    )

filtered = filter_data(data, date_range, selected_parameter, value_range[0], value_range[1])

if filtered.empty:
    st.warning("No observations match the selected filters. Widen the date or value range to continue.")
    st.stop()

# Overview section
st.header("Overview")
st.write(
    "This dashboard uses measurements collected during an autonomous Biscayne Bay survey. "
    "The dataset combines navigation, water-column, and water-quality readings. "
    "Adjust the controls in the sidebar to explore how the observations change."
)

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Visible observations", f"{len(filtered):,}")
kpi_2.metric("Survey days", f"{filtered['Date'].nunique():,}" if "Date" in filtered else "—")
kpi_3.metric(f"Average {selected_label}", format_number(filtered[selected_parameter].mean()))
kpi_4.metric("Average depth (m)", format_number(filtered["Total Water Column (m)"].mean()))

st.divider()

# Analysis section
st.header("Interactive analysis")
analysis_tab, relationship_tab, map_tab = st.tabs(["Trend", "Relationships", "Survey map"])

with analysis_tab:
    st.subheader(f"{selected_label} over time")
    st.plotly_chart(plot_time_series(filtered, selected_parameter, selected_label), use_container_width=True, config=PLOTLY_CONFIG)
    st.info(
        "How to read this chart: hover over a point for its date and value. "
        "Use the sidebar filters to isolate a smaller range of survey conditions."
    )

with relationship_tab:
    st.subheader("Compare two water-quality measures")
    st.plotly_chart(plot_scatter(filtered), use_container_width=True, config=PLOTLY_CONFIG)
    st.write(
        "Each point represents a recorded observation. Color indicates the measured water-column depth, "
        "which helps show whether depth is associated with temperature and salinity patterns."
    )

with map_tab:
    st.subheader("Where were the observations recorded?")
    if {"Latitude", "Longitude", "Temperature (c)"}.issubset(filtered.columns):
        st.plotly_chart(plot_map(filtered), use_container_width=True, config=PLOTLY_CONFIG)
        st.caption("The color scale represents temperature in degrees Celsius.")
    else:
        st.warning("The uploaded data does not include the location fields needed for the map.")

# Data and insights section
st.header("Data and insights")
insight_col, table_col = st.columns([1, 1])
with insight_col:
    st.subheader("Quick insights")
    st.markdown(
        f"- The current view contains **{len(filtered):,} observations**.\n"
        f"- **{selected_label}** ranges from **{format_number(filtered[selected_parameter].min())}** "
        f"to **{format_number(filtered[selected_parameter].max())}**.\n"
        f"- The average dissolved oxygen reading is **{format_number(filtered['ODO mg/L'].mean())} mg/L**.\n"
        f"- The average salinity is **{format_number(filtered['Salinity (ppt)'].mean())} ppt**."
    )
    st.caption("These are descriptive observations, not a scientific determination of ecosystem health.")

with table_col:
    st.subheader("Filtered data preview")
    preview_columns = list(
        dict.fromkeys(
            column
            for column in [
                "Date",
                "Latitude",
                "Longitude",
                selected_parameter,
                "Temperature (c)",
                "Salinity (ppt)",
                "ODO mg/L",
            ]
            if column in filtered.columns
        )
    )
    st.dataframe(filtered[preview_columns].head(25), use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="biscayne_bay_filtered.csv",
        mime="text/csv",
    )

with st.expander("About this dataset"):
    st.write(
        "The included CSV is the Biscayne Bay water-quality survey supplied with the CIS 3590 course materials. "
        "The dashboard preserves the original measurements and applies only light date/column cleaning for display."
    )
    st.write(f"Rows in source dataset: **{len(data):,}** • Columns: **{len(data.columns):,}**")
