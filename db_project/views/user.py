import streamlit as st
import db_project.controllers.user_manager as um
def navigation():
    st.title("Vartotojo paskyra", anchor=False)
    st.subheader("Jusu igudziai :sunglasses:", anchor=False)
    st.sidebar.success(f"Prisijungęs vartotojas: {st.session_state['current_user'].name}")
    if st.sidebar.button("Atsijungti"):
        if um.logout(st.session_state['current_user'].username):
            st.session_state['current_user'] = None
            st.rerun()
        else:
            st.write("Įvyko klaida. Vartotojas nerastas arba neprisijunges.")