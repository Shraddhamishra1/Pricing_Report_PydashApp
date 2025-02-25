import base64
import io
from dash import html
from dash import dash_table
import pandas as pd
import datetime

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



def parse_contents(contents1, filename1):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # mapping_file_path, ppt_excel_path, depot_mapping_path
    ppt_excel_path = r"C:\Users\Shraddha.Mishra\Shell\GSCF Digital Portal - Transfer Pricing\Input\ppt_excel.xlsx"
    depot_mapping_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Malaysia\T&S cockpit.xlsx"
    mapping_file_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Malaysia\Mapping for Quotation codes.xlsx"

    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("******************************")

    print("Calling generate_dataframe with arguments")

    try:
        # Call generate_dataframe with all decoded contents and filenames
        # df, tp_template = generate_dataframe(decoded1, filename1, decoded2, filename2, decoded3, filename3, decoded4, filename4)
        print("((((((((((((((((((((()))))))))))))))))))))")
        df, tp_template = generate_dataframe(decoded1, filename1, mapping_file_path, ppt_excel_path, depot_mapping_path)
        
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
        
        return html.Div([table]), df, tp_template
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    

# def parse_contents(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4):
#     # Decode the contents
#     decoded1 = base64.b64decode(contents1.split(',')[1])
#     decoded2 = base64.b64decode(contents2.split(',')[1])
#     decoded3 = base64.b64decode(contents3.split(',')[1])
#     decoded4 = base64.b64decode(contents4.split(',')[1])

#     print("Calling generate_dataframe with arguments")

#     try:
#         # Call generate_dataframe with all decoded contents and filenames
#         df, tp_template = generate_dataframe(decoded1, filename1, decoded2, filename2, decoded3, filename3, decoded4, filename4)
        
#     except Exception as e:
#         print(f"Error in generate_dataframe: {e}")
#         return html.Div([f"Error in generate_dataframe: {e}"]), False, False

#     # Ensure the function returns a DataFrame
#     if isinstance(df, pd.DataFrame):
#         # Create a DataTable to display the DataFrame
#         table = dash_table.DataTable(
#             id='table',
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             data=df.to_dict('records'),
#             style_table={'overflowX': 'auto'},
#             style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
#             style_cell={'textAlign': 'left', 'color': 'black'},
#             style_data={'color': 'black'}
#         )
        
#         return html.Div([table]), df, tp_template
#     else:
#         print("generate_dataframe did not return a DataFrame")
#         return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    

# -------------------------------------------
def parse_contents_YT06(contents1, filename1):
    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])
    ppt_excel_path = r"C:\Users\Shraddha.Mishra\Shell\GSCF Digital Portal - Transfer Pricing\Input\ppt_excel.xlsx"
    MY05_additivecost_path =  r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Malaysia\MY05AdditiveCost20240527.csv"
    MY08_additivecost_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Malaysia\MY08AdditiveCost20240527.csv"


    try:
        # Call generate_dataframe with all decoded contents and filenames
        df_updated_MY05, df_updated_MY08 ,ppt_excel= generate_dataframe_YT06(decoded1, filename1,ppt_excel_path,MY05_additivecost_path,MY08_additivecost_path)
    except Exception as e:
        print(f"Error in generate_dataframe: {e}")
        return html.Div([f"Error in generate_dataframe: {e}"]), False, False

    # Ensure the function returns DataFrames
    if isinstance(df_updated_MY05, pd.DataFrame) and isinstance(df_updated_MY08, pd.DataFrame):
        
        # Concatenate both DataFrames one above another
        concatenated_df = pd.concat([df_updated_MY05, df_updated_MY08], ignore_index=True)
        
        # Create a DataTable to display the concatenated DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in concatenated_df.columns],
            data=concatenated_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]),  df_updated_MY05, df_updated_MY08,ppt_excel
    else:
        print("generate_dataframe did not return DataFrames")
        return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False
    
