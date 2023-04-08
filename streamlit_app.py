import streamlit as st
import streamlit_authenticator as stauth
#import yaml
#from yaml.loader import SafeLoader
import hydralit_components as hc
import pandas as pd
from src.settings import keboola_client, STATUS_TAB_ID

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

st.title('Firehouse Subs Mapper')

#st.write(st.secrets)

#with open('config.yaml') as file:
#    config = yaml.load(file, Loader=SafeLoader)

#st.write(type(config))
#st.write(config)
config_dict = {}

# remaining_keys = []


@st.cache_data
def read_df(table_id, index_col=None, date_col=None):
    keboola_client.tables.export_to_file(table_id, '.')
    table_name = table_id.split(".")[-1]
    return pd.read_csv(table_name, index_col=index_col, parse_dates=date_col)

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

authenticator = stauth.Authenticate(
    config_dict['credentials'],
    config_dict['cookie']['name'],
    config_dict['cookie']['key'],
    config_dict['cookie']['expiry_days'],
    config_dict['preauthorized']
)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

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

# accessing the values via session state    
# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')

if authentication_status:
        
    st.markdown("### Workflow Progress")
    
    cc = st.columns(3)
    
#    with cc[0]:
#        hc.info_card(content='Config(s) created' ,bar_value=100,sentiment='good', key='info1')

    with cc[0]:
     # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
        card1 = hc.info_card(content='Authorization done!', sentiment='good',bar_value=100)
        
    if st.session_state["username"]=='ondra':
        with cc[1]:
         hc.info_card(content='Data extracted', sentiment='bad',bar_value=100, key='info2')

    elif st.session_state["username"] == 'kritiga':
        with cc[1]:
         hc.info_card(content='Data extracted', sentiment='good',bar_value=100, key='info2')
    else:
        with cc[1]:
         hc.info_card(content='Data extracted', sentiment='neutral',bar_value=100, key='info2')
        
    with cc[2]:
     #customise the the theming for a neutral content
     hc.info_card(content='Mapping done',key='sec',bar_value=100,sentiment='bad')    

    st.markdown("### Action Items")

    st.markdown("1. Please **authorize** the configuration by clicking at [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    st.markdown("2. Please fill in **Company ID** and **Custom Calendar**")


    with st.form("myform"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("Please enter company ID:")
            ti = st.text_input(label="", label_visibility="collapsed")
            
        with col2:
            st.markdown("Custom calendar:")
            checkb = st.checkbox(label="")
            
        st.form_submit_button("Submit")
        
    # replace by classes
    classes = ['Paris', 'Prague', 'Berlin', 'Rome']
    
    # replace by locations
    locations = ['Italy', 'Czechia', 'Germany', 'France']
    
    #classes_col, locations_col = st.columns(2)
    #row = st.columns(1)

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
    