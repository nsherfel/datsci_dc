import pandas as pd
from .utils import load_definitions, get_example_values, generate_initial_yaml

def generate_data_catalog(df, path_to_yaml=None, output_type='csv'):
    if path_to_yaml and not os.path.exists(path_to_yaml):
        generate_initial_yaml(df, path_to_yaml)
    elif not path_to_yaml:
        path_to_yaml = 'default_definitions.yaml'
        generate_initial_yaml(df, path_to_yaml)

    definitions = load_definitions(path_to_yaml)

    catalog = []
    for column in df.columns:
        example_values = get_example_values(df[column])
        column_info = get_column_info(df[column])
        data = {
            "Field Name": column,
            "Data Type": str(df[column].dtype),
            "Source": definitions.get(column, {}).get("source", "TBD"),
            "Definition": definitions.get(column, {}).get("definition", "No definition provided"),
            "Example Values": example_values,
            "Percent Null": f"{df[column].isnull().mean() * 100:.2f}%",
            "Statistics": column_info
        }
        
        catalog.append(data)
    
    catalog_df = pd.DataFrame(catalog)

    if output_type == 'markdown':
        return catalog_df.to_markdown(index=False)
    elif output_type == 'csv':
        return catalog_df.to_csv(index=False)
    else:
        raise ValueError("Unsupported output type. Use 'markdown' or 'csv'.")

    
    catalog_df = pd.DataFrame(catalog)

    if output_type == 'markdown':
        return catalog_df.to_markdown(index=False)
    elif output_type == 'csv':
        return catalog_df.to_csv(index=False)
    else:
        raise ValueError("Unsupported output type. Use 'markdown' or 'csv'.")