# -----------------------------------------------------
def parse_contents_YT07(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4):
    # Decode the contents
    decoded1 = base64.b64decode(contents1.split(',')[1])
    decoded2 = base64.b64decode(contents2.split(',')[1])
    decoded3 = base64.b64decode(contents3.split(',')[1])
    decoded4 = base64.b64decode(contents4.split(',')[1])

    print("YT07 files parse_contents function!!!!!!!")

    print("Calling generate_dataframe with arguments")

    try:
        # Call generate_dataframe with all decoded contents and filenames
        df_updated_MY05, df_updated_MY08 = generate_dataframe_YT07(decoded1, filename1, decoded2, filename2, decoded3, filename3, decoded4, filename4)
        print("Calling generate_dataframe with argumentsYT07")

    except Exception as e:
        print(f"Error in generate_dataframe_YT07: {e}")
        return html.Div([f"Error in generate_dataframe_YT07: {e}"]), False, False

    # Ensure the function returns DataFrames
    if isinstance(df_updated_MY05, pd.DataFrame) and isinstance(df_updated_MY08, pd.DataFrame):
        
        # Concatenate both DataFrames one above another
        concatenated_df = pd.concat([df_updated_MY05, df_updated_MY08], ignore_index=True)
        
        # Create a DataTable to display the concatenated DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in concatenated_df.columns],
            data=concatenated_df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
            style_cell={'textAlign': 'left', 'color': 'black'},
            style_data={'color': 'black'}
        )
        
        return html.Div([table]),  df_updated_MY05, df_updated_MY08
    else:
        print("generate_dataframe did not return DataFrames")
        return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False

# --------------------------------------------------------------------------------------


# # -------------------------------------------
# def parse_contents_YT06(contents1, filename1, contents2, filename2, contents3, filename3):
#     # Decode the contents
#     decoded1 = base64.b64decode(contents1.split(',')[1])
#     decoded2 = base64.b64decode(contents2.split(',')[1])
#     decoded3 = base64.b64decode(contents3.split(',')[1])

#     try:
#         # Call generate_dataframe with all decoded contents and filenames
#         df_updated_MY05, df_updated_MY08 = generate_dataframe_YT06(decoded1, filename1, decoded2, filename2, decoded3, filename3)
#     except Exception as e:
#         print(f"Error in generate_dataframe: {e}")
#         return html.Div([f"Error in generate_dataframe: {e}"]), False, False

#     # Ensure the function returns DataFrames
#     if isinstance(df_updated_MY05, pd.DataFrame) and isinstance(df_updated_MY08, pd.DataFrame):
        
#         # Concatenate both DataFrames one above another
#         concatenated_df = pd.concat([df_updated_MY05, df_updated_MY08], ignore_index=True)
        
#         # Create a DataTable to display the concatenated DataFrame
#         table = dash_table.DataTable(
#             id='table',
#             columns=[{'name': i, 'id': i} for i in concatenated_df.columns],
#             data=concatenated_df.to_dict('records'),
#             style_table={'overflowX': 'auto'},
#             style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
#             style_cell={'textAlign': 'left', 'color': 'black'},
#             style_data={'color': 'black'}
#         )
        
#         return html.Div([table]),  df_updated_MY05, df_updated_MY08
#     else:
#         print("generate_dataframe did not return DataFrames")
#         return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False
    
# # -----------------------------------------------------
# def parse_contents_YT07(contents1, filename1, contents2, filename2, contents3, filename3, contents4, filename4):
#     # Decode the contents
#     decoded1 = base64.b64decode(contents1.split(',')[1])
#     decoded2 = base64.b64decode(contents2.split(',')[1])
#     decoded3 = base64.b64decode(contents3.split(',')[1])
#     decoded4 = base64.b64decode(contents4.split(',')[1])

#     print("YT07 files parse_contents function!!!!!!!")

#     print("Calling generate_dataframe with arguments")

#     try:
#         # Call generate_dataframe with all decoded contents and filenames
#         df_updated_MY05, df_updated_MY08 = generate_dataframe_YT07(decoded1, filename1, decoded2, filename2, decoded3, filename3, decoded4, filename4)
#         print("Calling generate_dataframe with argumentsYT07")

#     except Exception as e:
#         print(f"Error in generate_dataframe_YT07: {e}")
#         return html.Div([f"Error in generate_dataframe_YT07: {e}"]), False, False

#     # Ensure the function returns DataFrames
#     if isinstance(df_updated_MY05, pd.DataFrame) and isinstance(df_updated_MY08, pd.DataFrame):
        
#         # Concatenate both DataFrames one above another
#         concatenated_df = pd.concat([df_updated_MY05, df_updated_MY08], ignore_index=True)
        
#         # Create a DataTable to display the concatenated DataFrame
#         table = dash_table.DataTable(
#             id='table',
#             columns=[{'name': i, 'id': i} for i in concatenated_df.columns],
#             data=concatenated_df.to_dict('records'),
#             style_table={'overflowX': 'auto'},
#             style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
#             style_cell={'textAlign': 'left', 'color': 'black'},
#             style_data={'color': 'black'}
#         )
        
