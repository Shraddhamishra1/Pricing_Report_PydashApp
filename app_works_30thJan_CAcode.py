import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table
from file_parsers_25thNov_copy import parse_contents,parse_contents_YT06,parse_contents_YT07,parse_contents_YT01_805,parse_contents_YT01_800,parse_contents_YT01_611,parse_contents_YT04_800,parse_contents_EthanolCBOB, parse_contents_YT06807,parse_contents_Ottawa_KgsBellev
import os
import pandas as pd
import webbrowser
import io
import tempfile
from datetime import datetime

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
        # html.Img(src=r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Pecten - colour with white outline.png", style={'height': '75px', 'margin-top': '-6px'}),  # icon height        
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
        # html.Img(src=r"C:\Users\Shraddha.Mishra\Downloads\UI_files\LNGOutlook_UK.JPG", 
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
        html.H1("Please select the required Country and report type to generate its Transfer Price report with new TP values. Then upload the GSAP data file, then click the generate report button which generates the report and to view the output in UI. Later you can click on download button to download the new transfer prices report in your Downloads folder.", style={
            'font-size': '19px',
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
                value=None,
                style={'margin-top': '20px', 'margin-bottom': '5px', 'width': '200px', 'font-size': '17px'}
            ),
            dcc.Dropdown(
                id='Report Type',
                options=[
                    {'label': 'YT01 800', 'value': 'YT01 800'},
                    {'label': 'YT01 805', 'value': 'YT01 805'},
                    {'label': 'YT01 611', 'value': 'YT01 611'},
                    {'label': 'YT04 800', 'value': 'YT04 800'},
                    {'label': 'YT06 807', 'value': 'YT06 807'},
                    {'label': 'Ethanol CBOB', 'value': 'Ethanol CBOB'},
                    {'label': 'Ottawa Kingston & Bellev', 'value': 'Ottawa Kingston & Bellev'},
                    {'label': 'MY05_YT06', 'value': 'MY05_YT06'},
                    {'label': 'MY08_YT06', 'value': 'MY08_YT06'},
                    {'label': 'MY05_YT07', 'value': 'MY05_YT07'},
                    {'label': 'MY08_YT07', 'value': 'MY08_YT07'},
                ],
                placeholder="Report Type",
                value=None,
                style={'margin-top': '20px', 'margin-bottom': '5px', 'width': '200px', 'font-size': '17px'}
            )
        ], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),
        
        html.Div(id='upload-container', children=[], style={'display': 'flex', 'justify-content': 'center', 'gap': '20px', 'flex-wrap': 'wrap'}),
        
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

# -----------------------------------------------------------
def update_upload_buttons(country, report_type):
    print(f"update_upload_buttons called with country={country}, report_type={report_type}")
    
    # Initialize upload_buttons as an empty list
    upload_buttons = []

    #  Check if country and report_type are not None
    if country is None or report_type is None:
        return upload_buttons

    # Update labels and buttons based on country and report type
    if country == 'Malaysia':
        if report_type == 'MY05_YT06':
            label_1 = 'MY05 Additive Cost'
            # label_2 = 'MY08 Additive Cost'
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
                ]
        elif report_type == 'MY08_YT06':
            # label_1 = 'MY05 Additive Cost'
            label_1 = 'MY08 Additive Cost'
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
                ]
        
        
        
        elif report_type == 'MY05_YT07':
            label_1 = 'MY05 PT Update'
            # label_2 = 'MY08 PT Update'
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
            ]

        elif report_type == 'MY08_YT07':
            # label_1 = 'MY05 PT Update'
            label_1 = 'MY08 PT Update'
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
                ]
        
        elif report_type in ['YT01 800', 'YT01 805', 'YT01 611', 'YT04 800','YT06 807','Ethanol CBOB','Ottawa Kingston & Bellev']:
            label_1 = 'Upload TP File'
            # label_2 = 'Quotation Codes Mapping'
            # label_3 = 'Depot/Plant Mapping File'
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
            ]
    
    elif country == 'Canada' and report_type in ['YT01 800', 'YT01 805', 'YT01 611', 'YT04 800','YT06 807','Ethanol CBOB','Ottawa Kingston & Bellev']:
        label_1 = 'GSAP File'
        print('CANADA: ',label_1, country , report_type)
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
            ], style={'background-color': '#F9C80E', 'padding': '40px', 'border-radius': '20px', 'margin-top': '40px', 'margin-bottom': '20px', 'border': '1px solid black'})
        ]

    return upload_buttons
# --------------------------------------------------------------------
@app.callback(
    [Output('progress-bar-1', 'value'),
     Output('upload-status-1', 'children')],
    [Input('upload-data-1', 'contents'),
     Input('Country', 'value'),
     Input('Report Type', 'value')],
    [State('upload-data-1', 'filename')]
)

