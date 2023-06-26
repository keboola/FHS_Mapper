import streamlit as st
from kbcstorage.client import Client

# credentials
KEBOOLA_STACK = st.secrets["kbc_url"]
KEBOOLA_TOKEN = st.secrets["kbc_token"]
keboola_client = Client(KEBOOLA_STACK, KEBOOLA_TOKEN)

#STATUS_TAB_ID = 'out.c-create_configs.status'
STATUS_TAB_ID = 'in.c-StreamlitIO.dev_status'
MAPPING_CLASSES_TAB_ID = 'in.c-StreamlitIO.mapping_classes'
STREAMLIT_BUCKET_ID = 'in.c-StreamlitIO'
RESTAURANTS_TAB_ID = 'in.c-StreamlitIO.restaurant_aux'
MAPPING_TAB_ID = 'in.c-StreamlitIO.mapping'
DEBUG = False
