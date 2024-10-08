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
    
    # Process all fields in the YAML file, including those not in the DataFrame
    for field, field_info in definitions.items():
        data = {
            "Field Name": field,
            "Data Type": field_info.get("data type", "Unknown"),
            "Source": field_info.get("source", "TBD"),
            "Definition": field_info.get("definition", "No definition provided"),
            "Example Values": field_info.get("example values", "N/A"),
            "Percent Null": field_info.get("percent null", "N/A"),
            "Statistics": field_info.get("statistics", "N/A"),
            "Status": field_info.get("status", "added")
        }
        
        # If the field is in the DataFrame and has status 'added', update its statistics
        if field in df.columns and data["Status"] == "added":
            column_info = get_example_values(df[field])
            data.update({
                "Data Type": str(df[field].dtype),
                "Example Values": column_info['examples'],
                "Percent Null": f"{df[field].isnull().mean() * 100:.2f}%",
                "Statistics": ', '.join([f"{k}: {', '.join(map(str, v))}" if isinstance(v, tuple) else f"{k}: {v}" for k, v in column_info.items() if k != 'examples'])
            })
        
        # Add any additional custom fields from the YAML file
        for key, value in field_info.items():
            if key.lower() not in [k.lower() for k in data.keys()]:
                data[key] = value
        
        catalog.append(data)
    
    # Add any fields from the DataFrame that are not in the YAML file
    for column in df.columns:
        if column not in definitions:
            column_info = get_example_values(df[column])
            data = {
                "Field Name": column,
                "Data Type": str(df[column].dtype),
                "Source": "TBD",
                "Definition": "No definition provided",
                "Example Values": column_info['examples'],
                "Percent Null": f"{df[column].isnull().mean() * 100:.2f}%",
                "Statistics": ', '.join([f"{k}: {', '.join(map(str, v))}" if isinstance(v, tuple) else f"{k}: {v}" for k, v in column_info.items() if k != 'examples']),
                "Status": "added"
            }
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
