import pandas as pd
import numpy as np

def clean_stock_data(file_path):
    print(f"Loading data from: {file_path}")
    df = pd.read_csv(file_path)

    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    print("Standardized column names.")

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        print("Date column formatted and set as index.")
    else:
        print("Warning: 'date' column not found.")

    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - len(df)
    print(f"Removed {duplicates_removed} duplicate rows.")

    critical_columns = ['open', 'high', 'low', 'close', 'volume', 'adj_close']
    for col in critical_columns:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)

    missing_before = df.isna().sum().sum()
    df.fillna(method='ffill', inplace=True)
    
    df.dropna(inplace=True)
    missing_after = missing_before - df.isna().sum().sum()
    print(f"Handled missing values (filled/dropped {missing_before} nulls).")

    print(f"Data cleaning complete. Final dataset shape: {df.shape}")
    return df

if __name__ == "__main__":
    input_file = "raw_stock_data.csv"
    output_file = "cleaned_stock_data.csv"
    
    try:
        cleaned_df = clean_stock_data(input_file)
        
        cleaned_df.to_csv(output_file)
        print(f"Cleaned data successfully saved to {output_file}")
        
        print("\nCleaned Data Preview:")
        print(cleaned_df.head())
        
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")