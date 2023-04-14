#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:15:39 2023

@author: ondrejsvoboda
"""

import streamlit as st
import streamlit.components.v1 as components

import hydralit_components as hc
import webbrowser
from st_click_detector import click_detector

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

def open_url(url='www.google.com'):
    #webbrowser.open(url, 2)
    webbrowser.open_new_tab(url)
        
        #self.authorization_sentiment='good'
def submit_form():
    
        with st.form("submitform"):
            st.markdown("1. Please fill in your **Quickbooks Company ID** and if you are using a financial calendar, then select the checkbox below **Using Financial Calendar**")

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("Quickbooks Company ID:")
                st.text_input(label="aaa", label_visibility="collapsed", key='company_id')
                
            with col2:
                st.markdown("Using Financial Calendar:")
                st.checkbox(label="", key='custom_calendar')
                
#            submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
            submitted = st.form_submit_button("Submit", on_click=clicked)

            ChangeButtonColour('Submit', 'black', '#F8C471') # button txt to find, colour to assign

            if submitted:
               st.info(f"You have entered: a company ID = {st.session_state.company_id} and Financial Calendar = {st.session_state.custom_calendar}")
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

def render_clickable_link(url):
    with st.container():
        content = f'''
                    <p>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. &nbsp;&nbsp;&nbsp;&nbsp;Please click here to authorize to access <a href="{url}" id='Link code' target="_blank" style="sans serif" >QuickBooks</a>.</p>
                    '''
        clicked = click_detector(content)
        
        if clicked:
            st.success("QuickBooks account has been authorized")
        else:
            st.warning("The link is yet to be clicked")
        
def render_selectboxes(n_select=3):
    with st.form("mapping_form"):
        st.markdown("**Please put together related locations and classes:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Location**")
        
        with col2:
            st.markdown("**Class**")
        
        
        for i in range(n_select):
            with st.container():
                with col1:
                    st.selectbox("", [i for i in range(n_select)], index=i, key=f"select{i}1", label_visibility='collapsed', disabled=True)
                with col2:
                    st.selectbox("", [i for i in range(n_select)], key=f"select{i}2", label_visibility='collapsed')

        submitted = st.form_submit_button("Submit")
        ChangeButtonColour('Submit', 'black', '#F8C471') # button txt to find, colour to assign
        if submitted:
            st.success("Classes and locations have been mapped.")
