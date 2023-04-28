#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 20:03:54 2023

@author: ondrejsvoboda
"""

import streamlit as st
from kbcstorage.client import Client

# credentials
KEBOOLA_STACK = st.secrets["kbc_url"]
KEBOOLA_TOKEN = st.secrets["kbc_token"]
keboola_client = Client(KEBOOLA_STACK, KEBOOLA_TOKEN)

#STATUS_TAB_ID = 'out.c-create_configs.status'
STATUS_TAB_ID = 'in.c-StreamlitIO.status'
MAPPING_CLASSES_TAB_ID = 'in.c-StreamlitIO.mapping_classes'
STREAMLIT_BUCKET_ID = 'in.c-StreamlitIO'
RESTAURANTS_TAB_ID = 'in.c-StreamlitIO.restaurant_aux'
MAPPING_TAB_ID = 'in.c-StreamlitIO.mapping'
DEBUG = False