import streamlit as st
import db_project.controllers.user_manager as um
def navigation():
    
    st.subheader(f"Sveiki prisijungę, {st.session_state['current_user'].name} :sunglasses:", anchor=False)
    
    
    st.sidebar.success(f"Prisijungęs vartotojas: {st.session_state['current_user'].name}")
    if st.sidebar.button("Home"):
        st.session_state['current_page'] = 'home'
    if st.sidebar.button("Add skill"):
        st.session_state['current_page'] = 'add-skill'
    if st.sidebar.button("Create course"):
        st.session_state['current_page'] = 'add-course'
    if st.sidebar.button("My created courses"):
        st.session_state['current_page'] = 'my-courses'
    if st.sidebar.button("Available courses"):
        st.session_state['current_page'] = 'available-courses'
    if st.sidebar.button("Course History"):
        st.session_state['current_page'] = 'history'
















    if st.sidebar.button("Atsijungti"):
        if um.logout(st.session_state['current_user'].username):
            st.session_state['current_user'] = None
            st.rerun()
        else:
            st.write("Įvyko klaida. Vartotojas nerastas arba neprisijunges.")