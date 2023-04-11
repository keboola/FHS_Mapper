#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 08:50:44 2023

@author: ondrejsvoboda
"""

from src.settings import keboola_client
import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/


@st.cache_data
def read_df(table_id, index_col=None, date_col=None):
    keboola_client.tables.export_to_file(table_id, '.')
    table_name = table_id.split(".")[-1]
    return pd.read_csv(table_name, index_col=index_col, parse_dates=date_col)

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
    st.error("""Downloading data from Quickbooks failed. Our team is working on fixing the problems. 
             For more information, please check your inbox and look for ticket Request #27324 """)