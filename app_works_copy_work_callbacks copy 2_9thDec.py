import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table
from file_parsers_25thNov_copy import parse_contents , parse_contents_YT06, parse_contents_YT07 , parse_contents_YT01_805
import os
import pandas as pd
import webbrowser

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home", style={'font-size': '1.5em', 'color': 'white'})),
        dbc.NavItem(dbc.NavLink("Upload", id="upload-link", href="/upload", style={'font-size': '1.5em', 'color': 'white'})),
        dbc.NavItem(dbc.NavLink("TP History", href="/historical-data", style={'font-size': '1.5em', 'color': 'white'})),
    ],
    brand=html.Div([
        html.Img(src="https://my.shell.com/:i:/r/personal/shraddha_mishra_shell_com/Documents/CANADA/Pydash%20UI/Pecten%20-%20colour%20with%20white%20outline.png?csf=1&web=1&e=MPVNUy", style={'height': '75px', 'margin-top': '-6px'}),  # icon height        
        # html.H3("TRANSFER PRICING PORTAL", style={'color': 'white', 'margin-left': '9px'})
        html.H3("TRANSFER PRICING PORTAL", style={'color': 'white', 'margin-left': '9px', 'margin-right': '30px'})

    ], style={'display': 'flex', 'align-items': 'center'}),
    brand_href="/home",
    color="dark",
    dark=True,
    brand_style={'position': 'absolute', 'left': '50%', 'transform': 'translateX(-50%)', 'color': 'white', 'font-size': '2.0em'}
)

# Home Page Layout with Image and Objective
home_layout = html.Div([
    navbar,
    html.Div([
        html.Img(src="https://my.shell.com/:i:/r/personal/shraddha_mishra_shell_com/Documents/CANADA/Pydash%20UI/LNGOutlook_UK.JPG", 
                 style={'max-width': '100%', 'max-height': '70vh', 'display': 'block', 'margin': 'auto', 'margin-bottom': '20px', 'width': '90%'}),
    ]),
    html.H1("Objective", style={'font-size': '30px','text-align': 'center', 'color': 'white', 'width': '80%', 'margin': 'auto'}),
    html.Div([
        html.P(html.B("Welcome to Ezee-TP."), style={'color': 'white', 'font-size': '20px'}),
        html.P("This is a tool that makes your Transfer Price updates simpler. At present, this tool is designed for Malaysia.", style={'color': 'white', 'font-size': '18px'}),
        html.P(html.B("How to use:"), style={'color': 'white', 'font-size': '20px'}),
        html.P("Please upload the YT01 GSAP file. Paste the latest TP in the respective tabs here: GSCF Digital Portal - Input - All Documents (shell.com)", style={'color': 'white', 'font-size': '18px'}),
        html.P("Click Run", style={'color': 'white', 'font-size': '18px'}),
        html.P("Download the output file, and use it to upload it back to GSAP.", style={'color': 'white', 'font-size': '18px'}),
        ], style={'margin-top': '20px', 'text-align': 'left', 'color': 'white', 'width': '80%', 'margin': 'auto'})
    ], style={'background-color': '#1e2732', 'color': 'white'})


