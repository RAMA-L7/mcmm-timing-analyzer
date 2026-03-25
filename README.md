# MCMM Timing Analyzer

A Python-based GUI tool to parse and analyze MCMM timing reports.

## Features
- Parse MCMM timing reports
- View all timing paths in a table
- Highlight timing violations (negative slack)
- Filter by scenario
- Search by startpoint
- Show worst path
- Export results to CSV

## Tech Stack
- Python
- Tkinter (GUI)
- Pandas

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   python gui.py


## Usage
- Click **Load Report** to load timing report
- Use filters and search options
- Export results using **Export CSV**

## Notes
- Input file should be a standard MCMM timing report
