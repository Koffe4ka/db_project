import streamlit as st
from time import sleep
import pandas as pd
import sqlalchemy
import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# streamlit run db_project/main.py

USER_DB = {
    "admin": {"name": "Admin User", "password": "adminpass"},
    "user1": {"name": "User One", "password": "user1pass"}
}

def authenticate_user(username, password):
    user = USER_DB.get(username)
    if user and user["password"] == password:
        return user
    return None

def register_user(username, name, password):
    if username in USER_DB:
        return False 
    USER_DB[username] = {"name": name, "password": password}
    return True

if 'user_login' not in st.session_state:
    st.session_state['user_login'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None


if st.session_state['user_login']:
    st.title("Vartotojo paskyra", anchor=False)
    st.subheader("Jusu igudziai :sunglasses:", anchor=False)
    st.sidebar.success(f"Prisijungęs vartotojas: {st.session_state['current_user']['name']}")
    if st.sidebar.button("Atsijungti"):
        st.session_state['user_login'] = False
        st.session_state['current_user'] = None
        st.rerun()
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
        with st.form(key='user_login_form'):
            st.subheader("Vartotojo prisijungimas", anchor=False)
            ent_user_name = st.text_input("Prisijungimo vardas", placeholder="įveskite vartotojo varda", autocomplete=None)
            ent_user_password = st.text_input("Slaptažodis", type='password', autocomplete=None)
            if st.form_submit_button("Prisijungti"):
                user_name = ent_user_name
                user_password = ent_user_password
                user = authenticate_user(user_name, user_password)
                if user:
                    st.success(f"Sėkmingai prisijungėte kaip {user['name']}")
                    sleep(0.5)
                    st.session_state['user_login'] = True
                    st.session_state['current_user'] = user
                    st.session_state['show_login'] = False
                    st.rerun()
                else:
                    st.warning("Vartotojo vardas arba slaptažodis neteisingi.")

    if st.session_state['show_register']:
        with st.form(key='user_register_form'):
            st.subheader("Vartotojo registracija", anchor=False)
            reg_user_name = st.text_input("Prisijungimo vardas", placeholder="sukurkite vartotojo varda", autocomplete=None)
            reg_name = st.text_input("Vardas", placeholder="įveskite savo vardą", autocomplete=None)
            reg_user_password = st.text_input("Slaptažodis", type='password', autocomplete=None)
            reg_user_password_confirm = st.text_input("Pakartokite slaptažodį", type='password', autocomplete=None)
            if st.form_submit_button("Registruotis"):
                if reg_user_password == reg_user_password_confirm:
                    success = register_user(reg_user_name, reg_name, reg_user_password)
                    if success:
                        st.success("Sėkmingai užsiregistravote. Dabar galite prisijungti.")
                        st.session_state['show_register'] = False
                    else:
                        st.warning("Vartotojo vardas jau egzistuoja.")
                else:
                    st.warning("Slaptažodžiai nesutampa.")