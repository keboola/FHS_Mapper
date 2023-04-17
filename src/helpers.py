#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 08:50:44 2023

@author: ondrejsvoboda
"""

from src.settings import keboola_client, STATUS_TAB_ID
import streamlit as st
import pandas as pd

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

@st.cache_data
def read_df(table_id, username, index_col=None, date_col=None):
    keboola_client.tables.export_to_file(table_id, '.')
    table_name = table_id.split(".")[-1]
    df = pd.read_csv(table_name, index_col=index_col, parse_dates=date_col)
    return df.loc[df["username"]==username]

def determine_step(username):
    status_df = read_df(STATUS_TAB_ID, username)    

    authorization = status_df.loc[status_df["username"]==username, "authorization_done"].values[0]
    if authorization==0:
        step = 1
    else:
        step = 2
    return step    
    
#@st.cache_data
def parse_credentials():
    """
    The method takes credentials from streamlit secret and converts
    these into a dictionary compatible with streamlit authenticator

    expected composition of secret variable
    credentials_usernames_USERNAME_VARIABLE
    
    eg
    
    credentials_usernames_ondra_email = 'ondrej.svoboda@keboola.com'
    credentials_usernames_ondra_name = 'Ondřej Svoboda'
    credentials_usernames_ondra_password = 'xxx'

    this would be converted into 
    
    {"credentials":{
        "usernames":{
            "ondra":{
                "email": 'ondrej.svoboda@keboola.com',
                "name": 'Ondřej Svoboda', 
                "password": 'xxx'
                }
            }
        }}

    Returns
    -------
    config_dict - dictionary containing information about credentials formatted
    for stauth
    
    NOTE
    ----
    advanced features of stauth are not currently implemented beyond the simplest
    use. For instance, no preauthorized users or passwords expiry

    """
    config_dict = {}
    
    # 1. check the longest inner subscription
    
    # at this point, I do not check for preauthorized or cookies
    for key in st.secrets:
        creds_dict = config_dict.get("credentials", dict())
        username_dict = creds_dict.get("usernames", dict())    
        username = key.split('_')[-2]
        key_end = key.split('_')[-1]
        user_dict =  username_dict.get(username, dict())
        user_dict[key_end] = st.secrets[key]
        username_dict[username] = user_dict
        creds_dict["usernames"] = username_dict
        config_dict["credentials"] = creds_dict
    
    config_dict["cookie"] = {'expiry_days':0,
                             'key':"random_signature_key",
                             'name':"random_cookie_name"}
    
    config_dict["preauthorized"] = {'emails':["melsby@gmail.com"]}
    
    return config_dict

def data_issues():
    st.error("""Downloading data from Quickbooks is not yet ready. Our team is monitoring the progress. 
             For more information, please check your inbox and look for ticket Request #27324 """)

def write_file_submit_authorization(status_df, 
                              company_id=None, 
                              financial_calendar=None, 
                              file_path=".status.csv"):
    """
    

    Parameters
    ----------
    status_df : TYPE
        DESCRIPTION.
    company_id : TYPE
        DESCRIPTION.
    financial_calendar : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """    

    if not company_id:
        company_id = st.session_state.get("company_id", "")
    
    if not financial_calendar:
        company_id = st.session_state.get("company_id", False)
    
    status_df["company_id"]=company_id
    status_df["authorization_done"] = 1
    status_df.to_csv(file_path, index=False)
    
    return None
    #status_df[""]
         
def update_status_table(
        keboola_client=keboola_client,
        #keboola_key,
        table_id=STATUS_TAB_ID,
    #    bucket_id,
        file_path='.status.csv',
        #primary_key='config_id',
        is_incremental=True, 
        delimiter=',',
        enclosure='"', 
        escaped_by='', 
        columns=['config_id'],
        without_headers=False
        ):
    
    #client = Client(keboola_URL, keboola_key)
    # check whether a table in the bucket exists. If so, retrieve its table_id
    
    res = keboola_client.tables.load(table_id=table_id,
                        file_path=file_path,
                        is_incremental=is_incremental, 
                        delimiter=delimiter,
                        enclosure=enclosure, 
                        escaped_by=escaped_by,
                        columns=columns,
                        without_headers=without_headers) 

    return res, f"table {table_id} has been updated."
    
    
    # try:
    #     try:
    #         tables = client.tables.list()

    #     except Exception as e:
    #         return str(e)
    #     # there will be 0 or 1 hit
    #     table_def = list(filter(lambda x: x['bucket']['id']==bucket_id and x['name']==table_name, tables))
    #     if table_def:
    #         table_id = table_def[0]['id']
    #         # table already exists --> load
    #         try:
    #             _= client.tables.load(table_id=table_id,
    #                                 file_path=file_path,
    #                                 is_incremental=is_incremental, 
    #                                 delimiter=delimiter,
    #                                 enclosure=enclosure, 
    #                                 escaped_by=escaped_by,
    #                                 columns=columns,
    #                                 without_headers=without_headers) 
    #             return f"{table_name} has been updated."
    #         except Exception as e:
    #             return str(e)    
    #     else:
    #         # table does not exist --> create
    #         try:
    #             return client.tables.create(name=table_name,
    #                                 bucket_id=bucket_id,
    #                                 file_path=file_path,
    #                                 primary_key=primary_key) + " successfully created!!"
    #         except Exception as e:
    #             return str(e)   
    # except Exception as e:
    #     return str(e)         
    
def check_config_values():
    
    if (
            (st.session_state["company_id"]==st.session_state["company_id_old"]) or 
            (st.session_state["company_id_old"] in [None, ""])
        ):
        return 1
    else:
        return 0
    
        
        
    # fill logic for custom calendar
    
    
        
        
        
        
        