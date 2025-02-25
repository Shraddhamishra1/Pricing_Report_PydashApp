import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from file_parsers import parse_contents,parse_contents_YT06,parse_contents_YT07,parse_contents_YT01_805,parse_contents_YT01_800,parse_contents_YT01_611,parse_contents_YT04_800,parse_contents_EthanolCBOB, parse_contents_YT06807,parse_contents_Ottawa_KgsBellev
import os
import pandas as pd
from datetime import datetime
from utils import get_link
from app import app  # Import the app object

import io
import tempfile

dash.register_page(__name__)

# Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href=get_link("/home"), style={'font-size': '1.5em', 'color': 'white'})),
        dbc.NavItem(dbc.NavLink("Upload", id="upload-link", href=get_link("/upload"), style={'font-size': '1.5em', 'color': 'white'})),
        dbc.NavItem(dbc.NavLink("TP History", href=get_link("/historical-data"), style={'font-size': '1.5em', 'color': 'white'})),
    ],
    brand=html.Div([
        html.Img(src=get_link('/assets/Shell logo.png'), style={'height': '75px', 'margin-top': '-6px'}),  # icon height        
        html.H3("TRANSFER PRICING PORTAL", style={'color': 'white', 'margin-left': '9px', 'margin-right': '30px'})
    ], style={'display': 'flex', 'align-items': 'center'}),
    brand_href=get_link("/home"),
    color="dark",
    dark=True,
    brand_style={'position': 'absolute', 'left': '50%', 'transform': 'translateX(-50%)', 'color': 'white', 'font-size': '2.0em'}
)

