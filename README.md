# Biscayne Bay Water Quality Explorer

An interactive Streamlit dashboard for exploring water-quality observations collected during an autonomous Biscayne Bay survey. The app was created for the CIS 3590 **Interactive Data Visualization & App Development** assignment.

## What the app includes

- An included CSV dataset with water-quality, location, depth, and navigation readings.
- Sidebar controls for optional CSV upload, date-range filtering, a primary measure selector, and a numeric range slider.
- Interactive Plotly charts for trends, temperature/salinity relationships, and the survey route.
- KPI cards, descriptive explanations, quick insights, a filtered data preview, and CSV download.
- A responsive layout organized into Overview, Interactive analysis, and Data and insights sections.

## Dataset

The app uses `biscayneBay_waterquality.csv`, supplied with the CIS 3590 course materials. It contains 942 observations and 69 columns from a Biscayne Bay survey, including latitude, longitude, temperature, salinity, dissolved oxygen, pH, turbidity, chlorophyll, and depth fields. The app performs only light cleaning: it strips accidental whitespace from column names and parses the survey date for filtering and charting.

## Run locally

1. Clone this repository.
2. Create and activate a Python virtual environment (recommended).
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run water_dashboard.py
   ```

5. Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## User instructions

Use the sidebar to select a date range, choose a primary measurement, and narrow the measurement range. The Trend tab shows the selected measurement over time. The Relationships tab compares temperature and salinity, with color representing water-column depth. The Survey map shows where temperature observations were recorded. The filtered table can be downloaded as a CSV.

You may also upload a compatible CSV. Uploaded files should include the fields used by the selected chart, especially `Date`, `Temperature (c)`, `Salinity (ppt)`, `ODO mg/L`, `Total Water Column (m)`, `Latitude`, and `Longitude`.

## Deployment

This repository is structured for Streamlit Community Cloud:

1. Open [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with GitHub.
3. Choose this repository, branch `main`, and file `water_dashboard.py`.
4. Deploy and copy the generated public URL into the course submission.

No secrets or API keys are required.

## Agile process evidence

The project used a small iterative Agile workflow documented in [`AGILE.md`](AGILE.md). Work was divided into short increments: inspect the starter app and dataset, implement the core dashboard, add interaction and documentation, then test and prepare deployment. Each increment produced a working app that could be reviewed before the next change.

## Course deliverables

- Public Streamlit app URL: add the deployed URL here after Streamlit Community Cloud deployment.
- GitHub repository: this repository.
- README: this file.
