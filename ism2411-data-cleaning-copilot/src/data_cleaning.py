"""
Data Cleaning Script
Course: ISM 2411 - Muma College of Business (USF)

Purpose:
This script processes messy raw sales data (sales_data_raw.csv), cleans dirty text fields,
standardizes column names, handles missing values, and removes invalid business records.
"""

import os
import pandas as pd


# Helper Functions
def load_data(file_path: str) -> pd.DataFrame:
    """Loads raw sales dataset from a CSV file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: Target file not found at path '{file_path}'.")
    return pd.read_csv(file_path)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names to lowercase and replaces spaces with underscores."""
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
    )
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Strips whitespace from text fields and handles NaNs in numeric fields."""
    df = df.copy()

    # Strip whitespace from string columns
    string_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Coerce numeric values
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    if 'qty' in df.columns:
        df['qty'] = pd.to_numeric(df['qty'], errors='coerce')

    # Impute missing values
    if 'price' in df.columns:
        median_price = df['price'].median()
        df['price'] = df['price'].fillna(median_price)

    if 'qty' in df.columns:
        df['qty'] = df['qty'].fillna(0)

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Filters out invalid records where quantity or price is negative."""
    df = df.copy()

    if 'qty' in df.columns:
        df = df[df['qty'] >= 0]

    if 'price' in df.columns:
        df = df[df['price'] >= 0]

    return df


# Main Execution Block
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    raw_path = os.path.join(project_root, "data", "raw", "sales_data_raw.csv")
    cleaned_path = os.path.join(project_root, "data", "processed", "sales_data_clean.csv")

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

    print("--- Starting Data Cleaning Pipeline ---")
    df_raw = load_data(raw_path)
    print(f"Loaded raw records: {len(df_raw)} rows")

    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)

    df_clean.to_csv(cleaned_path, index=False)
    print(f"Pipeline complete! Saved cleaned records ({len(df_clean)} rows) to:\n{cleaned_path}\n")
    
    print("Cleaning complete. First few rows:")
    print(df_clean.head())