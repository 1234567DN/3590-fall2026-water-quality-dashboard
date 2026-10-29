# Agile Process Evidence

## Product goal

Deliver a clear, reliable, and beginner-friendly Streamlit dashboard that lets a user explore Biscayne Bay water-quality observations without editing Python code.

## Backlog and acceptance criteria

| Story | Acceptance criteria | Status |
|---|---|---|
| As a user, I can see what the app is about | Overview text and dataset explanation are visible | Done |
| As a user, I can focus the analysis | Date range, measure selector, and numeric slider update the view | Done |
| As a user, I can understand the data visually | Plotly trend, relationship, and map charts have titles, labels, and legends | Done |
| As a user, I can inspect and reuse results | Filtered table and CSV download are available | Done |
| As a reviewer, I can run the project | `requirements.txt`, README, and a local run command are included | Done |
| As a student, I can explain my software process | This Agile evidence file documents the workflow | Done |

## Iterations

### Iteration 1 — Discover and plan

- Reviewed the course rubric and starter repository.
- Identified the supplied Biscayne Bay CSV as the app's data source.
- Audited the columns and missing values before choosing safe visualizations.

### Iteration 2 — Build the minimum usable product

- Reworked the starter dashboard into a clear Streamlit layout.
- Added cached loading, date parsing, data filtering, KPI cards, and a selectable primary measure.
- Added the interactive Plotly trend chart.

### Iteration 3 — Add user value and polish

- Added relationship and geographic visualizations.
- Added quick insights, a filtered preview table, CSV download, upload support, help text, and responsive columns/tabs.
- Added friendly empty-state and upload-error handling.

### Iteration 4 — Test and prepare release

- Verified imports and data transformations locally.
- Checked the Streamlit app starts in headless mode.
- Added requirements, README, deployment steps, and this evidence file.
- Prepared the `main` branch for GitHub and Streamlit Community Cloud.

## Definition of done

The dashboard is considered done when it runs without errors from a clean environment, all required controls and Plotly visualizations work, the documentation explains setup and use, and the repository can be deployed directly by Streamlit Community Cloud.
