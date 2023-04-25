#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:15:39 2023

@author: ondrejsvoboda
"""

import streamlit as st
import streamlit.components.v1 as components
from src.helpers import write_file_submit_authorization
from src.helpers import update_status_table
from src.helpers import check_config_values
from src.helpers import prepare_mapping_file
from src.helpers import create_or_update_mapping
from src.helpers import read_df
from src.settings import RESTAURANTS_TAB_ID, MAPPING_TAB_ID
import hydralit_components as hc
import webbrowser
from st_click_detector import click_detector

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
            st.markdown("1. Please fill in your **Quickbooks Company ID** and if you are using a financial calendar, then select the checkbox below **Using Financial Calendar**")

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("Quickbooks Company ID:")
                st.text_input(label="aaa", label_visibility="collapsed", key='company_id')
                
            with col2:
                st.markdown("Using Financial Calendar:")
                st.checkbox(label="", key='custom_calendar')
            
            #if st.session_state['custom_calendar']:
            #    st.session_state['custom_calendar']=1
            
#            submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
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
                    <p>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. &nbsp;&nbsp;&nbsp;&nbsp;Please click at the hyperlink to authorize the access to <a href="{url}" id='Link code' target="_blank" style="sans serif" >QuickBooks</a>.</p>
                    '''
        
        clicked_auth = click_detector(content, key="clicked_auth")
        
        if clicked_auth:
            #st.session_state.clicked_auth = False
            write_file_submit_authorization(status_df)

            res, _ = update_status_table()
            
            if 'company_id' in st.session_state.keys():
                st.session_state['company_id_old'] = st.session_state['company_id']
                
            if 'custom_calendar' in st.session_state.keys():
                st.session_state['custom_calendar_old'] = int(st.session_state['custom_calendar'])


            #st.write("checking response", res)
            st.success("QuickBooks account has been authorized")
        else:
            st.warning("The link is yet to be clicked")
        
def render_selectboxes(mapping_values_classes, status_df):
    with st.form("mapping_form"):
        st.markdown("**Please put together related locations and classes:**")
        col1, col2 = st.columns(2)
        
        config_id = status_df.config_id.values[0]
        current_mapping = mapping_df.loc[mapping_df.config_id=='957469662', ["class_dep", "location"]]
        #current_mapping = mapping_df.loc[mapping_df.config_id==config_id, ["class_dep", "location"]]

        #st.write(current_mapping)
        
        
        #mapping_values_classes = list(range(0, 3))
        if mapping_values_classes.shape[0]>0:
            nmapping = mapping_values_classes.shape[0]
        else:
            nmapping = 3
            
        if len(mapping_values_classes)==0:
            st.warning(f"WARNING: No data are available for Quickbooks Company ID {status_df.company_id.values[0]}.")
        
        mapping_values_locations = ["NA"] + restaurants_df.CenterName.values.tolist() 
        mapping_values_locations = sorted(list(set(mapping_values_locations)))
        idx = mapping_values_locations.index("NA")
        
        with col1:
            st.markdown("**Class or Department**")
        
        with col2:
            st.markdown("**Location**")
        
        #nmapping = mapping_values_classes.shape[0]
        
        for i in range(nmapping):
                with col1:
                    st.selectbox("cls", mapping_values_classes, index=i, key=f"class_{i}", label_visibility='collapsed', disabled=True)
                with col2:
                    st.selectbox("loc", mapping_values_locations, index=idx,  key=f"location_{i}", label_visibility='collapsed')

        submitted = st.form_submit_button("Submit")
        ChangeButtonColour('Submit', 'black', '#F8C471') # button txt to find, colour to assign
        if submitted:
            path = prepare_mapping_file(status_df)
            result, message=create_or_update_mapping('mapping', file_path=path)
            if result:
                st.success(message)
            else:
                print(message)
                st.error("Something is going wrong, please contact admins.")
