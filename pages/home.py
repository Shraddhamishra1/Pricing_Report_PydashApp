import dash_bootstrap_components as dbc
from dash import html, dcc
from utils import get_link
import dash

dash.register_page(__name__, path = '/')

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

# Home Page Layout with Image and Objective
layout = html.Div([
    navbar,
    html.Div([
        html.Img(src=get_link('/assets/Transferprice_ship.JPG'), style={'max-width': '100%', 'max-height': '70vh', 'display': 'block', 'margin': 'auto', 'margin-bottom': '20px', 'width': '90%'}),
    ]),
    html.H1("Objective", style={'font-size': '30px','text-align': 'center', 'color': 'white', 'width': '80%', 'margin': 'auto'}),
    html.Div([
        html.P(html.B("Welcome to Ezee-TP."), style={'color': 'white', 'font-size': '20px'}),
        html.P("This is a tool that makes your Transfer Price updates simpler. At present, this tool is designed for Malaysia and Canada.", style={'color': 'white', 'font-size': '18px'}),
        html.P(html.B("How to use:"), style={'color': 'white', 'font-size': '20px'}),
        html.B("Upload page", style={'color': 'white', 'font-size': '20px'}),
        html.P("i. Maintain the mapping files in sharepoint folders of respective countries.", style={'color': 'white', 'font-size': '18px'}),
        html.P("ii. Upload the GSAP data through the button displayed.", style={'color': 'white', 'font-size': '18px'}),
        html.P("iii. Click the run button to generate the report.", style={'color': 'white', 'font-size': '18px'}),
        html.P("iv. Click the download button that will download the output report in Download folder of your system.", style={'color': 'white', 'font-size': '18px'}),
        html.B("TP History", style={'color': 'white', 'font-size': '20px'}),
        html.P("i. This page shows historical values of Transfer prices. Select Country from dropdown and it will display its historical values.", style={'color': 'white', 'font-size': '18px'}),
    ], style={'margin-top': '20px', 'text-align': 'left', 'color': 'white', 'width': '80%', 'margin': 'auto'})
], style={'background-color': '#1e2732', 'color': 'white'})

