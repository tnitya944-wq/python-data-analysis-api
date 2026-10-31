# Python Data Analysis & REST API Project

A beginner-friendly data analysis application using NumPy, Pandas, Matplotlib, and Requests.

## Features
- Load CSV data into a Pandas DataFrame
- Clean column names, remove duplicate rows, and fill missing values
- Calculate descriptive statistics and missing-value summaries
- Generate histograms and a correlation heatmap when numeric columns allow it
- Save a cleaned CSV and a text analysis report
- Consume a public REST API and save a sample JSON response

## Requirements
Python 3.9+ and packages listed in `requirements.txt`.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
python data_analysis_app.py
```

Press Enter to use `sample_dataset.csv`. The program creates an `output/` folder with the cleaned dataset, report, plots, and optional API JSON file.

## Google Colab
1. Open Google Colab: https://colab.research.google.com/
2. Create a new notebook.
3. Upload this project or upload `sample_dataset.csv`.
4. Install dependencies in a notebook cell:

   ```python
   %pip install pandas numpy matplotlib seaborn requests
   ```
5. Run the code from `data_analysis_app.py` in a cell, or upload the Python file and run it using notebook commands.

## Concepts demonstrated
- NumPy/Pandas fundamentals and DataFrames
- Data cleaning and manipulation
- Descriptive statistics
- Matplotlib visualization
- HTTP GET requests, status checks, timeouts, and JSON payloads
- Report generation and file output

## Notes
The sample dataset intentionally includes duplicate rows and missing values so the cleaning steps can be demonstrated. API access requires an internet connection.
