import streamlit as st
#import pandas as pd
#from src.settings import STATUS_TAB_ID
from src.helpers import parse_credentials, data_issues
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

    #st.title('Quickbooks Automation Setup')
    st.markdown('## **QUICKBOOKS AUTOMATION SETUP**')

    STEP = st.selectbox("[MOCK ONLY] select workflow step", [1, 2])

    name, authentication_status, username = authenticator.login('Login', 'main')

#----------------------------------------------------------
if STEP == 1:
    st.session_state.authorization_sentiment = WorkflowProgress.theme_inprogress
    st.session_state.mapping_sentiment = WorkflowProgress.theme_neutral

# if STEP == 2:
#     st.session_state.authorization_sentiment = WorkflowProgress.theme_good
#     st.session_state.data_sentiment = WorkflowProgress.theme_good
#     st.session_state.mapping_sentiment = WorkflowProgress.theme_neutral

if STEP == 2:
    st.session_state.authorization_sentiment = WorkflowProgress.theme_good
    st.session_state.mapping_sentiment = WorkflowProgress.theme_inprogress
#----------------------------------------------------------


if authentication_status:
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout', 'main')
elif authentication_status == False:
    with st.sidebar:
        st.error('Username/password is incorrect')
elif authentication_status == None:
    with st.sidebar:
        st.warning('Please enter your username and password')

# stop the code flow if the authentication is not successful
if not authentication_status:
    st.stop()
       
#st.markdown("### Workflow Progress")

wc = WorkflowProgress("ondra")

if STEP == 1:    
    # Initialize disabled for form_submit_button to False
    if "clicked" not in st.session_state:
        st.session_state.clicked = False
    
    submitted = submit_form()
        
    if st.session_state.clicked:
        render_clickable_link("https://www.firehousesubs.com/")
        #submit_form2()
elif STEP == 2:
    #st.write("fix data issues")
    data_issues()
    render_selectboxes()
    
else:
    st.info("mapping functionality is about to be released")
    
# # replace by classes
# classes = ['Paris', 'Prague', 'Berlin', 'Rome']

# # replace by locations
# locations = ['Italy', 'Czechia', 'Germany', 'France']

# st.markdown("**Status Table**")       
# status_df = read_df(STATUS_TAB_ID).head(3)
# st.dataframe(status_df)
# st.markdown("**Mapping Table**")

# df = pd.DataFrame(
#     {"select mapping": locations}
# )
# df["select mapping"] = (
#     df["select mapping"].astype("category"))

# s = df.style

# cell_color = pd.DataFrame([True, True, True, True],
#                           index=df.index,
#                           columns=df.columns)
# s.set_td_classes(cell_color)

# df.index=classes

# edited_df = st.experimental_data_editor(df, width=1000)
