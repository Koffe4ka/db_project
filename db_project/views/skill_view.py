import streamlit as st
import pandas as pd
from time import sleep
import db_project.controllers.user_manager as um
import db_project.controllers.skills_manager as sm

def add_skill():
    st.subheader("Pridėti įgūdžius", anchor=False)

    if 'skill_added' not in st.session_state:
        st.session_state['skill_added'] = None

    with st.form(key='add_skill_form', clear_on_submit=True): 
        name = st.text_input("Skill title")
        description = st.text_area("Description")
        levels = {level.id: level.name for level in sm.get_levels()}
        option = st.selectbox("Lygis", levels, format_func=lambda x: levels[x])

        submitted = st.form_submit_button('Add skill')
        if submitted:
            if name and description and option in levels:
                user_id = st.session_state['current_user'].id
                sm.add_skill(user_id, name, description, option)
                st.session_state['skill_added'] = (name, levels[option]) 
                st.success(f"Skill '{name}' added successfully at level '{levels[option]}'.") 
                st.rerun()
    if st.session_state['skill_added']:
        skill_name, skill_level = st.session_state['skill_added']
        st.success(f"Skill '{skill_name}' added successfully at level '{skill_level}'.")
        st.session_state['skill_added'] = None


def show_my_skills():
    st.subheader("Mano įgūdžiai", anchor=False)
    current_user = st.session_state.get('current_user')

    if current_user:
        user_id = current_user.id
        skills = sm.get_user_skills(user_id)

        if skills:
            skill_data = {
                'Select': [False] * len(skills),
                'Name': [skill.name for skill in skills],
                'Description': [skill.description for skill in skills],
                'Level': [skill.level.name for skill in skills],
                'Pt to Next Level': [sm.points_to_next_level(skill.level.name) for skill in skills]
            }
            df_skills = pd.DataFrame(skill_data)

            edited_skills = st.data_editor(df_skills, num_rows="fixed", key="skill_table", hide_index=True, disabled=("Name", "Description", "Level", "Pt to Next Level"))

            if st.button("Remove Selected Skills"):
                ids_to_remove = [skills[i].id for i in range(len(skills)) if edited_skills['Select'][i]]
                for skill_id in ids_to_remove:
                    sm.delete_skill(skill_id, user_id)
                st.success("Selected skills removed successfully.")
                sleep(0.5)
                st.rerun()
        else:
            st.write("No skills yet")
            if st.button("Add skill?", key='addskill2'):
                st.session_state['current_page'] = 'add-skill'
                st.rerun()
    else:
        st.write("User not logged in")
