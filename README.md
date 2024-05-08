# Data Catalog Management

This repository includes a Python module, `data_catalog`, that simplifies the creation and management of data catalogs for datasets, particularly useful in the initial phases of data analysis and machine learning projects.

## Features

- **Automated Data Catalog Creation:** Automatically generate a YAML data catalog from your dataset which contains essential metadata for each field.
- **Editable Definitions:** Utilize an interactive table to edit and define metadata for your dataset fields, ensuring clarity and consistency.
- **Flexible Output Formats:** Generate data catalog in different formats including DataFrame, Markdown, or CSV, catering to various documentation or analysis needs.

## How It Works

1. **Installation:**
   - To install the `data_catalog` module, use the following pip command:
     ```bash
     pip install git+https://github.com/nsherfel/datsci_dc.git
     ```

2. **Initial Setup:**
   - Import the required functions from the module:
     ```python
     from data_catalog import edit_definitions, generate_data_catalog
     ```

3. **Generate/Edit YAML File:**
   - The `generate_data_catalog` function reads your dataset and generates a YAML file. You can specify a custom name for the YAML file using the `path_to_yaml` parameter. If not specified, a default file named `data_definitions.yaml` is used or created.
     ```python
     df = pd.read_csv('./dataset.csv')
     catalog = generate_data_catalog(df, path_to_yaml='custom_definitions.yaml', output_type='markdown')
     ```
![Markdown Output Example](/images/markdown_output.png "Markdown Output Example")


4. **View and Edit Metadata:**
   - Use the interactive `edit_definitions` table to easily modify metadata definitions. This tool provides a user-friendly interface to manage the details without directly editing the YAML file. **Note**: Changes made using the UI table do not automatically save, users must click the 'save changes' button to save the changes.
![Edit Definitions Interface](/images/edit_definitions.png "Edit Definitions Interface")


5. **Generate Catalog for Documentation:**
   - Convert the YAML metadata into a markdown format to include in your project's README or documentation, facilitating easy understanding and reference:
     ```python
     print(catalog)
     ```

## Output Options

- `df` (default): Generates a DataFrame that can be used with `edit_definitions` for an interactive metadata management experience.
- `markdown`: Useful for documentation purposes, can be directly included in Markdown files.
- `csv`: Provides a simple, flat file format that can be used for other forms of data handling or analysis.

## Additional Notes

- The default YAML file, if not specified, will be named `data_definitions.yaml`. You can specify a custom file name using the `path_to_yaml` parameter.
- The YAML file serves as a central definition store that can be revised through the `edit_definitions` interface, and these revisions are reflected when generating new outputs.
