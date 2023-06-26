from src.settings import keboola_client, STATUS_TAB_ID
from src.settings import STREAMLIT_BUCKET_ID
import requests
import json
import streamlit as st
import pandas as pd
import datetime
import numpy as np

# https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/

@st.cache_data
def read_df(table_id, filter_col_name=None, filter_col_value=None, index_col=None, date_col=None, dtype=None):
    keboola_client.tables.export_to_file(table_id, '.')
    table_name = table_id.split(".")[-1]
    #st.write(filter_col_value)
    df = pd.read_csv(table_name, index_col=index_col, parse_dates=date_col, dtype=dtype)
    if filter_col_name:
        return df.loc[df[filter_col_name]==filter_col_value]
    else:
        return df

def determine_step(username):
    status_df = read_df(STATUS_TAB_ID, "entity_name", username)    
    authorization = status_df.loc[status_df["entity_name"]==username, "config_has_data"].values[0]
    report_tracking = (status_df.loc[status_df["entity_name"]==username, "report_tracking"].values[0])
    if authorization==1 or report_tracking=='None':
        step = 2
    else:
        step = 1
    return step    
    
#@st.cache_data
def parse_credentials():
    """
    The method takes credentials from streamlit secret and converts
    these into a dictionary compatible with streamlit authenticator

    expected composition of secret variable
    credentials_usernames_USERNAME_VARIABLE
    
    eg
    
    credentials_usernames_ondra_email = 'ondrej.svoboda@keboola.com'
    credentials_usernames_ondra_name = 'Ondřej Svoboda'
    credentials_usernames_ondra_password = 'xxx'

    this would be converted into 
    
    {"credentials":{
        "usernames":{
            "ondra":{
                "email": 'ondrej.svoboda@keboola.com',
                "name": 'Ondřej Svoboda', 
                "password": 'xxx'
                }
            }
        }}

    Returns
    -------
    config_dict - dictionary containing information about credentials formatted
    for stauth
    
    NOTE
    ----
    advanced features of stauth are not currently implemented beyond the simplest
    use. For instance, no preauthorized users or passwords expiry

    """
    config_dict = {}
    
    # 1. check the longest inner subscription
    
    # at this point, I do not check for preauthorized or cookies
    
    cred_keys = [key for key in st.secrets if "credentials" in key]
    
    for key in cred_keys:
        creds_dict = config_dict.get("credentials", dict())
        username_dict = creds_dict.get("usernames", dict())    
        username = key.split('-')[-2]
        key_end = key.split('-')[-1]
        user_dict =  username_dict.get(username, dict())
        user_dict[key_end] = st.secrets[key]
        username_dict[username] = user_dict
        creds_dict["usernames"] = username_dict
        config_dict["credentials"] = creds_dict
    
    config_dict["cookie"] = {'expiry_days':0,
                             'key':"random_signature_key",
                             'name':"random_cookie_name"}
    
    config_dict["preauthorized"] = {'emails':["melsby@gmail.com"]}
    
    return config_dict

def data_issues():
    st.error("""Downloading data from Quickbooks is not yet ready. Our team is monitoring the progress. 
             For more information, please check your inbox and look for ticket Request #27324 """)

def write_file_submit_authorization(status_df, 
                              company_id=None, 
                              financial_calendar=None, 
                              tracking_selection = None,
                              file_path=".dev_status.csv"):
    """
    

    Parameters
    ----------
    status_df : TYPE
        DESCRIPTION.
    company_id : TYPE
        DESCRIPTION.
    financial_calendar : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """  

    if not company_id:
        company_id = st.session_state.get("company_id", "").replace(" ","")
    
    if not financial_calendar:
        financial_calendar = st.session_state.get("custom_calendar", False)

    if not tracking_selection:
        tracking_selection = st.session_state.get('report_tracking',"")
    

    
    status_df["company_id"]=company_id
    status_df["custom_calendar"] = int(financial_calendar)
    status_df["authorization_timestamp"] = str(datetime.datetime.now())
    status_df["report_tracking"] = tracking_selection
    status_df.to_csv(file_path, index=False)
    
    return None
    #status_df[""]
         
def update_status_table(
        keboola_client=keboola_client,
        #keboola_key,
        table_id=STATUS_TAB_ID,
    #    bucket_id,
        file_path='.dev_status.csv',
        #primary_key='config_id',
        is_incremental=True, 
        delimiter=',',
        enclosure='"', 
        escaped_by='', 
        columns=['username'],
        without_headers=False
        ):
    
    #client = Client(keboola_URL, keboola_key)
    # check whether a table in the bucket exists. If so, retrieve its table_id
    
    res = keboola_client.tables.load(table_id=table_id,
                        file_path=file_path,
                        is_incremental=is_incremental, 
                        delimiter=delimiter,
                        enclosure=enclosure, 
                        escaped_by=escaped_by,
                        columns=columns,
                        without_headers=without_headers) 

    return res, f"table {table_id} has been updated."
    
    
