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
            yaml.safe_dump({
                col: {
                    "source": "TBD",
                    "definition": "No definition provided",
                    "status": "added"
                } for col in df.columns
            }, file)

def get_example_values(column):
    info = {}
    if column.dtype == 'object':
        # Sample 5 random values from the column if possible
        sample_values = column.dropna().sample(min(5, len(column))).tolist()
        info['examples'] = ', '.join(str(v) for v in sample_values)
        info['categories'] = len(column.dropna().unique())
    elif column.dtype in ['int64', 'float64']:
        info['examples'] = ', '.join(str(v) for v in column.dropna().sample(min(5, len(column))).tolist())
        info['range'] = (column.min(), column.max())
    elif pd.api.types.is_datetime64_any_dtype(column):
        sample_values = column.dropna().sample(min(5, len(column)))
        info['examples'] = ', '.join(v.strftime('%Y-%m-%d') for v in sample_values)
        info['range'] = (column.min().strftime('%Y-%m-%d'), column.max().strftime('%Y-%m-%d'))
    else:
        info['examples'] = "N/A"
    return info

