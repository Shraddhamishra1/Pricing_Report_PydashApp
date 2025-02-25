import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table
import os
import pandas as pd
import webbrowser
import io
import tempfile
from datetime import datetime
from utils import get_link
from app import app

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


# historical_data_layout = html.Div([
layout = html.Div([
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
        dcc.Tabs(id='tabs', value=None, children=[], style={
            'color': 'black',
            'fontWeight': 'bold',
            'overflowX': 'auto',
            'whiteSpace': 'nowrap',
            'display': 'flex',
            'flexWrap': 'nowrap',
            'maxWidth': '100%',
            'height': 'auto',
            'minWidth': '600px'
        }      
        ),
        html.Div(id='tabs-content', style={
            'background-color': '#1e2732',
            'padding': '20px',
            'border-radius': '10px',
            'margin-top': '15px',
            'minWidth': '300px'
        })
    ], style={'background-color': '#1e2732', 'border-radius': '20px'})
], style={'background-color': '#1e2732', 'color': '#1e2732'})


app.layout = layout
# app.layout = historical_data_layout

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
    return [dcc.Tab(label=sheet, value=sheet, style={
        'whiteSpace': 'nowrap',
        'textAlign': 'center',
        'height': 'auto',
        'display': 'inline-block',
        'minWidth': '400px'
    },
    selected_style={
        'whiteSpace': 'nowrap',
        'textAlign': 'center',
        'height': 'auto',
        'display': 'inline-block',
        'minWidth': '200px',  # Ensure the selected tab has the same minWidth
        'maxWidth': '200px',  # Ensure the selected tab has the same maxWidth
        'padding': '10px',
        'backgroundColor': '#d3d3d3' 
    }) for sheet in sheets]

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

        if df.empty:
            print(f"No data available for tab: {tab_name}")
            return html.Div("Select a Country option in dropdown menu then select individual material tab to display its historical TP values.", style={'color': 'white'})

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
        print("No data available")
        return html.Div("This page will display the historical transfer price values of different Countries.", style={'color': 'white'})

