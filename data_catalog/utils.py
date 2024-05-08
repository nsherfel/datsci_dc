import yaml
import os
import pandas as pd

def load_definitions(path_to_yaml):
    if os.path.exists(path_to_yaml):
        with open(path_to_yaml, 'r') as file:
            definitions = yaml.safe_load(file)
    else:
        definitions = {}
    return definitions

def generate_initial_yaml(df, path_to_yaml):
    if not os.path.exists(path_to_yaml):
        with open(path_to_yaml, 'w') as file:
            yaml.safe_dump({col: {"source": "TBD", "definition": "No definition provided"} for col in df.columns}, file)

def get_example_values(column):
    info = {}
    if column.dtype == 'object':
        unique_values = column.dropna().unique()
        info['examples'] = ', '.join(str(v) for v in unique_values[:5])
        info['categories'] = len(unique_values)
    elif column.dtype in ['int64', 'float64']:
        info['examples'] = f"{column.min()} to {column.max()}"
        info['range'] = (column.min(), column.max())
    elif pd.api.types.is_datetime64_any_dtype(column):
        info['examples'] = f"{column.min().strftime('%Y-%m-%d')} to {column.max().strftime('%Y-%m-%d')}"
        info['range'] = (column.min(), column.max())
    else:
        info['examples'] = "N/A"
    return info
