import streamlit as st
from src.settings import STATUS_TAB_ID, MAPPING_CLASSES_TAB_ID, DEBUG
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

    with st.sidebar:
        st.write(f'Welcome *{name}*')
        x = authenticator.logout('Logout', 'main')
        if st.session_state['logout'] == True:
            st.cache_data.clear()
            st.session_state['logout'] = False

    status_df = read_df(STATUS_TAB_ID, filter_col_name="entity_name", filter_col_value=name, dtype={'config_id':str})
    config_id = status_df.config_id.values[0]
    if "company_id_old" not in st.session_state.keys(): 
        st.session_state["company_id_old"] = status_df["company_id"].values[0]
    if "custom_calendar_old" not in st.session_state.keys(): 
        st.session_state["custom_calendar_old"] = status_df["custom_calendar"].values[0]
    if "report_tracking_old" not in st.session_state.keys(): 
        st.session_state["report_tracking_old"] = status_df["report_tracking"].values[0]
    STEP = determine_step(name)
    preselected_option = [1, 2].index(STEP)
        

    if STEP == 1:
        st.session_state.authorization_sentiment = WorkflowProgress.theme_inprogress
        st.session_state.mapping_sentiment = WorkflowProgress.theme_neutral
        
    if STEP == 2:
        st.session_state.authorization_sentiment = WorkflowProgress.theme_good
        st.session_state.mapping_sentiment = WorkflowProgress.theme_inprogress
        mapping_df = read_df(MAPPING_CLASSES_TAB_ID, "config_id", config_id, dtype={'config_id':str})
        
        # if there are no classes, just show departments, otherwise show classes
        
        if 'Class' in  mapping_df.type.values: 
            mapping_values = mapping_df.loc[mapping_df.type=='Class', "class_dep"].unique()
        else:
            mapping_values = mapping_df.loc[mapping_df.type=='Department', "class_dep"].unique()

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
        url = status_df["OauthUrl"].values[0]
        render_clickable_link(url, status_df)

elif STEP == 2:
    render_selectboxes(mapping_values, status_df,name, debug=DEBUG)
        
else:
    st.info("mapping functionality is about to be released")
    
