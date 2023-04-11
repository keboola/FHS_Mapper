import streamlit as st
#import pandas as pd
#from src.settings import STATUS_TAB_ID
from src.helpers import parse_credentials
from src.streamlit_widgets import WorkflowProgress, submit_form, submit_form2
import streamlit_authenticator as stauth

st.title('Firehouse Subs Mapper')

config_dict = parse_credentials()

authenticator = stauth.Authenticate(
    config_dict['credentials'],
    config_dict['cookie']['name'],
    config_dict['cookie']['key'],
    config_dict['cookie']['expiry_days'],
    config_dict['preauthorized']
)

        
with st.sidebar:
    name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
elif authentication_status == False:
    with st.sidebar:
        st.error('Username/password is incorrect')
elif authentication_status == None:
    with st.sidebar:
        st.warning('Please enter your username and password')

# stop the code flow if the authentication is not successful
if not authentication_status:
    st.stop()
       
st.markdown("### Workflow Progress")

wc = WorkflowProgress("ondra")
    
# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

submitted = submit_form()
    
if st.session_state.disabled:
    submit_form2()
        
    
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
