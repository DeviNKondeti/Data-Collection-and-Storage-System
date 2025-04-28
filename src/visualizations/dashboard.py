import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from charts import ChartBuilder
from data_loader import DataLoader

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Data Collection Dashboard", className="text-center mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Select Dataset"),
            dcc.Dropdown(
                id='dataset-selector',
                options=[{'label': f, 'value': f} for f in DataLoader.get_available_files()],
                value=DataLoader.get_available_files()[0] if DataLoader.get_available_files() else None
            )
        ], width=6),
        
        dbc.Col([
            html.H3("Select Chart Type"),
            dcc.Dropdown(
                id='chart-type-selector',
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Pie Chart', 'value': 'pie'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='bar'
            )
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='main-chart'), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Data Summary"),
            html.Div(id='data-summary')
        ], width=12)
    ])
], fluid=True)

@app.callback(
    [Output('main-chart', 'figure'),
     Output('data-summary', 'children')],
    [Input('dataset-selector', 'value'),
     Input('chart-type-selector', 'value')]
)
def update_chart(selected_file, chart_type):
    if not selected_file:
        return {}, "No data available"
    
    # Load data based on file extension
    if selected_file.endswith('.json'):
        data = DataLoader.load_json_data(selected_file)
        df = pd.DataFrame(data)
    else:
        df = DataLoader.load_csv_data(selected_file)
    
    # Generate summary statistics
    summary = dbc.Card([
        dbc.CardHeader("Dataset Summary"),
        dbc.CardBody([
            html.P(f"Rows: {len(df)}"),
            html.P(f"Columns: {', '.join(df.columns)}"),
            html.P(f"Sample data:"),
            html.Pre(df.head().to_string())
        ])
    ])
    
    # Create appropriate chart
    if chart_type == 'bar' and len(df.columns) >= 2:
        fig = ChartBuilder.create_bar_chart(df, df.columns[0], df.columns[1])
    elif chart_type == 'line' and len(df.columns) >= 2:
        fig = ChartBuilder.create_time_series(df, df.columns[0], df.columns[1])
    elif chart_type == 'pie' and len(df.columns) >= 2:
        fig = ChartBuilder.create_pie_chart(df, df.columns[0], df.columns[1])
    elif chart_type == 'scatter' and len(df.columns) >= 2:
        color_col = df.columns[2] if len(df.columns) > 2 else None
        fig = ChartBuilder.create_scatter_plot(df, df.columns[0], df.columns[1], color_col)
    else:
        fig = {}
    
    return fig, summary

def run_dashboard(port=8050):
    app.run_server(port=port, debug=True)