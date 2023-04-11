import streamlit as st
import pandas as pd
from src.settings import STATUS_TAB_ID
from src.helpers import read_df, authenticator
from src.streamlit_widgets import WorkflowProgress, submit_form

st.title('Firehouse Subs Mapper')

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

st.markdown("### Action Items")

st.markdown("1. Please **authorize** the configuration by clicking at [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
st.markdown("2. Please fill in **Company ID** and **Custom Calendar**")
    
submit_form()

# replace by classes
classes = ['Paris', 'Prague', 'Berlin', 'Rome']

# replace by locations
locations = ['Italy', 'Czechia', 'Germany', 'France']

st.markdown("**Status Table**")       
status_df = read_df(STATUS_TAB_ID).head(3)
st.dataframe(status_df)
st.markdown("**Mapping Table**")

df = pd.DataFrame(
    {"select mapping": locations}
)
df["select mapping"] = (
    df["select mapping"].astype("category"))

s = df.style

cell_color = pd.DataFrame([True, True, True, True],
                          index=df.index,
                          columns=df.columns)
s.set_td_classes(cell_color)

df.index=classes

edited_df = st.experimental_data_editor(df, width=1000)
