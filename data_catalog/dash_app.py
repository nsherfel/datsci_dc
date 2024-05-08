from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from .catalog_generator import generate_data_catalog
from .utils import load_definitions, generate_initial_yaml

def run_server(df, path_to_yaml='definitions.yaml'):
    app = Dash(__name__)
    if path_to_yaml:
        definitions = load_definitions(path_to_yaml)
    else:
        generate_initial_yaml(df, 'definitions.yaml')
        definitions = load_definitions('definitions.yaml')

    catalog_df = generate_data_catalog(df, definitions)

    app.layout = html.Div([
        dash_table.DataTable(
            id='data-catalog-table',
            columns=[{"name": i, "id": i, "editable": True if i in ['Source', 'Definition'] else False} for i in catalog_df.columns],
            data=catalog_df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            row_deletable=True
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
            new_definitions = {row['Field Name']: {'source': row['Source'], 'definition': row['Definition']} for row in rows}
            with open(path_to_yaml, 'w') as file:
                yaml.safe_dump(new_definitions, file)
            return 'Changes saved!'
        return ''

    app.run_server(debug=True)
