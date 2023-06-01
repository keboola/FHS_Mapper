import streamlit as st
import streamlit.components.v1 as components
from src.helpers import write_file_submit_authorization
from src.helpers import update_status_table
from src.helpers import check_config_values
from src.helpers import prepare_mapping_file
from src.helpers import create_or_update_table
from src.helpers import read_df
from src.settings import RESTAURANTS_TAB_ID, MAPPING_TAB_ID
import hydralit_components as hc
import webbrowser
from st_click_detector import click_detector
import pandas as pd
import datetime
import numpy as np

restaurants_df = read_df(RESTAURANTS_TAB_ID)
mapping_df = read_df(MAPPING_TAB_ID)

class WorkflowProgress():
    theme_bad = {'bgcolor': '#FFF0F0','progress_color': 'red', 'title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}
    theme_inprogress = {'bgcolor': '#F8C471','progress_color': 'black', 'title_color': 'black','content_color': 'black','icon_color': 'black', 'icon': 'fa fa-cog'}
    theme_neutral = {'bgcolor': '#f9f9f9','progress_color': 'orange', 'title_color': 'orange','content_color': 'orange','icon_color': 'orange', 'icon': 'fa fa-question-circle'}
    theme_good = {'bgcolor': '#EFF8F7','progress_color': 'green', 'title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
    
    def __init__(self, user):
        self.user = user
        self.columns = st.columns(2)
        self.authorization_sentiment = st.session_state.authorization_sentiment
        #self.data_sentiment = st.session_state.data_sentiment
        self.mapping_sentiment = st.session_state.mapping_sentiment
        #self._update_sentiments()
        self._prepare_progress_widget()
        
        
        
    def _prepare_progress_widget(self):
        
        with self.columns[0]:
            self.info_card = hc.info_card(content='Authorization', theme_override=self.authorization_sentiment, bar_value=100, key='auth_card')
    #    with self.columns[1]:
    #        hc.info_card(content='Data extracted', theme_override=self.data_sentiment, bar_value=100, key='data_card')
        with self.columns[1]:
            hc.info_card(content='Mapping', theme_override=self.mapping_sentiment, bar_value=100, key='map_card')    
    
        
def disable():
    st.session_state.disabled = True

def clicked():
    st.session_state.clicked = True

def clicked_submit():
    st.session_state.clicked_submit = True

def clicked_auth():
    st.session_state.clicked_auth = True



def open_url(url='www.google.com'):
    #webbrowser.open(url, 2)
    webbrowser.open_new_tab(url)
        
        #self.authorization_sentiment='good'
def submit_form(status_df):
    
        with st.form("submitform"):

            if not pd.isna(status_df["company_id"].values[0]):
                st.warning("The Quickbooks Company ID and Authorization is already done! Please proceed only if you want to update the Company ID")


            st.markdown("1. Please fill in your **Quickbooks Company ID** and select the **Accounting Calendar** you are using and the method of **Report tracked** from the drop-down")

            
            tracking_selection = st.selectbox(label = 'How do you track your restaurants in QuickBooks?',options=('By Class', 'By Location', 'One Account per Restaurant'),key="tracking_selection")
            if st.session_state["tracking_selection"] == 'By Class':
                report_tracking = 'Class'
                st.session_state["report_tracking"] = 'Class'
            if st.session_state["tracking_selection"] == 'By Location':
                report_tracking = 'Department'
                st.session_state["report_tracking"] = 'Department'
            else:
                report_tracking = 'None'
                st.session_state["report_tracking"] = 'None'
            
            col1, col2 = st.columns(2)
        


            with col1:
                st.text_input(label="Quickbooks Company ID:",  key='company_id')


                
            with col2:
                #st.markdown("Select Calendar Type:")
                #st.checkbox(label="custom_cal_check", key="custom_calendar", label_visibility="collapsed")

                #st.checkbox(label="custom_cal_check", key="custom_calendar")
                
                calendar_selection = st.selectbox(label = 'Accounting Calendar',options=('Calendar (Jan 1- Dec 31)', 'Fiscal Calendar (Period 4-4-5)'),key="calendar_selection")
                if st.session_state["calendar_selection"] == 'Fiscal Calendar (Period 4-4-5)':
                    custom_calendar = 1
                    st.session_state["custom_calendar"] = 1
                else:
                    custom_calendar = 0
                    st.session_state["custom_calendar"] = 0

         
                #st.markdown("Select Calendar Type:")
                #st.checkbox(label="custom_cal_check", key="custom_calendar", label_visibility="collapsed")

                #st.checkbox(label="custom_cal_check", key="custom_calendar")
                

            #if st.session_state['custom_calendar']:
            #    st.session_state['custom_calendar']=1

            
            #submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
            st.write("_You will have the **Company ID** in the format **9130 3565 4172 6086**, please enter without spaces  eg: **9130356541726086**_")
            submitted = st.form_submit_button("Submit", on_click=clicked_submit)
            

            ChangeButtonColour('Submit', 'black', '#F8C471') # button txt to find, colour to assign

            if submitted:
                val_status = check_config_values()
                st.session_state.clicked_auth = False
                #st.write(f"st.session_state.clicked_auth {st.session_state.clicked_auth}")
                if val_status == 0:
                    st.warning(
                        f"""You are trying to replace previously input values (company_id = {st.session_state['company_id_old']}
                            and {st.session_state['custom_calendar_old']}) for new values (company_id = {st.session_state['company_id']} and {int(st.session_state['custom_calendar'])}). If this is not desired, 
                            please change the values in the form and click "Submit" again.
                        """
                        )
                else:
                    st.info(f"You have entered: a company ID = {st.session_state.company_id} and Financial Calendar = {int(st.session_state.custom_calendar)}")
               
                #write_file_submit_authorization(status_df)
            return submitted

            
def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)

def render_clickable_link(url, status_df):
    with st.container():
        #st.session_state.clicked_auth = False
        content = f'''
                    <p>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. &nbsp;&nbsp;&nbsp;&nbsp;Please click at the hyperlink to access authorization wizard <a href="{url}" id='Link code' target="_blank" style="sans serif" >QuickBooks</a>.</p>
                    '''
        
        clicked_auth = click_detector(content, key="clicked_auth")
        
        if clicked_auth:
            #st.session_state.clicked_auth = False
            write_file_submit_authorization(status_df)
            status_df.loc[:, ["entity_name", "config_id"]].to_csv(".flow2trigger.csv", index=False)
            # here instead I will have the api call to call the config / orchestration
            
            res, message = create_or_update_table("flow2_trigger_tab", file_path=".flow2trigger.csv",is_incremental=False,columns=None)
            
            if not res:
                print("trying to create trigger table:" + message)
            res, _ = update_status_table()
            
            if 'company_id' in st.session_state.keys():
                st.session_state['company_id_old'] = st.session_state['company_id']
                
            if 'custom_calendar' in st.session_state.keys():
                st.session_state['custom_calendar_old'] = int(st.session_state['custom_calendar'])

            if 'report_tracking' in st.session_state.keys():
                st.session_state['report_tracking_old'] = (st.session_state['report_tracking'])


            #st.write("checking response", res)
            st.success("QuickBooks account authorization is in progress. Please log out and wait for an email notification to proceed (if you do not receive it shortly, please check also your spam folder).")
            st.cache_data.clear()

        else:
            st.warning("The link is yet to be clicked")
        
def render_selectboxes(mapping_values_classes, status_df,entity_name, debug=False):
    mapping_values_classes = np.sort(mapping_values_classes)
    mapping_values_classes = np.append(mapping_values_classes,"NA")
    if status_df["report_tracking"].isna().all():
        st.warning(f"WARNING: No data are available for Quickbooks Company ID {status_df.company_id.values[0]}.")

    if (status_df["report_tracking"]=='None').all():
        st.markdown(f"There are no further actions needed from your end for Quickbooks Company ID **{status_df.company_id.values[0]}**.")
    
    if (status_df["report_tracking"].isin(['Class','Department'])).all() : 
        with st.form("mapping_form"):
            st.markdown("**Please put together related locations and classes:**")
            col1, col2 = st.columns(2)
            
        #mapping_values_classes = list(range(0, 3))
            if mapping_values_classes.shape[0]>0:
                nmapping = mapping_values_classes.shape[0]
            else:
                nmapping = 3
                
            if len(mapping_values_classes)==0:
                st.warning(f"WARNING: No data are available for Quickbooks Company ID {status_df.company_id.values[0]}.")
            
            if debug:
                license_number='Jason_Steele' 
                st.warning("DEBUG MODE TURNED ON")
            

            mapping_values_locations = restaurants_df.loc[restaurants_df.entity_name==str(entity_name), "Restaurant"].values.tolist() 
            mapping_values_locations = sorted(list(set(mapping_values_locations)))
            
            
            with col1:
                st.markdown("**Restaurant name**")

            
            with col2:
                st.markdown("**Class or Location**")

            
            #nmapping = mapping_values_classes.shape[0]
            
            for i in range(nmapping):
                    with col1:
                        st.selectbox("loc", mapping_values_locations, index=i,  key=f"location_{i}", label_visibility='collapsed', disabled=True)

                    with col2:
                        st.selectbox("cls", mapping_values_classes, index=i, key=f"class_{i}", label_visibility='collapsed')


            text_area = st.text_area("If there are any issues with data or you have any concerns, please fill in the following text area.", key="text_area")
            text_df = pd.DataFrame([{'entity_name':entity_name, 'message':text_area, 'timestamp':str(datetime.datetime.now())}])
            text_df.to_csv('.text.csv', index=False)
            
            submitted = st.form_submit_button("Submit")
            ChangeButtonColour('Submit', 'black', '#F8C471') # button txt to find, colour to assign
            if submitted:
                path = prepare_mapping_file(status_df)
                result, message=create_or_update_table('mapping', file_path=path)
                result2, message2=create_or_update_table('text_messages', file_path='.text.csv', columns=['entity_name'])

                if result and result2:
                    st.success(message)

                else:
                    print(message)
                    print(message2)
                    st.error("Something is going wrong, please contact admins.")