#         return html.Div([table]),  df_updated_MY05, df_updated_MY08
#     else:
#         print("generate_dataframe did not return DataFrames")
#         return html.Div(["Error: generate_dataframe did not return DataFrames"]), False, False

# --------------------------------------------------------------------------------------
#YT01_805

def parse_contents_YT01_805(contents1, filename1):
    # Define the local file paths
    mappingfile_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\mapping_conditionsfile.xlsx"
    # tpvalue_conditions_path = r"C:\Users\Shraddha.Mishra\Downloads\mapping_conditionsfile.xlsx"
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)
    # print("--------------------------Parse content function YT01 805 --------------------------------------")
    # print("--------------------------*********************************** --------------------------------------")
    # print(Transferprice_Data)
    # print("--------------------------*********************************** --------------------------------------")

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with arguments YT01 805 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        # df = generate_dataframe_YT01805(decoded1, filename1, mappingfile_path, tpvalue_conditions_path, Transferprice_Data_path)
        # print("11111111111111Calling generate_dataframe_YT01805 inside parse function  YT01 805 ")
        df = generate_dataframe_YT01805(decoded1, filename1, mappingfile_path, Transferprice_Data_path)
        # print("2222222222Calling generate_dataframe_YT01805 inside parse function  YT01 805 ")
        
        
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
        
        print("######################## --- AT END OF parse function YT01 805 --- ###############################")
        # print(Transferprice_Data)
        return html.Div([table]), df,Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# ---------------------------------------------------------------------
#YT01_800
def parse_contents_YT01_800(contents1, filename1):
    # Define the local file paths
    mappingfile_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\mapping_conditionsfile.xlsx"
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)
    print("Inside parse function YT01 800")

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with arguments YT01 800 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        print("Inside TRY OF parse function YT01 800")

    
        df = generate_dataframe_YT01800(decoded1, filename1, mappingfile_path,Transferprice_Data_path)
        print("Inside after generate function in parse function YT01 800")

        
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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------------------------------
#YT01_611
def parse_contents_YT01_611(contents1, filename1):
    # Define the local file paths
    mappingfile_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\mapping_conditionsfile.xlsx"
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with arguments YT01 611 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT01611(decoded1, filename1, mappingfile_path,Transferprice_Data_path)
        
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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    

# -----------------------------------------------------------------------------------------------------------------
#YT04_800
def parse_contents_YT04_800(contents1, filename1):
    # Define the local file paths
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"    
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with arguments YT04 800 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT04800(decoded1, filename1,Transferprice_Data_path)
        
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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False
    
# -----------------------------------------------------------------------------------------------------------------
#EthanolCBOB
def parse_contents_EthanolCBOB(contents1, filename1):
    # Define the local file paths
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"    
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with arguments EthanolCBOB Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_EthanolCBOB(decoded1, filename1, Transferprice_Data_path)
        
        # df = generate_dataframe_YT04800(decoded1, filename1,Transferprice_Data_path)
        
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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------------------------------
#YT06_807
def parse_contents_YT06807(contents1, filename1):
    # Define the local file paths
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"    
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with argumeznts YT06 807 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_YT06807(decoded1, filename1, Transferprice_Data_path)

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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False

# -----------------------------------------------------------------------------------------------------------------
#Ottawa_kingston_Bellev
def parse_contents_Ottawa_KgsBellev(contents1, filename1):
    # Define the local file paths
    Transferprice_Data_path = r"C:\Users\Shraddha.Mishra\Downloads\UI_files\Transfer Price Template_New1.xlsx"    
    Transferprice_Data = pd.read_excel(Transferprice_Data_path, engine='openpyxl', dtype='object', sheet_name=None)

    # Decode the GSAP_data content
    decoded1 = base64.b64decode(contents1.split(',')[1])
    print("Calling generate_dataframe with argumeznts YT06 807 Canada")

    try:
        # Call generate_dataframe with the decoded GSAP_data content and local file paths
        df = generate_dataframe_Ottawa_KgsBellev(decoded1, filename1, Transferprice_Data_path)

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
        
        return html.Div([table]), df, Transferprice_Data
    else:
        print("generate_dataframe did not return a DataFrame")
        return html.Div(["Error: generate_dataframe did not return a DataFrame"]), False, False


