import streamlit as st
#import pandas as pd
from src.settings import STATUS_TAB_ID, MAPPING_CLASSES_TAB_ID
from src.helpers import parse_credentials
from src.helpers import read_df
from src.helpers import determine_step
from src.streamlit_widgets import WorkflowProgress, submit_form, render_clickable_link
from src.streamlit_widgets import render_selectboxes
import streamlit_authenticator as stauth
from PIL import Image

config_dict = parse_credentials()

authenticator = stauth.Authenticate(
    config_dict['credentials'],
    config_dict['cookie']['name'],
    config_dict['cookie']['key'],
    config_dict['cookie']['expiry_days'],
    config_dict['preauthorized']
)
        
with st.sidebar:
    image = Image.open('FHS_logo.png')
    st.image(image, caption='')

    st.markdown('## **QUICKBOOKS AUTOMATION SETUP**')
    name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    status_df = read_df(STATUS_TAB_ID, filter_col_name="username", filter_col_value=name)
    config_id = status_df.config_id.values[0]
    #st.write(config_id)
    if "company_id_old" not in st.session_state.keys(): 
        st.session_state["company_id_old"] = status_df["company_id"].values[0]
    if "custom_calendar_old" not in st.session_state.keys(): 
        st.session_state["custom_calendar_old"] = status_df["custom_calendar"].values[0]

    step = determine_step(name)
    preselected_option = [1, 2].index(step)
        
    with st.sidebar:
        STEP = st.selectbox("[MOCK ONLY] select workflow step", [1, 2], index=preselected_option)


    #----------------------------------------------------------
    if STEP == 1:
        st.session_state.authorization_sentiment = WorkflowProgress.theme_inprogress
        st.session_state.mapping_sentiment = WorkflowProgress.theme_neutral
        
    if STEP == 2:
        st.session_state.authorization_sentiment = WorkflowProgress.theme_good
        st.session_state.mapping_sentiment = WorkflowProgress.theme_inprogress
        mapping_df = read_df(MAPPING_CLASSES_TAB_ID, "config_id", config_id)
        st.dataframe(mapping_df)
        mapping_values = mapping_df.loc[mapping_df.type=='Class', "class_dep"].unique()
        #st.write(mapping_df.loc[mapping_df.type=='Class', "class_dep"])
    #   st.write(mapping_values)
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        x = authenticator.logout('Logout', 'main')
        if st.session_state['logout'] == True:
            st.cache_data.clear()
            st.session_state['logout'] = False
elif authentication_status == False:
    with st.sidebar:
        st.error('Username/password is incorrect')
elif authentication_status == None:
    with st.sidebar:
        st.warning('Please enter your username and password')

# stop the code flow if the authentication is not successful
if not authentication_status:
    st.stop()
       
wc = WorkflowProgress("ondra")

if STEP == 1:    
    # Initialize disabled for form_submit_button to False
    if "clicked_submit" not in st.session_state:
        st.session_state.clicked_submit = False
    
    submitted = submit_form(status_df)
        
    if st.session_state.clicked_submit:
    #if submitted:
        url = status_df["OauthUrl"].values[0]
        render_clickable_link(url, status_df)

elif STEP == 2:
    render_selectboxes(mapping_values, status_df)
    
else:
    st.info("mapping functionality is about to be released")
    
