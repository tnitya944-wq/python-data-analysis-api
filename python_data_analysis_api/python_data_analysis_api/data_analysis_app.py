"""
Python Data Analysis Application
Loads a CSV dataset, cleans it with Pandas, summarizes it, creates plots,
and optionally fetches JSON from a public REST API.
"""

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
import requests

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_dataset(file_path):
    """Load a CSV file into a Pandas DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError("Please provide a CSV file.")
    return pd.read_csv(path)


def clean_dataset(df):
    """Return a cleaned copy: normalize headers, remove duplicates, fill missing values."""
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.astype(str).str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
    )
    cleaned = cleaned.drop_duplicates()

    for column in cleaned.columns:
        if pd.api.types.is_numeric_dtype(cleaned[column]):
            median = cleaned[column].median()
            if pd.notna(median):
                cleaned[column] = cleaned[column].fillna(median)
        else:
            modes = cleaned[column].mode(dropna=True)
            fill_value = modes.iloc[0] if not modes.empty else "Unknown"
            cleaned[column] = cleaned[column].fillna(fill_value)

    return cleaned


def generate_report(df):
    """Generate useful summary statistics and a text report."""
    report_lines = [
        "PYTHON DATA ANALYSIS REPORT",
        "=" * 28,
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        "",
        "Column names:",
        ", ".join(map(str, df.columns)),
        "",
        "Missing values per column:",
        df.isna().sum().to_string(),
        "",
        "Summary statistics:",
        df.describe(include="all").to_string(),
    ]
    report_path = OUTPUT_DIR / "analysis_report.txt"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return report_path


def save_cleaned_data(df):
    path = OUTPUT_DIR / "cleaned_dataset.csv"
    df.to_csv(path, index=False)
    return path


def create_visualizations(df):
    """Create a histogram for numeric columns and a correlation heatmap when possible."""
    numeric = df.select_dtypes(include="number")
    created = []

    if not numeric.empty:
        for column in numeric.columns[:4]:
            plt.figure(figsize=(7, 4))
            numeric[column].dropna().plot(kind="hist", bins=15, title=f"Distribution of {column}")
            plt.xlabel(column)
            plt.tight_layout()
            path = OUTPUT_DIR / f"{column}_histogram.png"
            plt.savefig(path)
            plt.close()
            created.append(path)

        if len(numeric.columns) >= 2:
            plt.figure(figsize=(7, 5))
            correlation = numeric.corr(numeric_only=True)
            plt.imshow(correlation, interpolation="nearest", aspect="auto")
            plt.colorbar(label="Correlation")
            plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha="right")
            plt.yticks(range(len(correlation.columns)), correlation.columns)
            plt.title("Correlation Heatmap")
            plt.tight_layout()
            path = OUTPUT_DIR / "correlation_heatmap.png"
            plt.savefig(path)
            plt.close()
            created.append(path)

    return created


def fetch_json_api(url="https://jsonplaceholder.typicode.com/posts", limit=10):
    """Fetch JSON from a public REST API with timeout and error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as error:
        raise RuntimeError(f"API request failed: {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("API response was not valid JSON.") from error

    if isinstance(payload, list):
        return payload[:limit]
    return payload


def run_analysis(csv_path):
    """Run the full load-clean-analyze-visualize-report workflow."""
    raw = load_dataset(csv_path)
    cleaned = clean_dataset(raw)
    cleaned_path = save_cleaned_data(cleaned)
    report_path = generate_report(cleaned)
    plots = create_visualizations(cleaned)
    return {
        "rows_before": len(raw),
        "rows_after": len(cleaned),
        "columns": len(cleaned.columns),
        "cleaned_csv": str(cleaned_path),
        "report": str(report_path),
        "plots": [str(path) for path in plots],
    }


def main():
    print("=== Python Data Analysis Application ===")
    default_csv = Path(__file__).parent / "sample_dataset.csv"
    csv_path = input(f"CSV path (Enter for {default_csv.name}): ").strip()
    if not csv_path:
        csv_path = str(default_csv)

    try:
        result = run_analysis(csv_path)
        print("\nAnalysis completed!")
        print(json.dumps(result, indent=2))
    except (FileNotFoundError, ValueError, pd.errors.ParserError, OSError) as error:
        print(f"Dataset analysis error: {error}")

    choice = input("\nFetch sample JSON data from a public REST API? (y/n): ").strip().lower()
    if choice == "y":
        try:
            data = fetch_json_api()
            api_path = OUTPUT_DIR / "api_sample.json"
            api_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"Fetched {len(data) if isinstance(data, list) else 1} API item(s). Saved to {api_path}")
        except RuntimeError as error:
            print(error)


if __name__ == "__main__":
    main()
