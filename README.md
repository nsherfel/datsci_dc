# Data Catalog Management

This repository includes a Python module, `data_catalog`, that simplifies the creation and management of data catalogs for datasets, particularly useful in data analysis and machine learning projects.

## Features

- **Automated Data Catalog Creation:** Automatically generate a YAML data catalog from your dataset which contains essential metadata for each field.
- **Editable Definitions:** Utilize an interactive table to edit and define metadata for your dataset fields, ensuring clarity and consistency.
- **Flexible Output Formats:** Generate data catalog in different formats including DataFrame, Markdown, or CSV, catering to various documentation or analysis needs.

## How It Works

1. **Initial Setup:**
   - Import the required functions from the module:
     ```python
     from data_catalog import edit_definitions, generate_data_catalog
     ```

2. **Generate/Edit YAML File:**
   - The `generate_data_catalog` function reads your dataset and either creates a new YAML file or updates an existing one. This YAML file stores metadata definitions and can be edited directly or through an interactive table (`edit_definitions`).
     ```python
     catalog = generate_data_catalog(pd.read_csv('./dataset.csv'), path_to_yaml='data_definitions.yaml', output_type='markdown')
     ```

3. **View and Edit Metadata:**
   - Use the interactive `edit_definitions` table to easily modify metadata definitions. This tool provides a user-friendly interface to manage the details without directly editing the YAML file.

4. **Generate Catalog for Documentation:**
   - Convert the YAML metadata into a markdown format to include in your project's README or documentation, facilitating easy understanding and reference:
     ```python
     print(catalog)
     ```

## Output Options

- `df` (default): Generates a DataFrame that can be used with `edit_definitions` for an interactive metadata management experience.
- `markdown`: Useful for documentation purposes, can be directly included in Markdown files.
- `csv`: Provides a simple, flat file format that can be used for other forms of data handling or analysis.

## Additional Notes

- If the path to the YAML file is not defined, the system will create a default `data_definitions.yaml` file. If this file already exists, it will be used by default.
- The YAML file serves as a central definition store that can be revised through the `edit_definitions` interface, and these revisions are reflected when generating new outputs.
