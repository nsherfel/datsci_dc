import pandas as pd
from .utils import load_definitions, get_example_values, generate_initial_yaml

def generate_data_catalog(df, path_to_yaml=None):
    if path_to_yaml and not os.path.exists(path_to_yaml):
        generate_initial_yaml(df, path_to_yaml)
    elif not path_to_yaml:
        path_to_yaml = 'default_definitions.yaml'
        generate_initial_yaml(df, path_to_yaml)

    definitions = load_definitions(path_to_yaml)

    catalog = []
    for column in df.columns:
        column_info = get_example_values(df[column])
        data = {
            "Field Name": column,
            "Data Type": str(df[column].dtype),
            "Source": definitions.get(column, {}).get("source", "TBD"),
            "Definition": definitions.get(column, {}).get("definition", "No definition provided"),
            "Example Values": column_info['examples'],
            "Percent Null": f"{df[column].isnull().mean() * 100:.2f}%"
        }
        if 'categories' in column_info:
            data["Number of Categories"] = column_info['categories']
        if 'range' in column_info:
            data["Range"] = f"{column_info['range'][0]} to {column_info['range'][1]}"
        catalog.append(data)
    return pd.DataFrame(catalog)
