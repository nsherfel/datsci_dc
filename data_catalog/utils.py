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

import pandas as pd

def get_example_values(column):
    # Sample up to 5 random values from the column, converting to string for consistency
    examples = column.dropna().sample(min(5, len(column))).tolist()
    return ', '.join(str(v) for v in examples)

