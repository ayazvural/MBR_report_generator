# Intercom Customer Support Report Generator

This Streamlit application generates a monthly customer support report from a raw CSV export from Intercom, allowing users to filter and visualize key metrics.

## Project Structure

```
support-report/
│
├── app.py                   # Main Streamlit application script
├── utils/                   # Helper modules
│   ├── filters.py           # Sidebar filter logic
│   ├── charts.py            # Chart generation functions
│   └── metrics.py           # Data loading, processing, and metric calculations
├── assets/                  # (Optional) Static files like logos or custom CSS
├── data/                    # (Optional) Placeholder for sample data or instructions
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore file
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