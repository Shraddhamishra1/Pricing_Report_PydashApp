import base64
from dash import html
from dash import dash_table
import pandas as pd

from YT01_805_800_MY import generate_dataframe
from YT06_pythoncode import generate_dataframe_YT06
from YT07_pythoncode import generate_dataframe_YT07
from YT01_805pythoncode import generate_dataframe_YT01805
from YT01_800pythoncode import generate_dataframe_YT01800
from YT01_611pythoncode import generate_dataframe_YT01611
from YT04_800pythoncode import generate_dataframe_YT04800
from Ethanol_CBOBpythoncode import generate_dataframe_EthanolCBOB
from YT06_807pythoncode import generate_dataframe_YT06807
from Ottawa_kingston_Bellev_pythoncode import generate_dataframe_Ottawa_KgsBellev
import dash_html_components as html
from Sharepoint_connection import load_files_from_SP,load_files_from_SP_MY

def parse_contents(contents1, filename1):
    Mapping_quotation_codes ,Bio_diesel,  ppt_excel, PTtransfer, depot_mapping, MY_Historical_values = load_files_from_SP_MY()
    
    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])

    try:
        df = generate_dataframe(decoded1, filename1, Mapping_quotation_codes, depot_mapping, Bio_diesel,MY_Historical_values)
        
    except Exception as e:
        print(f"Error in generate_dataframe: {e}")
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, MY_Historical_values
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    

def parse_contents_YT06(contents1, filename1):

    Mapping_quotation_codes , Bio_diesel, ppt_excel, PTtransfer, depot_mapping, MY_Historical_values = load_files_from_SP_MY()

    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])
    
    try:
        # Call generate_dataframe with all decoded contents and filenames
        df = generate_dataframe_YT06(decoded1, filename1,ppt_excel)
    except Exception as e:
        print(f"Error in generate_dataframe: {e}")
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, MY_Historical_values
    
    else:
        return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False

def parse_contents_YT07(contents1, filename1):

    Mapping_quotation_codes  ,Bio_diesel,  ppt_excel, PTtransfer, depot_mapping, MY_Historical_values = load_files_from_SP_MY()
    
    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])
    
    try:
        # Call generate_dataframe with all decoded contents and filenames
        df = generate_dataframe_YT07(decoded1, filename1,PTtransfer,depot_mapping)
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False
    
    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        print("######################## --- AT END OF parse function YT06 --- ###############################")
        return html.Div([table]), df, MY_Historical_values
    
    else:
        print("generate_dataframe did not return DataFrames")
        return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False


# --------------------------------------------------------------------------------------
#YT01_805
def parse_contents_YT01_805(contents1, filename1):

    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()

    Transferprice_Data = Transferprice_Historical_CA

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])

    try:
        df = generate_dataframe_YT01805(decoded1, filename1,mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel)
        
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df,Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# ---------------------------------------------------------------------
#YT01_800
def parse_contents_YT01_800(contents1, filename1):

    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA= load_files_from_SP()

    Transferprice_Data = Transferprice_Historical_CA
    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
    
        df = generate_dataframe_YT01800(decoded1, filename1,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping)
         
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------
# YT01 611

def parse_contents_YT01_611(contents1, filename1):

    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()

    Transferprice_Data = Transferprice_Historical_CA

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT01611(decoded1, filename1,Material_df_611,Orbit_table_df,Customer_specific_dis,Transferprice_Historical_CA )
        
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# # -----------------------------------------------------------------------------------------------------------------
#YT04_800
def parse_contents_YT04_800(contents1, filename1):

    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()
    
    Transferprice_Data = Transferprice_Historical_CA

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT04800(decoded1, filename1,additive_df,ref_price,jet_price,locdiff_df,plant_list)
        
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    
# -----------------------------------------------------------------------------------------------------------------
#EthanolCBOB
def parse_contents_EthanolCBOB(contents1, filename1):
   
    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()

    Transferprice_Data = Transferprice_Historical_CA
    
    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
   
    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_EthanolCBOB(decoded1, filename1, ZonalTP)
             
    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------------------------------
#YT06_807
def parse_contents_YT06807(contents1, filename1):

    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()
    Transferprice_Data = Transferprice_Historical_CA
    
    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    
    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT06807(decoded1, filename1,Additive_MaterialCode,Additive_TPcost)

    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------------------------------
#Ottawa_kingston_Bellev
def parse_contents_Ottawa_KgsBellev(contents1, filename1):
  
    mappingfile,TPValue_conditions_805,zonal_tp,bio_fuels,aviation_fuel,Lines_conditions,TPValue_conditions_800, Zonal_TP,Biofuels_prices,AviationT_prices,CF_CN_Locomotive_Discount,B20_Discount_by_Plant,Zone_Plant_mapping,Material_df_611,Orbit_table_df,Customer_specific_dis, additive_df,ref_price,jet_price,locdiff_df,plant_list,Additive_MaterialCode,Additive_TPcost,ZonalTP,Ottawa_kgsBlv_TP,Transferprice_Historical_CA = load_files_from_SP()
    Transferprice_Data = Transferprice_Historical_CA

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    
    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_Ottawa_KgsBellev(decoded1, filename1, Ottawa_kgsBlv_TP)

    except Exception as e:
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns a DataFrame
    if isinstance(df, pd.DataFrame):
        # Create a DataTable to display the DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]), df, Transferprice_Data
    else:
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False


