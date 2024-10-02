from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import yaml
from catalog_generator import generate_data_catalog
from utils import load_definitions, generate_initial_yaml

def edit_definitions(df, path_to_yaml=None):
    app = Dash(__name__)
    if path_to_yaml:
        definitions = load_definitions(path_to_yaml)
    else:
        generate_initial_yaml(df, 'data_definitions.yaml')
        definitions = load_definitions('data_definitions.yaml')
    
    catalog_df = generate_data_catalog(df, path_to_yaml, output_type='df')
    
    # Add the Status column if it doesn't exist
    if 'Status' not in catalog_df.columns:
        catalog_df['Status'] = 'added'
    
    app.layout = html.Div([
        dash_table.DataTable(
            id='data-catalog-table',
            columns=[
                {"name": i, "id": i, "editable": True if i in ['Source', 'Definition'] else False}
                for i in catalog_df.columns if i != 'Status'
            ] + [
                {
                    "name": "Status",
                    "id": "Status",
                    "presentation": "dropdown"
                }
            ],
            data=catalog_df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            row_deletable=True,
            dropdown={
                'Status': {
                    'options': [
                        {'label': i, 'value': i}
                        for i in ['to be added', 'added', 'removed']
                    ]
                }
            }
        ),
        html.Button('Save Changes', id='save-button', n_clicks=0),
        html.Div(id='save-confirm')
    ])

    @app.callback(
        Output('save-confirm', 'children'),
        Input('save-button', 'n_clicks'),
        State('data-catalog-table', 'data')
    )
    def update_definitions(n_clicks, rows):
        if n_clicks > 0:
            new_definitions = {
                row['Field Name']: {
                    'source': row['Source'],
                    'definition': row['Definition'],
                    'status': row['Status']
                } for row in rows
            }
            with open(path_to_yaml, 'w') as file:
                yaml.safe_dump(new_definitions, file)
            return 'Changes saved!'
        return ''

    app.run_server(debug=True)
