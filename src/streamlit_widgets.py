#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:15:39 2023

@author: ondrejsvoboda
"""

import streamlit as st
import hydralit_components as hc

class WorkflowProgress():

    def __init__(self, user):
        self.user = user
        self.columns = st.columns(3)
        self.authorization_sentiment = 'neutral'
        self.data_sentiment = 'neutral'
        self.mapping_sentiment = 'neutral'
        self._update_sentiments()
        self._prepare_progress_widget()
        
    def _prepare_progress_widget(self):
        
        with self.columns[0]:
            self.info_card = hc.info_card(content='Authorization done!', sentiment=self.authorization_sentiment,bar_value=100, key='auth_card')
        with self.columns[1]:
            hc.info_card(content='Data extracted', sentiment=self.data_sentiment, bar_value=100, key='data_card')
        with self.columns[2]:
            hc.info_card(content='Mapping done', sentiment=self.mapping_sentiment, bar_value=100, key='map_card')    

    def _update_sentiments(self):
        """
        THIS METHOD SHOULD UPDATE THE WORKFLOW PROGRESS BASED ON NEW INFORMATION
        COMING FROM STATUS TABLE

        Returns
        -------
        None.

        """
        self.authorization_sentiment='neutral'
    
        
def disable():
    st.session_state.disabled = True
        
        #self.authorization_sentiment='good'
def submit_form():
    
        with st.form("submitform"):
            st.markdown("1. Please fill in your **Company ID** and if you are using a financial calendar, then select the checkbox below **Financial Calendar**")

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("Company ID:")
                st.text_input(label="aaa", label_visibility="collapsed", key='company_id')
                
            with col2:
                st.markdown("Financial Calendar:")
                st.checkbox(label="", key='custom_calendar')
                
            submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
            if submitted:
               st.info(f"You have entered: a company ID = {st.session_state.company_id} and Financial Calendar = {st.session_state.custom_calendar}")
            return submitted
    
            
def submit_form2():
            
    with st.form("submitform2"):
        st.markdown("2. Now, please **authorize** the configuration by clicking at the buttom below")
            
        submitted = st.form_submit_button("Authorize", on_click=disable)
        if submitted:
            st.success("The configuration has been authorized. Now, data will be downloaded from Quickbooks.")
