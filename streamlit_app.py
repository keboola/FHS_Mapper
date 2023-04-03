import streamlit as st
import streamlit_authenticator as stauth
#import yaml
#from yaml.loader import SafeLoader
import hydralit_components as hc
import pandas as pd

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

st.title('Firehouse Subs Mapper')

#st.write(st.secrets)

#with open('config.yaml') as file:
#    config = yaml.load(file, Loader=SafeLoader)

#st.write(type(config))
#st.write(config)
config_dict = {}

# remaining_keys = []


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


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
#    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
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
        
    st.header("Workflow Progress")
    
    cc = st.columns(4)
    
    with cc[0]:
     # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
        card1 = hc.info_card(content='Authorization done!', sentiment='good',bar_value=100)
    
    with cc[1]:
        hc.info_card(content='Config created' ,bar_value=100,sentiment='neutral', key='info1')
    
    if st.session_state["username"]=='ondra':
        st.write(f"hi {st.session_state['username']}")
        with cc[2]:
         hc.info_card(content='Data extracted', sentiment='bad',bar_value=100, key='info2')

    elif st.session_state["username"] == 'kritiga':
        st.write(f"hi {st.session_state['name']}")
        with cc[2]:
         hc.info_card(content='Data extracted', sentiment='good',bar_value=100, key='info2')
    else:
        st.write(f"hi {st.session_state['username']}")

        with cc[2]:
         hc.info_card(content='Data extracted', sentiment='neutral',bar_value=100, key='info2')
        
    with cc[3]:
     #customise the the theming for a neutral content
     hc.info_card(content='Maybe...',key='sec',bar_value=100,sentiment='bad')    

    st.header("Mapping")



    # replace by classes
    classes = ['Paris', 'Prague', 'Berlin', 'Rome']
    
    # replace by locations
    locations = ['Italy', 'Czechia', 'Germany', 'France']
    
    #classes_col, locations_col = st.columns(2)
    #row = st.columns(1)
       
    
    
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
    