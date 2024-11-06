import streamlit as st
import pandas as pd
from time import sleep
import db_project.controllers.user_manager as um
import db_project.controllers.skills_manager as sm

def add_skill():
    st.subheader("Pridėti įgūdžius", anchor=False)

    if 'skill_added' not in st.session_state:
        st.session_state['skill_added'] = None

    with st.form(key='add_skill_form'): 
        st.markdown(
            """ :grey[*Reikalavaimai:  
                    * Naudokite tik raides ir tarpus   
                    * Pavadinimo ilgis nuo 3 iki 255 simbolių  
                    * Pavadinimas turi prasidėti didžiąją raide*]""")
        name = st.text_input("Skill title", max_chars=255)
        if name:
            if not all(char.isalpha() or char.isspace() for char in name):
                st.error("Įgūdžio pavadinimas gali būti tik raidžių")
            elif len(name.strip()) < 3:
                st.error("Pavadinimas turėtų turėti mažiausiai 3 simbolius")
            elif not name[0].isupper():
                st.error("Pavadinimas prasideda iš didžiosios raidės")
        
        st.markdown(""" :grey[*Reikalavaimai:   
                    * Aprašymas netrumpesnis nei 10 simbolių bei neilgesnis nei 500  
                    * Pavadinimas turi prasidėti didžiąją raide*]""")
        description = st.text_area("Description", max_chars=500)
        if description:
            if len(description.strip()) <10:
                st.error("Įgūdžio aprašymas turėtu būti netrumpesnis nei 10 simbolių")
            elif not description[0].isupper():
                st.error("Aprašymas pradedamas didžiąją raide")
        levels = {level.id: level.name for level in sm.get_levels()}
        option = st.selectbox("Lygis", levels, format_func=lambda x: levels[x])

        submitted = st.form_submit_button('Add skill')
        if submitted:
            is_valid_title = (
                name 
                and all(char.isalpha() or char.isspace() for char in name)
                and len(name.strip()) >= 3
                and name[0].isupper()
            )
            is_valid_description = (
                description
                and len(description.strip()) >= 10
                and description[0].isupper()
            )
            
            if is_valid_title and is_valid_description and option in levels:
                user_id = st.session_state['current_user'].id
                sm.add_skill(user_id, name, description, option)
                st.session_state['skill_added'] = (name, levels[option]) 
                st.success(f"Skill '{name}' added successfully at level '{levels[option]}'.") 
                st.rerun()
            else:
                if not is_valid_title:
                    st.error("Prašome pataisyti pavadinimas pagal reikalavimus")
                if not is_valid_description:
                    st.error("Prašome pataisyti aprašyma pagal reikalavimus")
                if not option not in levels:
                    st.error("Prašome pasirinkti tinkama lygį")
                
                
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