layout = html.Div([
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
    Output('Report Type', 'options'),
    Input('Country', 'value')
)
def set_report_options(selected_country):
    if selected_country == 'Malaysia':
        return [
            {'label': 'YT01 805', 'value': 'YT01 805'},
            {'label': 'YT01 800', 'value': 'YT01 800'},
            {'label': 'MY05_YT06', 'value': 'MY05_YT06'},
            {'label': 'MY08_YT06', 'value': 'MY08_YT06'},
            {'label': 'MY05_YT07', 'value': 'MY05_YT07'},
            {'label': 'MY08_YT07', 'value': 'MY08_YT07'}
        ]
    elif selected_country == 'Canada':
        return [
            {'label': 'YT01 805', 'value': 'YT01 805'},
            {'label': 'YT01 800', 'value': 'YT01 800'},
            {'label': 'YT01 611', 'value': 'YT01 611'},
            {'label': 'YT04 800', 'value': 'YT04 800'},
            {'label': 'YT06 807', 'value': 'YT06 807'},
            {'label': 'Ethanol CBOB', 'value': 'Ethanol CBOB'},
            {'label': 'Ottawa Kingston & Bellev', 'value': 'Ottawa Kingston & Bellev'}
        ]
    return []


@app.callback(
    Output('upload-container', 'children'),
    [Input('Country', 'value'),
     Input('Report Type', 'value')]
)

def update_upload_buttons(country, report_type):
    print(f"update_upload_buttons called with country={country}, report_type={report_type}")
    
    # Initialize upload_buttons as an empty list
    upload_buttons = []

    #  Check if country and report_type are not None
    if country is None or report_type is None:
        return upload_buttons

    elif country == 'Canada' or country == 'Malaysia' and report_type in ['YT01 800', 'YT01 805', 'YT01 611', 'YT04 800','YT06 807','MY05_YT06','MY05_YT07','MY08_YT06','MY08_YT07','Ethanol CBOB','Ottawa Kingston & Bellev']:
        label_1 = 'GSAP File'
        print(country,' : ',label_1, country , report_type)
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


tp_template_global = None
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

    try:

        if country == "Malaysia" and report_type in ["YT01 800", "YT01 805"]:
            print("Report selected is :", country, report_type)
            if contents1:
                print("In Malayisa and report_type == YT01 805 or YT01 800")
                output_div, output_df, tp_template = parse_contents(contents1, filename1)

            tp_template_global = tp_template


        elif country == "Malaysia" and report_type in ["MY05_YT06","MY08_YT06"]:
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Malaysia and report_type == YT06")
                output_div, output_df, MY_Historical_values = parse_contents_YT06(contents1, filename1)

            tp_template_global = MY_Historical_values

        elif country == "Malaysia" and report_type in ["MY05_YT07","MY08_YT07"]:
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Malaysia and report_type == YT07")
                output_div, output_df, MY_Historical_values = parse_contents_YT07(contents1, filename1)

            tp_template_global = MY_Historical_values
    
        elif country == "Canada" and report_type == "YT01 805":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT01 805")
                output_div, output_df, Transferprice_Data = parse_contents_YT01_805(contents1, filename1)

            Canada_historicaldf = Transferprice_Data
            
        elif country == "Canada" and report_type == "YT01 800":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT01 800")
                output_div, output_df, Transferprice_Data = parse_contents_YT01_800(contents1, filename1)

            Canada_historicaldf = Transferprice_Data
            
        elif country == "Canada" and report_type == "YT01 611":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT01 611")
                output_div, output_df, Transferprice_Data = parse_contents_YT01_611(contents1, filename1)
                
            Canada_historicaldf = Transferprice_Data
            

        elif country == "Canada" and report_type == "YT04 800":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT04 800")
                output_div, output_df, Transferprice_Data = parse_contents_YT04_800(contents1, filename1)

            Canada_historicaldf = Transferprice_Data
            

        elif country == "Canada" and report_type == "Ethanol CBOB":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type Ethanol")
                output_div, output_df, Transferprice_Data = parse_contents_EthanolCBOB(contents1, filename1)

            Canada_historicaldf = Transferprice_Data
            
        
        elif country == "Canada" and report_type == "YT06 807":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type == YT06 807")
                output_div, output_df, Transferprice_Data = parse_contents_YT06807(contents1, filename1)

            Canada_historicaldf = Transferprice_Data
            
        
        elif country == "Canada" and report_type == "Ottawa Kingston & Bellev":
            print("Report selected is :", country, report_type)
            if contents1:
                print("in Canada and report_type Ottawa Kingston & Bellev")
                output_div, output_df, Transferprice_Data = parse_contents_Ottawa_KgsBellev(contents1, filename1)

                Canada_historicaldf = Transferprice_Data
            
            else:
                print("Not support fitlers")
                raise ValueError("One file is required for Canada 800, 805, and 611,  report types")
        else:
            raise ValueError("Unsupported country or report type")
        

        if output_df is not None and isinstance(output_df, pd.DataFrame):
            #  Get the path to the output folder in the repo
            repo_path = os.path.dirname(os.path.abspath(__file__))
            output_folder_path = os.path.join(repo_path, 'output')

            print("@@@@@@@@@@@@@@@@@@@@@")

            print(repo_path , output_folder_path)
            print("^^^^^^^^^^^^^^^^^^")
            
            # Ensure the output folder exists
            os.makedirs(output_folder_path, exist_ok=True)

            # Define the output path
            output_path = os.path.join(output_folder_path, f'output_{country}_{report_type.replace(" ", "_")}.xlsx')
    
            print(f"Saving DataFrame to: {output_path}")
            # Save the output DataFrame to a file
    
            output_df_global = output_df  # Store the DataFrame in the global variable
            output_df.to_excel(output_path, index=False)
            print("Processed output file saved successfully.")

        # # Check if output_df is a DataFrame (for parse_contents)
        # if output_df is not None and isinstance(output_df, pd.DataFrame):
        #     # Get the path to the Downloads folder
        #     downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        #     # output_path = os.path.join(downloads_path, 'tp_my_test.xlsx')
        #     output_path = os.path.join(downloads_path, f'output_{country}_{report_type.replace(" ", "_")}.xlsx')
            
        #     print(f"Saving DataFrame to: {output_path}")
        #     # Save the output DataFrame to a file
        #     output_df_global = output_df  # Store the DataFrame in the global variable
        #     print("Processed output file saved successfully.")

        #     # Create a table to display the DataFrame
        #     output_div = dash_table.DataTable(
        #         data=output_df.to_dict('records'),
        #         columns=[{'name': i, 'id': i} for i in output_df.columns],
        #         style_table={'overflowX': 'auto'},
        #         style_cell={'textAlign': 'left', 'color': 'black'}
        #     )
        

    except Exception as e:
        print(f"Error in run_script: {e}")
        return html.Div([f"Error in run_script: {e}"]), True

    return output_div, False


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