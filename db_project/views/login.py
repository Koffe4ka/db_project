import streamlit as st
import db_project.controllers.user_manager as um
def show_login():
    with st.form(key='user_login_form'):
        st.subheader("Vartotojo prisijungimas", anchor=False)
        user_name = st.text_input("Prisijungimo vardas", placeholder="įveskite vartotojo varda", autocomplete=None)
        user_password = st.text_input("Slaptažodis", type='password', autocomplete=None)
        if st.form_submit_button("Prisijungti"):
            if not user_name or not user_password:
                st.warning("Visi laukai yra privalomi")
            else:
                user = um.login(user_name, user_password)
                if user:
                    st.success(f"Sėkmingai prisijungėte kaip {user.name}")
                    st.session_state['user_login'] = True
                    st.session_state['current_user'] = user
                    st.session_state['show_login'] = False
                    st.rerun()
                else:
                    st.warning("Vartotojo vardas arba slaptažodis neteisingi.")
def show_registration():
    with st.form(key='user_register_form'):
        st.subheader("Vartotojo registracija", anchor=False)
        reg_user_name = st.text_input("Prisijungimo vardas", placeholder="sukurkite vartotojo varda", autocomplete=None)
        reg_name = st.text_input("Vardas", placeholder="įveskite savo vardą", autocomplete=None)
        reg_user_password = st.text_input("Slaptažodis", type='password', autocomplete=None)
        reg_user_password_confirm = st.text_input("Pakartokite slaptažodį", type='password', autocomplete=None)
        if st.form_submit_button("Registruotis"):
            if not reg_name or not reg_user_name or not reg_user_password or not reg_user_password_confirm:
                st.warning("Visi laukai yra privalomi")
            else:
                if reg_user_password == reg_user_password_confirm:
                    success = um.register(reg_user_name, reg_name, reg_user_password)
                    if success:
                        st.success("Sėkmingai užsiregistravote. Dabar galite prisijungti.")
                        st.session_state['show_register'] = False
                    else:
                        st.warning("Vartotojas jau egzistuoja.")
                else:
                    st.warning("Slaptažodžiai nesutampa.")
