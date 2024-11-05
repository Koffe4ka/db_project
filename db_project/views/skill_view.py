import streamlit as st
import db_project.controllers.user_manager as um
import db_project.controllers.skills_manager as sm

def add_skill():
    st.write("PLEASE ADD YOUR SKILL")
    name = st.text_input("Skill title")
    description = st.text_area("Description")
    levels = {level.id:level.name for level in sm.get_levels()}
    option = st.selectbox("Lygis",levels, format_func=lambda x: levels[x])

    if st.button('Add skill',key='addskill'):
        if name and description and levels and option in levels:
            ...


def show_my_skills():
    ...

def remove_skill():
    ...


