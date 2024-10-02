import pandas as pd
import os
from data_catalog.utils import load_definitions, get_example_values, generate_initial_yaml

def generate_data_catalog(df, path_to_yaml=None, output_type='df'):
    if path_to_yaml and not os.path.exists(path_to_yaml):
        generate_initial_yaml(df, path_to_yaml)
    elif not path_to_yaml:
        path_to_yaml = 'data_definitions.yaml'
        generate_initial_yaml(df, path_to_yaml)
    
    definitions = load_definitions(path_to_yaml)
    catalog = []
    
    for column in df.columns:
        existing_data = definitions.get(column, {})
        status = existing_data.get("status", "added")
        
        if status == "added":
            # Update statistics only for 'added' fields
            column_info = get_example_values(df[column])
            data = {
                "Field Name": column,
                "Data Type": str(df[column].dtype),
                "Source": existing_data.get("source", "TBD"),
                "Definition": existing_data.get("definition", "No definition provided"),
                "Example Values": column_info['examples'],
                "Percent Null": f"{df[column].isnull().mean() * 100:.2f}%",
                "Statistics": ', '.join([f"{k}: {', '.join(map(str, v))}" if isinstance(v, tuple) else f"{k}: {v}" for k, v in column_info.items() if k != 'examples']),
                "Status": status
            }
        else:
            # For non-'added' fields, use existing data without updating statistics
            data = {
                "Field Name": column,
                "Data Type": existing_data.get("data type", str(df[column].dtype)),
                "Source": existing_data.get("source", "TBD"),
                "Definition": existing_data.get("definition", "No definition provided"),
                "Example Values": existing_data.get("example values", "N/A"),
                "Percent Null": existing_data.get("percent null", "N/A"),
                "Statistics": existing_data.get("statistics", "N/A"),
                "Status": status
            }
        
        # Add any additional custom fields from the YAML file
        for key, value in existing_data.items():
            if key.lower() not in [k.lower() for k in data.keys()]:
                data[key] = value
        
        catalog.append(data)
    
    catalog_df = pd.DataFrame(catalog)
    
    if output_type == 'markdown':
        return catalog_df.to_markdown(index=False)
    elif output_type == 'csv':
        return catalog_df.to_csv(index=False)
    elif output_type == 'df':
        return catalog_df
    else:
        raise ValueError("Unsupported output type. Use 'markdown', 'csv', or 'df'.")
