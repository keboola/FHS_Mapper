#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 08:50:44 2023

@author: ondrejsvoboda
"""

from src.settings import keboola_client
import streamlit as st
import pandas as pd

@st.cache_data
def read_df(table_id, index_col=None, date_col=None):
    keboola_client.tables.export_to_file(table_id, '.')
    table_name = table_id.split(".")[-1]
    return pd.read_csv(table_name, index_col=index_col, parse_dates=date_col)
