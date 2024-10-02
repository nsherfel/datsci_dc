from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import yaml
from data_catalog.catalog_generator import generate_data_catalog
from data_catalog.utils import load_definitions, generate_initial_yaml, update_yaml_with_status

def edit_definitions(df, path_to_yaml=None):
    app = Dash(__name__)
    app.config.suppress_callback_exceptions = True

    if path_to_yaml:
        definitions = load_definitions(path_to_yaml)
        update_yaml_with_status(path_to_yaml)
    else:
        generate_initial_yaml(df, 'data_definitions.yaml')
        definitions = load_definitions('data_definitions.yaml')
    
    catalog_df = generate_data_catalog(df, path_to_yaml, output_type='df')
    
    columns_to_keep = ['Field Name', 'Data Type', 'Source', 'Definition', 'Status', 'Example Values', 'Percent Null', 'Statistics']
    catalog_df = catalog_df[columns_to_keep]
    
    # Set default value for Status if it's empty
    catalog_df['Status'] = catalog_df['Status'].fillna('to be added')

    app.layout = html.Div([
        dash_table.DataTable(
            id='data-catalog-table',
            columns=[
                {"name": i, "id": i, "editable": True if i in ['Source', 'Definition'] else False}
                for i in catalog_df.columns if i != 'Status'
            ] + [
                {"name": "Status", "id": "Status", "presentation": "dropdown"}
            ],
            data=catalog_df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            row_deletable=False,
            dropdown={
                'Status': {
                    'options': [
                        {'label': i, 'value': i}
                        for i in ['to be added', 'added', 'removed']
                    ]
                },
            },
            css=[{
                'selector': '.Select-menu-outer',
                'rule': 'display: block !important'
            }]
        ),
        html.Div([
            dcc.Input(id='new-column-name', type='text', placeholder='Enter new column name'),
            html.Button('Add Column', id='add-column-button', n_clicks=0),
        ]),
        html.Button('Save Changes', id='save-button', n_clicks=0),
        html.Div(id='save-confirm')
    ])

    @app.callback(
        Output('data-catalog-table', 'columns'),
        Output('data-catalog-table', 'data'),
        Input('add-column-button', 'n_clicks'),
        State('data-catalog-table', 'columns'),
        State('data-catalog-table', 'data'),
        State('new-column-name', 'value')
    )
    def add_column(n_clicks, existing_columns, existing_data, new_column_name):
        if n_clicks > 0 and new_column_name:
            existing_columns.append({"name": new_column_name, "id": new_column_name, "editable": True})
            for row in existing_data:
                row[new_column_name] = ''
        return existing_columns, existing_data

    @app.callback(
        Output('save-confirm', 'children'),
        Input('save-button', 'n_clicks'),
        State('data-catalog-table', 'data'),
        State('data-catalog-table', 'columns')
    )
    def update_definitions(n_clicks, rows, columns):
        if n_clicks > 0:
            new_definitions = {}
            for row in rows:
                field_name = row['Field Name']
                new_definitions[field_name] = {}
                for col in columns:
                    if col['name'] not in ['Field Name', 'Data Type', 'Example Values', 'Percent Null', 'Statistics']:
                        # Use lowercase keys for consistency
                        key = col['name'].lower()
                        new_definitions[field_name][key] = row.get(col['id'], '')
            
            with open(path_to_yaml, 'w') as file:
                yaml.safe_dump(new_definitions, file)
            return 'Changes saved!'
        return ''

    app.run_server(debug=False)