def check_config_values():
    
    if (
            (st.session_state["company_id"]==st.session_state["company_id_old"]) or 
            (st.session_state["company_id_old"] in [None, ""])) and (
            (st.session_state["custom_calendar"]==st.session_state["custom_calendar_old"]) or
            (st.session_state["custom_calendar_old"]  in [None, ""])
        ) and (
            (st.session_state["report_tracking"]==st.session_state["report_tracking_old"]) or
            (st.session_state["report_tracking_old"]  in [None, ""])):
        return 1
    else:
        return 0
    
        
        
    # fill logic for custom calendar
def prepare_mapping_file(status_df, file_path='.mapping.csv'):
    
    username = status_df.entity_name.values[0]
    #class_{i}
    
    classes = sorted([ k for k in st.session_state.keys() if k.startswith('class_')])
    locations = sorted([ k for k in st.session_state.keys() if k.startswith('location_')])

   # old_classes = sorted([ k for k in st.session_state.keys() if k.startswith('old_class_')])
   # old_locations = sorted([ k for k in st.session_state.keys() if k.startswith('old_location_')])
    
    
    to_dict = []
    
    mapping_timestamp = str(datetime.datetime.now())
    for c, l in zip(classes, locations):
        inner_dict = {}
        inner_dict['entity_name'] = username
        inner_dict['class_dep'] = st.session_state[c]
        inner_dict['location'] = st.session_state[l]
        inner_dict['timestamp'] = mapping_timestamp
        to_dict.append(inner_dict)
        
    mapdf = pd.DataFrame(to_dict)
    mapdf.to_csv(file_path, index=False)
    return file_path

def create_or_update_table(table_name,
        keboola_client=keboola_client,
        bucket_id=STREAMLIT_BUCKET_ID,
        file_path='.mapping.csv',
        primary_key='xxx', # define primary key
        is_incremental=True, 
        delimiter=',',
        enclosure='"', 
        escaped_by='', 
        columns=["entity_name", "class_dep"],
        without_headers=False):
    """
    The function creates or incrementally updates the mapping table. 
    Mapping table should be keyed by hash(config_id+class)

    Parameters
    ----------
    table_name : TYPE
        DESCRIPTION.
    keboola_client : TYPE, optional
        DESCRIPTION. The default is keboola_client.
    bucket_id : TYPE, optional
        DESCRIPTION. The default is 'out.c-create_configs'.
    file_path : TYPE, optional
        DESCRIPTION. The default is '.mapping.csv'.
    primary_key : TYPE, optional
        DESCRIPTION. The default is 'xxx'.
    # define primary key        is_incremental : TYPE, optional
        DESCRIPTION. The default is False.
    delimiter : TYPE, optional
        DESCRIPTION. The default is ','.
    enclosure : TYPE, optional
        DESCRIPTION. The default is '"'.
    escaped_by : TYPE, optional
        DESCRIPTION. The default is ''.
    columns : TYPE, optional
        DESCRIPTION. The default is None.
    without_headers : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    # check whether a table in the bucket exists. If so, retrieve its table_id
    try:
        try:
            tables = keboola_client.tables.list()

        except Exception as e:
            return str(e)
        # there will be 0 or 1 hit
        table_def = list(filter(lambda x: x['bucket']['id']==bucket_id and x['name']==table_name, tables))
        if table_def:
            table_id = table_def[0]['id']
            # table already exists --> load
            try:
                _= keboola_client.tables.load(table_id=table_id,
                                    file_path=file_path,
                                    is_incremental=is_incremental, 
                                    delimiter=delimiter,
                                    enclosure=enclosure, 
                                    escaped_by=escaped_by,
                                    columns=columns,
                                    without_headers=without_headers) 
                return True, f"{table_name} table has been updated."
            except Exception as e:
                return False, str(e)    
        else:
            # table does not exist --> create
            try:
                return True, keboola_client.tables.create(name=table_name,
                                    bucket_id=bucket_id,
                                    file_path=file_path,
                                    primary_key=columns) + " table has been successfully created!!"
            except Exception as e:
                return False, str(e)   
    except Exception as e:
        return False, str(e)     

def trigger_flow(api_token, config_id, component_name):
    headers = {
        'accept': 'application/json',
        'X-KBC-RunId': '',  # Set the appropriate run ID if available
        'X-StorageApi-Token': api_token,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "component": component_name,
        "mode": "run",
        "config": config_id
    })

    url = "https://queue.keboola.com/jobs"
    try:
        # Check if a job is already running for the config_id
        if is_job_running(api_token, config_id):
            print("A job is already running for the current config_id. Skipping job creation.")
            return None

        # Create a new job
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            job_data = response.json()
            run_id = job_data.get("id")
            print("Flow for mapping is triggered")
            return response.json()
        else:
            print(f"Error - Response code: {response.status_code}, JSON: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error - {e}")

def is_job_running(api_token, config_id):
    headers = {
        'accept': 'application/json',
        'X-StorageApi-Token': api_token,
    }
    url = f"https://queue.keboola.com/jobs"
    try:
        response = requests.get(url, headers=headers, params={"config": config_id, "status": "running"})
        if response.status_code == 200:
            job_data = response.json()
            return len(job_data) > 0
        else:
            print(f"Error - Response code: {response.status_code}, JSON: {response.json()}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error - {e}")
        return False
