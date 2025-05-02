# Intercom Customer Support Report Generator

This Streamlit application generates a monthly customer support report from a raw CSV export from Intercom, allowing users to filter and visualize key metrics.

## Project Structure

```
MBR_report_generator/
├── manifest.yml                  # Snowflake app config
├── setup.sql                     # (Optional) roles/warehouse setup script
├── streamlit_app/                # App source code
│   ├── app.py                    # Your main Streamlit app
│   ├── utils/
│   │   ├── filters.py
│   │   ├── charts.py
│   │   └── metrics.py
│   ├── requirements.txt
│   └── __init__.py
```

## Setup

1.  **Clone the repository (if applicable).**
2.  **Ensure you have Python 3.8+ installed.**
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
2.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
3.  Upload your Intercom CSV export using the file uploader in the sidebar.
4.  The application will process the data and display the dashboard.
5.  Use the filters in the sidebar to refine the analysis.
6.  To save a snapshot of the current view, use your browser's Print function (Ctrl+P or Cmd+P) and select "Save as PDF".
7.  Use the "Download Metrics Table (HTML)" button to download the main summary table.

## Key Features

*   Monthly Metrics Summary (Table)
*   Ticket Performance Overview (Opened vs Resolved, Avg/Median Close Time)
*   Top Ticket Types (Category & Issue Source)
*   Priority & Escalation Distribution Pie Charts
*   Top Customers by Ticket Volume
*   Ticket Closures by Agent
*   Extensive Sidebar Filtering Options 