def update_progress_bars(contents1, country, report_type, filename1):
    progress_values = [0]
    upload_status = ['Not Uploaded']

    if contents1:
        progress_values[0] = 100
        upload_status[0] = 'Uploaded'
    # if contents2:
    #     progress_values[1] = 100
    #     upload_status[1] = 'Uploaded'
    # if contents3:
    #     progress_values[2] = 100
    #     upload_status[2] = 'Uploaded'

    if country in ['Malaysia','Canada'] and report_type in ["YT01 805", "YT01 800", "YT01 611", "YT04 800","YT06 807","Ethanol CBOB","Ottawa Kingston & Bellev","MY05_YT06","MY08_YT06", "MY05_YT07","MY08_YT07"]:
        return (
            progress_values[0],
            upload_status[0]
        )
    else:
        return (
            progress_values[0],
            upload_status[0]
        )

# ---------------------------------------------------------------------
tp_template_global = None
# Global variable to store the output DataFrame
output_df_global = None
Canada_historicaldf = None

@app.callback(
    [Output('output-data-upload', 'children'),
     Output('download-button', 'disabled')],
    [Input('run-script-button', 'n_clicks')],
    [State('upload-data-1', 'contents'),
     State('upload-data-1', 'filename'),
     State('Country', 'value'),
     State('Report Type', 'value')]
)
def run_script(n_clicks, contents1, filename1,country, report_type):
    global tp_template_global  # Declare the global variable
    global output_df_global
    global Canada_historicaldf

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
        # if country == "Malaysia" and report_type == "YT06":
        #     if contents1 and contents2 and contents3:
        #         YT06_output_div, MY05_additivecost, MY08_additivecost = parse_contents_YT06(contents1, filename1, contents2, filename2, contents3, filename3)
        #     else:
        #         raise ValueError("Three files are required for YT06 report type")
            
        # if country == "Malaysia" and report_type == "YT07":
        #     if contents1 and contents2 and contents3:
        #         YT07_output_div, MY05_PTUpdate, MY08_PTUpdate = parse_contents_YT07(contents1, filename1, contents2, filename2, contents3, filename3)
        #     else:
        #         raise ValueError("Three files are required for YT07 report type")
            
        # elif country == "Malaysia" and report_type in ["YT01 800", "YT01 805", "YT01 611"]:
        #     print("Using parse_contents yt01 800")
        #     if contents1 and contents2 and contents3:
        #         output_div, output_df, tp_template = parse_contents(contents1, filename1, contents2, filename2, contents3, filename3)
        #     else:
        #         raise ValueError("Three files are required for 800, 805, and 600 report types")

        print('------------------------------------ After Country and Report Type is selected -------------------------------------')
        if country == "Canada" and report_type == "YT01 805":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT01 805")
                output_div, output_df, Transferprice_Data = parse_contents_YT01_805(contents1, filename1)

        elif country == "Canada" and report_type == "YT01 800":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_YT01_800(contents1, filename1)
        
        elif country == "Canada" and report_type == "YT01 611":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_YT01_611(contents1, filename1)

        elif country == "Canada" and report_type == "YT04 800":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_YT04_800(contents1, filename1)

        elif country == "Canada" and report_type == "Ethanol CBOB":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_EthanolCBOB(contents1, filename1)
        
        elif country == "Canada" and report_type == "YT06 807":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_YT06807(contents1, filename1)
        
        elif country == "Canada" and report_type == "Ottawa Kingston & Bellev":
            print("Report selected is :", country, report_type)
            if contents1:
                output_div, output_df, Transferprice_Data = parse_contents_Ottawa_KgsBellev(contents1, filename1)
            
            else:
                print("Not support fitlers")
                raise ValueError("One file is required for Canada 800, 805, and 611,  report types")
        else:
            raise ValueError("Unsupported country or report type")

        # Check if output_df is a DataFrame (for parse_contents)
        if output_df is not None and isinstance(output_df, pd.DataFrame):
            # Get the path to the Downloads folder
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

            # output_path = os.path.join(downloads_path, 'tp_my_test.xlsx')
            output_path = os.path.join(downloads_path, f'output_{country}_{report_type.replace(" ", "_")}.xlsx')
            
            print(f"Saving DataFrame to: {output_path}")
            # Save the output DataFrame to a file
            output_df_global = output_df  # Store the DataFrame in the global variable
            print("Processed output file saved successfully.")

            # Create a table to display the DataFrame
            output_div = dash_table.DataTable(
                data=output_df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in output_df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'color': 'black'}
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
        Canada_historicaldf = Transferprice_Data

    except Exception as e:
        print(f"Error in run_script: {e}")
        return html.Div([f"Error in run_script: {e}"]), True

    # Return the appropriate output based on the report type
    if report_type == "YT06":
        return YT06_output_div, False
    elif report_type == "YT07":
        return YT07_output_div, False
    else:
        return output_div, False

