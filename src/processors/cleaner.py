import pandas as pd
import numpy as np

class DataCleaner:
    @staticmethod
    def clean_dataframe(df, cleaning_rules):
        """Apply cleaning rules to dataframe"""
        # Handle missing values
        if 'missing_values' in cleaning_rules:
            for col, strategy in cleaning_rules['missing_values'].items():
                if strategy == 'drop':
                    df = df.dropna(subset=[col])
                elif strategy == 'fill':
                    fill_value = cleaning_rules['fill_values'].get(col, 0)
                    df[col] = df[col].fillna(fill_value)
        
        # Convert data types
        if 'dtype_conversion' in cleaning_rules:
            for col, dtype in cleaning_rules['dtype_conversion'].items():
                if col in df.columns:
                    try:
                        df[col] = df[col].astype(dtype)
                    except (ValueError, TypeError):
                        print(f"Could not convert {col} to {dtype}")
        
        # Standardize text
        if 'text_columns' in cleaning_rules:
            for col in cleaning_rules['text_columns']:
                if col in df.columns:
                    df[col] = df[col].str.strip().str.lower()
        
        return df