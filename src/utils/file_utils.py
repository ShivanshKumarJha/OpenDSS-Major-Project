import os
import pandas as pd

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Clean headers
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def ensure_directory(directory):
    os.makedirs(directory, exist_ok=True)