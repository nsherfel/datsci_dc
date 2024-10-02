from dash import Dash, html, dcc, dash_table, callback_context
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
    
    catalog_df['Status'] = catalog_df['Status'].fillna('to be added')

    app.layout = html.Div([
        dash_table.DataTable(
            id='data-catalog-table',
            columns=[
                {"name": i, "id": i, "editable": True if i in ['Field Name', 'Source', 'Definition'] else False}
                for i in catalog_df.columns if i != 'Status'
            ] + [
                {"name": "Status", "id": "Status", "presentation": "dropdown"}
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
                },
            },
            css=[{
                'selector': '.Select-menu-outer',
                'rule': 'display: block !important'
            }]
        ),
        html.Div([
            dcc.Input(id='new-field-name', type='text', placeholder='Enter new field name'),
            html.Button('Add Row', id='add-row-button', n_clicks=0),
        ]),
        html.Div([
            dcc.Input(id='new-column-name', type='text', placeholder='Enter new column name'),
            html.Button('Add Column', id='add-column-button', n_clicks=0),
        ]),
        html.Button('Save Changes', id='save-button', n_clicks=0),
        html.Div(id='save-confirm'),
        dcc.Interval(id='auto-save-interval', interval=1000, n_intervals=0)  # Auto-save every 10 seconds
    ])

    @app.callback(
        Output('data-catalog-table', 'data'),
        Output('data-catalog-table', 'columns'),
        Input('add-row-button', 'n_clicks'),
        Input('add-column-button', 'n_clicks'),
        State('data-catalog-table', 'data'),
        State('data-catalog-table', 'columns'),
        State('new-field-name', 'value'),
        State('new-column-name', 'value')
    )
    def update_table(add_row_clicks, add_column_clicks, rows, columns, new_field_name, new_column_name):
        ctx = callback_context
        if not ctx.triggered:
            return rows, columns
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'add-row-button' and new_field_name:
            new_row = {col['id']: '' for col in columns}
            new_row['Field Name'] = new_field_name
            new_row['Status'] = 'to be added'
            rows.append(new_row)
        elif button_id == 'add-column-button' and new_column_name:
            columns.append({"name": new_column_name, "id": new_column_name, "editable": True})
            for row in rows:
                row[new_column_name] = ''
        
        return rows, columns

    @app.callback(
        Output('save-confirm', 'children'),
        Input('save-button', 'n_clicks'),
        Input('auto-save-interval', 'n_intervals'),
        Input('data-catalog-table', 'data'),
        Input('data-catalog-table', 'columns'),
        State('save-confirm', 'children')
    )
    def save_changes(manual_save_clicks, auto_save_intervals, rows, columns, previous_message):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if not ctx.triggered or (triggered_id == 'auto-save-interval' and previous_message == 'Auto-saved!'):
            return previous_message

        new_definitions = {}
        for row in rows:
            field_name = row['Field Name']
            new_definitions[field_name] = {}
            for col in columns:
                if col['name'] not in ['Field Name', 'Data Type', 'Example Values', 'Percent Null', 'Statistics']:
                    key = col['name'].lower()
                    new_definitions[field_name][key] = row.get(col['id'], '')
        
        with open(path_to_yaml, 'w') as file:
            yaml.safe_dump(new_definitions, file)
        
        if triggered_id == 'save-button':
            return 'Changes saved manually!'
        else:
            return 'Auto-saved!'

    app.run_server(debug=False)
