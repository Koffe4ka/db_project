import streamlit as st
from time import sleep
import pandas as pd
import sqlalchemy
import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from db_project.controllers.user_manager import login, register, logout
from db_project.db_setup import init_db
import db_project.views.user as user_view
import db_project.views.login as login_view

init_db()

if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None


if st.session_state['current_user']:
    user_view.navigation()
else:
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
        st.title("Programėlė", anchor=False)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registruotis", key="reg", icon=":material/app_registration:"):
            st.session_state['show_register'] = True
            st.session_state['show_login'] = False
    with col2:
        if st.button("Prisijungti", key="log", icon=":material/passkey:"):
            st.session_state['show_login'] = True
            st.session_state['show_register'] = False


    if st.session_state['show_login']:
        login_view.show_login() 
    if st.session_state['show_register']:
        login_view.show_registration()