# ---------------------------------------------------------------------
historical_data_layout = html.Div([
    navbar,

    html.H1("Click the below tabs to see its past Transfer Price data.", style={
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

    
app.layout = historical_data_layout

@app.callback(
    Output('tabs', 'children'),
    Input('country-dropdown', 'value')
)
def update_tabs(selected_country):
    if selected_country == 'Canada':
        sheets = Canada_historicaldf.keys()
    elif selected_country == 'Malaysia':
        sheets = tp_template_global.keys()
    else:
        sheets = []

    print("This 596 displays the tabs list")
    return [dcc.Tab(label=sheet, value=sheet, style={'whiteSpace': 'normal', 'wordWrap': 'break-word', 'textAlign': 'center', 'height': 'auto'}) for sheet in sheets]

    # return [dcc.Tab(label=sheet, value=sheet) for sheet in sheets]
    # return [dcc.Tab(label=sheet, value=sheet, style={'whiteSpace': 'normal', 'wordWrap': 'break-word', 'textAlign': 'center', 'height': 'auto'}) for sheet in sheets]
    print("---------------------55555------------------")

    # print("This displays the tabs list")
    # print("---------------------")


# --------------------------------------------------------------------
# correct code

# @app.callback(
#     Output('tabs-content', 'children'),
#     Input('tabs', 'value'),
#     Input('country-dropdown', 'value')
# )
# def update_tab_content(tab_name, selected_country):
#     print('Selected Country', selected_country)
#     if selected_country == 'Canada':
#         data_dict = Canada_historicaldf
#     elif selected_country == 'Malaysia':
#         data_dict = tp_template_global
#     else:
#         data_dict = {}

#     if data_dict:
#         df = data_dict.get(tab_name, pd.DataFrame())

#         if df.empty:
#             print(f"No data available for tab: {tab_name}")
#             return html.Div("Select a Country option in dropdown menu then select individual material tab to display its historical TP values.", style={'color': 'white'})

#         print(f"Displaying data for tab: {tab_name}")
#         return dash_table.DataTable(
#             id='historical-data-table',
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             data=df.to_dict('records'),
#             style_table={'overflowX': 'auto'},
#             style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
#             style_cell={'textAlign': 'left', 'color': 'black'},
#             style_data={'color': 'black'}
#         )
#     else:
#         print("No data available")
#         return html.Div("This page will display the historical transfer price values of different Countries.", style={'color': 'white'})

# -----------------------------------------------------------------------------------------------

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('country-dropdown', 'value')
)
def update_tab_content(tab_name, selected_country):
    print('Selected Country', selected_country)
    if selected_country == 'Canada':
        data_dict = Canada_historicaldf
    elif selected_country == 'Malaysia':
        data_dict = tp_template_global
    else:
        data_dict = {}

    if data_dict:
        df = data_dict.get(tab_name, pd.DataFrame())

        print('Line 658 displaying the tabs')

        if df.empty:
            print(f"No data available for tab: {tab_name}")
            return html.Div("Select a Country option in dropdown menu then select individual material tab to display its historical TP values.", style={'color': 'white'})

        print(f"Displaying data for tab: {tab_name}")
        return dash_table.DataTable(
            id='historical-data-table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'color': 'black',
                'whiteSpace': 'normal',  # Add this line to wrap text
                'height': 'auto'  # Add this line to adjust height
            },
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
    else:
        print("No data available")
        return html.Div("This page will display the historical transfer price values of different Countries.", style={'color': 'white'})
    

    # -------------------------

@app.callback(
    Output('download-file', 'data'),
    [Input('download-button', 'n_clicks')],
    [State('Country', 'value'),
     State('Report Type', 'value')]
)
def download_file(n_clicks, country, report_type):
    global output_df_global
    print("inside downloadfile function")

    if n_clicks:
        print("n_clicks:", n_clicks)
        if output_df_global is not None:
            print('output_df_global:', output_df_global)

            # Convert the DataFrame to a file-like object
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                output_df_global.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)

            # Save the BytesIO object to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(output.read())
                tmp_file_path = tmp_file.name

            # Get today's date
            today_date = datetime.today().strftime('%Y-%m-%d')
            return dcc.send_file(tmp_file_path, filename=f'output_{country}_{report_type.replace(" ", "_")}_{today_date}.xlsx')
        else:
            print("No output DataFrame available to download.")
            return None

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
    app.run_server(debug=False)

