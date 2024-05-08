import pandas as pd
import os
from .utils import load_definitions, get_example_values, generate_initial_yaml

def generate_data_catalog(df, path_to_yaml=None, output_type='df'):
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
            "Percent Null": f"{df[column].isnull().mean() * 100:.2f}%",
            "Statistics": ', '.join([v for k, v in column_info.items() if k != 'examples'])
        }
        catalog.append(data)
    
    catalog_df = pd.DataFrame(catalog)

    # Ensure that the DataFrame is returned by default
    if output_type == 'markdown':
        return catalog_df.to_markdown(index=False)
    elif output_type == 'csv':
        return catalog_df.to_csv(index=False)
    elif output_type == 'df':
        return catalog_df  # This line ensures a DataFrame is returned
    else:
        raise ValueError("Unsupported output type. Use 'markdown', 'csv', or 'df'.")