upload_layout = html.Div([
    navbar,
    html.Div([
        html.H1("Please upload the required files below, then click the generate report button and download buttons to generate and download the new transfer prices.", style={
            'font-size': '18px',
            'text-align': 'center',
            'margin-top': '20px',
            'color': 'white',
            'font-weight': 'bold'
        }),
        # Dropdowns
        html.Div([
            dcc.Dropdown(
                id='Country',
                options=[
                    {'label': 'Malaysia', 'value': 'Malaysia'},
                    {'label': 'Canada', 'value': 'Canada'}
                ],
                placeholder="Country",
                value=None,  # Remove the default value
                style={'margin-top': '20px', 'margin-bottom': '5px', 'width': '200px', 'font-size': '17px'}
            ),
            dcc.Dropdown(
                id='Report Type',
                options=[
                    {'label': 'YT01 800', 'value': 'YT01 800'},
                    {'label': 'YT01 805', 'value': 'YT01 805'},
                    {'label': 'YT01 600', 'value': 'YT01 600'},
                    {'label': 'YT06', 'value': 'YT06'},
                    {'label': 'YT07', 'value': 'YT07'},
                ],
                placeholder="Report Type",
                value=None,  # Remove the default value
                style={'margin-top': '20px', 'margin-bottom': '5px', 'width': '200px', 'font-size': '17px'}
            )
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),
        
        html.Div(id='upload-container', children=[
            html.Div([
                dcc.Upload(
                    id='upload-data-1',
                    children=html.Div('GSAP Report', style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                    style={
                        'flex': '1',
                        'height': '50px',
                        'lineHeight': '50px',
                        'border': '3px solid white',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'black',
                        'cursor': 'pointer',
                        'display': 'inline-block'
                    },
                    multiple=False
                ),
                dbc.Progress(id='progress-bar-1', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
                html.Span(id='upload-status-1', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
            ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'}),
            
            html.Div([
                dcc.Upload(
                    id='upload-data-2',
                    children=html.Div('Depot/Plant Mapping File', style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                    style={
                        'flex': '1',
                        'height': '50px',
                        'lineHeight': '50px',
                        'border': '3px solid white',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'black',
                        'cursor': 'pointer',
                        'display': 'inline-block'
                    },
                    multiple=False
                ),
                dbc.Progress(id='progress-bar-2', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
                html.Span(id='upload-status-2', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
            ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'}),
            
            html.Div([
                dcc.Upload(
                    id='upload-data-3',
                    children=html.Div('New TP Price Ref File', style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                    style={
                        'flex': '1',
                        'height': '50px',
                        'lineHeight': '50px',
                        'border': '3px solid white',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'black',
                        'cursor': 'pointer',
                        'display': 'inline-block'
                    },
                    multiple=False
                ),
                dbc.Progress(id='progress-bar-3', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
                html.Span(id='upload-status-3', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
            ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'})
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px', 'flex-wrap': 'wrap'}),
        
        # Buttons for running the script and downloading the file
        html.Div([
            dbc.Button("Click To Generate Transfer Price Report", id="run-script-button", color="primary", style={'font-size': '18px', 'font-weight': 'bold', 'margin-right': '10px'}),
            dbc.Button("Download Output File", id="download-button", color="success", style={'font-size': '18px', 'font-weight': 'bold', 'margin-right': '10px'}, disabled=True),
            dcc.Download(id="download-file")
        ], style={'text-align': 'center', 'margin-top': '20px'}),

        html.Div(id='output-data-upload', style={
            'color': 'white',
            'text-align': 'center',
            'margin-top': '20px',
            'padding': '20px',
            'border': '1px solid #ccc',
            'border-radius': '10px',
            'font-size': '16px',
            'background-color': '#F9C80E',
            'margin-left': '20px',
            'margin-right': '20px',
            'padding-left': '20px',
            'padding-right': '20px'
        })

    ], style={
        'padding': '40px',
        'border-radius': '10px',
        'width': '90%',
        'margin': 'auto',
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    })
])

@app.callback(
    Output('upload-container', 'children'),
    [Input('Country', 'value'),
     Input('Report Type', 'value')]
)
def update_upload_buttons(country, report_type):
    print(f"update_upload_buttons called with country={country}, report_type={report_type}")
    
    # Define default labels
    label_1 = 'GSAP Report'
    label_2 = 'Depot/Plant Mapping File'
    label_3 = 'New TP Price Ref File'
    label_4 = 'Quotation Codes Mapping'
    
    # Update labels based on country and report type
    if country == 'Malaysia':
        if report_type == 'YT06':
            label_1 = 'MY05 Additive Cost'
            label_2 = 'MY08 Additive Cost'
        elif report_type == 'YT07':
            label_1 = 'MY05 PT Update'
            label_2 = 'MY08 PT Update'
        elif report_type in ['YT01 800', 'YT01 805', 'YT01 600']:
            label_1 = 'Upload TP File'
            label_2 = 'Quotation Codes Mapping'
            label_4 = 'Depot/Plant Mapping File'
    elif country == 'Canada':
        if report_type == 'YT01 805':  
            label_1 = 'Lines_mappingfile'
            label_2 = 'TPValue_mappingfile'
            label_3 = 'GSAP Data File'
            label_4 = 'Combined Data File'
        
        
    upload_buttons = [
        html.Div([
            dcc.Upload(
                id='upload-data-1',
                children=html.Div(label_1, style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                style={
                    'flex': '1',
                    'height': '50px',
                    'lineHeight': '50px',
                    'border': '3px solid white',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': 'black',
                    'cursor': 'pointer',
                    'display': 'inline-block'
                },
                multiple=False
            ),
            dbc.Progress(id='progress-bar-1', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
            html.Span(id='upload-status-1', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
        ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'}),
        
        html.Div([
            dcc.Upload(
                id='upload-data-2',
                children=html.Div(label_2, style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                style={
                    'flex': '1',
                    'height': '50px',
                    'lineHeight': '50px',
                    'border': '3px solid white',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': 'black',
                    'cursor': 'pointer',
                    'display': 'inline-block'
                },
                multiple=False
            ),
            dbc.Progress(id='progress-bar-2', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
            html.Span(id='upload-status-2', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
        ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'}),
        
        html.Div([
            dcc.Upload(
                id='upload-data-3',
                children=html.Div(label_3, style={'padding': '0 20px', 'font-size': '18px', 'font-weight': 'bold', 'color': 'black'}),
                style={
                    'flex': '1',
                    'height': '50px',
                    'lineHeight': '50px',
                    'border': '3px solid white',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': 'black',
                    'cursor': 'pointer',
                    'display': 'inline-block'
                },
                multiple=False
            ),
            dbc.Progress(id='progress-bar-3', value=0, striped=True, animated=True, color='info', style={'height': '20px', 'margin': '20px'}),
            html.Span(id='upload-status-3', children='Not Uploaded', style={'margin': '10px', 'color': 'black', 'font-size': '20px'}),
        ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'})
    ]

    if not (country == "Malaysia" and report_type in ["YT06"]):
        upload_buttons.append(
            html.Div([
                dcc.Upload(
                    id="upload-data-4",
                    children=html.Div(label_4, style={"padding": "0 20px", "font-size": "18px", "font-weight": "bold", "color": "black"}),
                    style={
                        "flex": "1",
                        "height": "50px",
                        "lineHeight": "50px",
                        "border": "3px solid white",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "color": "black",
                        "cursor": "pointer",
                        "display": "inline-block"
                    },
                    multiple=False
                ),
                dbc.Progress(id="progress-bar-4", value=0, striped=True, animated=True, color="info", style={"height": "20px", "margin": "20px"}),
                html.Span(id="upload-status-4", children="Not Uploaded", style={"margin": "10px", "color": "black", "font-size": "20px"}),
            ], style={"background-color": "#F9C80E", "padding": "40px", "border-radius": "20px", "margin-top": "40px", "margin-bottom": "20px", "border": "1px solid black"})
        )

    return upload_buttons

# -----------------------------------------------
@app.callback(
    [Output('progress-bar-1', 'value'),
     Output('progress-bar-2', 'value'),
     Output('progress-bar-3', 'value'),
     Output('upload-status-1', 'children'),
     Output('upload-status-2', 'children'),
     Output('upload-status-3', 'children')],
    [Input('upload-data-1', 'contents'),
     Input('upload-data-2', 'contents'),
     Input('upload-data-3', 'contents'),
     Input('Report Type', 'value')],
    [State('upload-data-1', 'filename'),
     State('upload-data-2', 'filename'),
     State('upload-data-3', 'filename')]
)
def update_progress_bars(contents1, contents2, contents3, report_type, filename1, filename2, filename3):
    # print(f"update_progress_bars called with contents1={contents1}, contents2={contents2}, contents3={contents3}, report_type={report_type}")
    progress_values = [0, 0, 0]
    upload_status = ['Not Uploaded', 'Not Uploaded', 'Not Uploaded']

    if contents1:
        progress_values[0] = 100
        upload_status[0] = 'Uploaded'
    if contents2:
        progress_values[1] = 100
        upload_status[1] = 'Uploaded'
    if contents3:
        progress_values[2] = 100
        upload_status[2] = 'Uploaded'

    if report_type in ["YT01 800", "YT01 805", "YT01 600", "YT07"]:
        print("Report type is YT01 800, YT01 805, YT01 600, YT07")
        return (
            progress_values[0], progress_values[1], progress_values[2],
            upload_status[0], upload_status[1], upload_status[2]
        )
    elif report_type in ["YT06"]:
        print("Report type is YT06 ")
        return (
            progress_values[0], progress_values[1], progress_values[2],
            upload_status[0], upload_status[1], upload_status[2]
        )
    else:
        return (
            progress_values[0], progress_values[1], progress_values[2],
            upload_status[0], upload_status[1], upload_status[2]
        )
    
# @app.callback(
#     [Output('progress-bar-1', 'value'),
#      Output('progress-bar-2', 'value'),
#      Output('progress-bar-3', 'value'),
#      Output('progress-bar-4', 'value'),
#      Output('upload-status-1', 'children'),
#      Output('upload-status-2', 'children'),
#      Output('upload-status-3', 'children'),
#      Output('upload-status-4', 'children')],
#     [Input('upload-data-1', 'contents'),
#      Input('upload-data-2', 'contents'),
#      Input('upload-data-3', 'contents'),
#      Input('upload-data-4', 'contents'),
#      Input('Report Type', 'value')],
#     [State('upload-data-1', 'filename'),
#      State('upload-data-2', 'filename'),
#      State('upload-data-3', 'filename'),
#      State('upload-data-4', 'filename')]
# )
# def update_progress_bars(contents1, contents2, contents3, contents4, report_type, filename1, filename2, filename3, filename4):
#     progress_values = [0, 0, 0, 0]
#     upload_status = ['Not Uploaded', 'Not Uploaded', 'Not Uploaded', 'Not Uploaded']

#     if contents1:
#         progress_values[0] = 100
#         upload_status[0] = 'Uploaded'
#     if contents2:
#         progress_values[1] = 100
#         upload_status[1] = 'Uploaded'
#     if contents3:
#         progress_values[2] = 100
#         upload_status[2] = 'Uploaded'
#     if contents4:
#         progress_values[3] = 100
#         upload_status[3] = 'Uploaded'

#     if report_type in ["YT01 800", "YT01 805", "YT01 600", "YT07"]:
#         print("Report type is YT01 800, YT01 805, YT01 600, YT07")
#         return (
#             progress_values[0], progress_values[1], progress_values[2], progress_values[3],
#             upload_status[0], upload_status[1], upload_status[2], upload_status[3]
#         )
#     elif report_type in ["YT06"]:
#         print("Report type is YT06 ")
#         return (
#             progress_values[0], progress_values[1], progress_values[2], progress_values[3],
#             upload_status[0], upload_status[1], upload_status[2], upload_status[3]
#         )
#     else:
#         return (
#             progress_values[0], progress_values[1], progress_values[2], progress_values[3],
#             upload_status[0], upload_status[1], upload_status[2], upload_status[3]
#         )

tp_template_global = None

@app.callback(
    [Output('output-data-upload', 'children'),
     Output('download-button', 'disabled')],
    [Input('run-script-button', 'n_clicks')],
    [State('upload-data-1', 'contents'),
     State('upload-data-2', 'contents'),
     State('upload-data-3', 'contents'),
     State('upload-data-4', 'contents'),
     State('upload-data-1', 'filename'),
     State('upload-data-2', 'filename'),
     State('upload-data-3', 'filename'),
     State('upload-data-4', 'filename'),
     State('Country', 'value'),
     State('Report Type', 'value')]
)
def run_script(n_clicks, contents1, contents2, contents3, contents4, filename1, filename2, filename3, filename4, country, report_type):
    global tp_template_global  # Declare the global variable
    if n_clicks is None:
        return html.Div(['Preview of the updated Transfer Prices']), True

    output_div = None
    output_df = None
    tp_template = None
    YT06_output_div = None
    MY05_additivecost = None
    MY08_additivecost = None
    YT07_output_div = None
    MY05_PTUpdate = None
    MY08_PTUpdate = None

    try:
        if country == "Malaysia" and report_type == "YT06":
            if contents1 and contents2 and contents3:
                YT06_output_div, MY05_additivecost, MY08_additivecost = parse_contents_YT06(contents1, filename1, contents2, filename2, contents3, filename3)
            else:
                raise ValueError("Three files are required for YT06 report type")
            
        if country == "Malaysia" and report_type == "YT07":
            if contents1 and contents2 and contents3 and contents4:
                YT07_output_div, MY05_PTUpdate, MY08_PTUpdate = parse_contents_YT07(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
            else:
                raise ValueError("Four files are required for YT07 report type")
            
        elif country == "Malaysia" and report_type in ["YT01 800", "YT01 805", "YT01 600"]:
            print("Using parse_contents yt01 800")
            if contents1 and contents2 and contents3 and contents4:
                # output_div, output_df, tp_template = parse_contents(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
                output_div, output_df, tp_template = parse_contents(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
            else:
                raise ValueError("Four files are required for 800, 805, and 600 report types")
        
        elif country == "Canada" and report_type in ["YT01 805", "YT01 800", "YT01 611"]:
            if contents1 and contents2 and contents3 and contents4:
                output_div, output_df = parse_contents_YT01_805(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
                print(f"output_df for YT01 805 Canada: {output_df}")
            else:
                raise ValueError("Four files are required for Canada 800, 805, and 600 report types")
       
        else:
            raise ValueError("Unsupported country or report type")

        # Check if output_df is a DataFrame (for parse_contents)
        if output_df is not None and isinstance(output_df, pd.DataFrame):
            print("4 inside try ")
            print(f"output_df contents: {output_df.head()}")

            # Get the path to the Desktop folder
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            output_path = os.path.join(desktop_path, 'tp_my_test.xlsx')
            print(f"Saving DataFrame to: {output_path}")
            # Save the output DataFrame to a file
            output_df.to_excel(output_path, index=False)
            print("800, 805, 600 file saved successfully.")

            # Create a table to display the DataFrame
            output_div = dash_table.DataTable(
                data=output_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in output_df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'color': 'black'},
                page_size=10
            )
        
        # Check if MY05_additivecost and MY08_additivecost are DataFrames (for parse_contents_YT06)
        if MY05_additivecost is not None and MY08_additivecost is not None:

            if isinstance(MY05_additivecost, pd.DataFrame) and isinstance(MY08_additivecost, pd.DataFrame):

                # Get the path to the Desktop folder
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                output_path = os.path.join(desktop_path, 'YT06_cost_update.xlsx')
                print(f"Saving DataFrames to: {output_path}")
                # Write to Excel with different sheets
                with pd.ExcelWriter(output_path) as writer:
                    MY08_additivecost.to_excel(writer, sheet_name='MY08', index=False)
                    MY05_additivecost.to_excel(writer, sheet_name='MY05', index=False)
                print("YT06 output file saved successfully.")

                # Create tables to display the DataFrames
                YT06_output_div = html.Div([
                    html.H4('MY08 Additive Cost'),
                    dash_table.DataTable(
                        data=MY08_additivecost.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in MY08_additivecost.columns],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'color': 'black'},
                        page_size=10
                    ),
                    html.H4('MY05 Additive Cost'),
                    dash_table.DataTable(
                        data=MY05_additivecost.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in MY05_additivecost.columns],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'color': 'black'},
                        page_size=10
                    )
                ])

        # Check if MY05_PTUpdate and MY08_PTUpdate are DataFrames (for parse_contents_YT07)
        if MY05_PTUpdate is not None and MY08_PTUpdate is not None:

            if isinstance(MY05_PTUpdate, pd.DataFrame) and isinstance(MY08_PTUpdate, pd.DataFrame):

                # Get the path to the Desktop folder
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                output_path = os.path.join(desktop_path, 'YT07_cost_update.xlsx')
                print(f"Saving DataFrames to: {output_path}")
                # Write to Excel with different sheets
                with pd.ExcelWriter(output_path) as writer:
                    MY05_PTUpdate.to_excel(writer, sheet_name='MY05', index=False)
                    MY08_PTUpdate.to_excel(writer, sheet_name='MY08', index=False)
                print("YT07 output file saved successfully.")

                # Create tables to display the DataFrames
                YT07_output_div = html.Div([
                    html.H4('MY05 PT Update'),
                    dash_table.DataTable(
                        data=MY05_PTUpdate.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in MY05_PTUpdate.columns],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'color': 'black'},
                        page_size=10
                    ),
                    html.H4('MY08 PT Update'),
                    dash_table.DataTable(
                        data=MY08_PTUpdate.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in MY08_PTUpdate.columns],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'color': 'black'},
                        page_size=10
                    )
                ])

        # Update the global variable
        tp_template_global = tp_template
        print(f"tp_template_global updated: {tp_template_global}")

    except Exception as e:
        print("inside run_script except")
        print(f"Error in run_script: {e}")
        return html.Div([f"Error in run_script: {e}"]), True

    # Return the appropriate output based on the report type
    if report_type == "YT06":
        return YT06_output_div, False
    elif report_type == "YT07":
        return YT07_output_div, False
    else:
        return output_div, False
    
# @app.callback(
#     [Output('output-data-upload', 'children'),
#      Output('download-button', 'disabled')],
#     [Input('run-script-button', 'n_clicks')],
#     [State('upload-data-1', 'contents'),
#      State('upload-data-2', 'contents'),
#      State('upload-data-3', 'contents'),
#      State('upload-data-4', 'contents'),
#      State('upload-data-1', 'filename'),
#      State('upload-data-2', 'filename'),
#      State('upload-data-3', 'filename'),
#      State('upload-data-4', 'filename'),
#      State('Country', 'value'),
#      State('Report Type', 'value')]
# )
# def run_script(n_clicks, contents1, contents2, contents3, contents4, filename1, filename2, filename3, filename4, country, report_type):
#     global tp_template_global  # Declare the global variable
#     print("1 inside run script")

#     if n_clicks is None:
#         print("2 inside run script")
#         return html.Div(['Preview of the updated Transfer Prices']), True

#     # Initialize variables
#     output_div = None
#     output_df = None
#     tp_template = None
#     YT06_output_div = None
#     MY05_additivecost = None
#     MY08_additivecost = None
#     YT07_output_div = None
#     MY05_PTUpdate = None
#     MY08_PTUpdate = None

#     try:
#         print("3 inside try")

#         # Determine which parse_contents function to use based on country and report type
#         if country == "Malaysia" and report_type == "YT06":
#             print("Using parse_contents_YT06")
#             if contents1 and contents2 and contents3:
#                 YT06_output_div, MY05_additivecost, MY08_additivecost = parse_contents_YT06(contents1, filename1, contents2, filename2, contents3, filename3)
#             else:
#                 raise ValueError("Three files are required for YT06 report type")
            
#         if country == "Malaysia" and report_type == "YT07":
#             print("Using parse_contents_YT07")
#             if contents1 and contents2 and contents3 and contents4:
#                 YT07_output_div, MY05_PTUpdate, MY08_PTUpdate = parse_contents_YT07(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
#             else:
#                 raise ValueError("Four files are required for YT07 report type")
        
            
#         elif country == "Malaysia" and report_type in ["YT01 800", "YT01 805", "YT01 600"]:
#             print("Using parse_contents yt01 800")
#             if contents1 and contents2 and contents3 and contents4:
#                 output_div, output_df, tp_template = parse_contents(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
#             else:
#                 raise ValueError("Four files are required for 800, 805, and 600 report types")
        
#         elif country == "Canada" and report_type in ["YT01 805", "YT01 800", "YT01 611"]:
#             print("Using parse_contents yt01 805")
#             if contents1 and contents2 and contents3 and contents4:
#                 print('runnning Canaada parsefunction')
#                 output_div, output_df = parse_contents_YT01_805(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4)
#             else:
#                 raise ValueError("Four files are required for Canada 800, 805, and 600 report types")
        
#         else:
#             raise ValueError("Unsupported country or report type")

#         # Check if output_df is a DataFrame (for parse_contents)
#         if output_df is not None and isinstance(output_df, pd.DataFrame):
#             print("4 inside try ")

#             # Get the path to the Desktop folder
#             desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#             output_path = os.path.join(desktop_path, 'tp_my_test.xlsx')
#             print(f"Saving DataFrame to: {output_path}")
#             # Save the output DataFrame to a file
#             output_df.to_excel(output_path, index=False)
#             print("800, 805, 600 file saved successfully.")

#             # Create a table to display the DataFrame
#             output_div = dash_table.DataTable(
#                 data=output_df.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in output_df.columns],
#                 style_table={'overflowX': 'auto'},
#                 style_cell={'textAlign': 'left', 'color': 'black'},
#                 page_size=10
#             )
        
#         # Check if MY05_additivecost and MY08_additivecost are DataFrames (for parse_contents_YT06)
#         if MY05_additivecost is not None and MY08_additivecost is not None:

#             if isinstance(MY05_additivecost, pd.DataFrame) and isinstance(MY08_additivecost, pd.DataFrame):

#                 # Get the path to the Desktop folder
#                 desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#                 output_path = os.path.join(desktop_path, 'YT06_cost_update.xlsx')
#                 print(f"Saving DataFrames to: {output_path}")
#                 # Write to Excel with different sheets
#                 with pd.ExcelWriter(output_path) as writer:
#                     MY08_additivecost.to_excel(writer, sheet_name='MY08', index=False)
#                     MY05_additivecost.to_excel(writer, sheet_name='MY05', index=False)
#                 print("YT06 output file saved successfully.")

#                 # Create tables to display the DataFrames
#                 YT06_output_div = html.Div([
#                     html.H4('MY08 Additive Cost'),
#                     dash_table.DataTable(
#                         data=MY08_additivecost.to_dict('records'),
#                         columns=[{'name': i, 'id': i} for i in MY08_additivecost.columns],
#                         style_table={'overflowX': 'auto'},
#                         style_cell={'textAlign': 'left', 'color': 'black'},
#                         page_size=10
#                     ),
#                     html.H4('MY05 Additive Cost'),
#                     dash_table.DataTable(
#                         data=MY05_additivecost.to_dict('records'),
#                         columns=[{'name': i, 'id': i} for i in MY05_additivecost.columns],
#                         style_table={'overflowX': 'auto'},
#                         style_cell={'textAlign': 'left', 'color': 'black'},
#                         page_size=10
#                     )
#                 ])

#         # Check if MY05_PTUpdate and MY08_PTUpdate are DataFrames (for parse_contents_YT07)
#         if MY05_PTUpdate is not None and MY08_PTUpdate is not None:

#             if isinstance(MY05_PTUpdate, pd.DataFrame) and isinstance(MY08_PTUpdate, pd.DataFrame):

#                 # Get the path to the Desktop folder
#                 desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
#                 output_path = os.path.join(desktop_path, 'YT07_cost_update.xlsx')
#                 print(f"Saving DataFrames to: {output_path}")
#                 # Write to Excel with different sheets
#                 with pd.ExcelWriter(output_path) as writer:
#                     MY05_PTUpdate.to_excel(writer, sheet_name='MY05', index=False)
#                     MY08_PTUpdate.to_excel(writer, sheet_name='MY08', index=False)
#                 print("YT07 output file saved successfully.")

#                 # Create tables to display the DataFrames
#                 YT07_output_div = html.Div([
#                     html.H4('MY05 PT Update'),
#                     dash_table.DataTable(
#                         data=MY05_PTUpdate.to_dict('records'),
#                         columns=[{'name': i, 'id': i} for i in MY05_PTUpdate.columns],
#                         style_table={'overflowX': 'auto'},
#                         style_cell={'textAlign': 'left', 'color': 'black'},
#                         page_size=10
#                     ),
#                     html.H4('MY08 PT Update'),
#                     dash_table.DataTable(
#                         data=MY08_PTUpdate.to_dict('records'),
#                         columns=[{'name': i, 'id': i} for i in MY08_PTUpdate.columns],
#                         style_table={'overflowX': 'auto'},
#                         style_cell={'textAlign': 'left', 'color': 'black'},
#                         page_size=10
#                     )
#                 ])
        
#         # Update the global variable
#         tp_template_global = tp_template
#         print(f"tp_template_global updated: {tp_template_global}")

#     except Exception as e:
#         print("inside run_script except")
#         print(f"Error in run_script: {e}")
#         return html.Div([f"Error in run_script: {e}"]), True

#     # Return the appropriate output based on the report type
#     if report_type == "YT06":
#         return YT06_output_div, False
#     elif report_type == "YT07":
#         return YT07_output_div, False
#     else:
#         return output_div, False

# ----------------------------------------------------------------------
historical_data_layout = html.Div([
    navbar,
    html.H1(" Click the below tabs to see its past Transfer Price data. ", style={
        'font-size': '18px',
        'text-align': 'center',
        'margin-top': '35px',
        'color': 'white',
        'font-weight': 'bold'
    }),

    # Add the dropdown for country selection
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[
                {'label': 'Malaysia', 'value': 'Malaysia'},
                {'label': 'Canada', 'value': 'Canada'}
            ],
            placeholder="Country",
            style={'margin-top': '20px', 'margin-bottom': '5px', 'width': '200px', 'font-size': '17px'}
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),

    html.Div([ 
        dcc.Tabs(id='tabs', value=None, children=[], style={'color': 'black', 'fontWeight': 'bold'}),
        html.Div(id='tabs-content', style={
            'background-color': '#1e2732', 
            'padding': '20px',             
            'border-radius': '10px',
            'margin-top': '15px'           
        })
    ], style={'background-color': '#1e2732', 'border-radius': '20px'})  
], style={'background-color': '#1e2732', 'color': '#1e2732'}) 


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def update_tab(tab_name):
    print('TAB_NAME', tab_name)
    global tp_template_global  

    if tp_template_global:
        dfs = {}
        for sheet, data in tp_template_global.items():

            print(f"Processing sheet: {sheet}")
            df = pd.DataFrame(data)
            print(f"DataFrame for {sheet} created with columns: {df.columns}")
            if 'Period' in df.columns:
                df['Period'] = pd.to_datetime(df['Period']).dt.date
                cols = ['Period'] + [col for col in df.columns if col != 'Period']
                df = df[cols]
                print(f"'Period' column moved to first position in {sheet}")
            dfs[sheet] = df

        # print('TAB_NAME', tab_name)
        df = dfs.get(tab_name, pd.DataFrame())

        if df.empty:
            print(f"No data available for tab: {tab_name}")
            return html.Div("Select a Country option in dropdown menu than select individual material tab to display its historical TP values.", style={'color': 'white'})

        print(f"Displaying data for tab: {tab_name}")
        return dash_table.DataTable(
            id='historical-data-table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
    else:
        print("tp_template is None or empty")
        return html.Div("This page will display the historical transfer price values of different Countries.", style={'color': 'white'})
  
@app.callback(
    [Output('tabs', 'children')],
    Input('country-dropdown', 'value')  # Use the unique ID here
)
def update_tabs(selected_country):
    global tp_template_global  # Declare the global variable

    if selected_country != 'Malaysia':
        return [[]]

    print(f"Country selected: {selected_country}")

    if tp_template_global:
        sheet_names = list(tp_template_global.keys())
        print(f"Sheet names: {sheet_names}")
        tabs = [
            dcc.Tab(
                label=sheet_name, 
                value=sheet_name, 
                style={'color': 'black', 'fontWeight': 'bold'},  # Make text bold
                selected_style={'color': 'Brown', 'fontWeight': 'bold'}  # Bold for the selected tab as well
            ) for sheet_name in sheet_names
        ]
        print(f"Tabs created: {tabs}")
        return [tabs]
    return [[]]

@app.callback(
    Output('download-file', 'data'),
    [Input('download-button', 'n_clicks')]
)
def download_file(n_clicks):
    if n_clicks:
        # Get the path to the Desktop folder
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        output_path = os.path.join(desktop_path, 'New_Transferprice_report.xlsx')
        # print(output_path)
        if os.path.exists(output_path):
            return dcc.send_file(output_path)
        else:
            default_output_path = os.path.join(desktop_path, 'tp_my_test.xlsx')
            if os.path.exists(default_output_path):
                return dcc.send_file(default_output_path)
            else:
                return dcc.send_data_frame(pd.DataFrame().to_excel, "tp_my_test.xlsx")

            # Handle the case where the default file does not exist
            # default_output_path = os.path.join(desktop_path, 'default_output.xlsx')
            # if os.path.exists(default_output_path):
            #     return dcc.send_file(default_output_path)
            # else:
            #     return dcc.send_data_frame(pd.DataFrame().to_excel, "default_output.xlsx")
        

# -----------------------------
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/upload':
        return upload_layout
    elif pathname == '/historical-data':
        return historical_data_layout
    else:
        return home_layout

# Setting initial page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={'background-color': '#1e2732'})
    ])

def start_server():
    # Logic to start your server
    host = "127.0.0.1"
    port = "8050"  # Example port number
    url = f"http://{host}:{port}"

    # Print the URL to the console
    print(f"Running at {url}")  # Step 2: Existing URL output
    
    # Step 3: Open the URL in the default web browser
    webbrowser.open(url)

start_server()

if __name__ == '__main__':
    app.run_server(debug=True)