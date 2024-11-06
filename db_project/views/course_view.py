import streamlit as st
from datetime import datetime, time
from sqlalchemy import select
import pandas as pd
from time import sleep
import db_project.controllers.user_manager as um
import db_project.controllers.skills_manager as sm
import db_project.controllers.course_manager as cm

def add_course():
    st.subheader("Sukurti užsiėmimą", anchor=False)
    current_user = st.session_state.get('current_user')

    if not current_user:
        st.error("Please log in to create a course.")
        return

    if 'course_added' not in st.session_state:
        st.session_state['course_added'] = None

    with st.form(key='add_course_form', clear_on_submit=True): 
        name = st.text_input("Course title")
        description = st.text_area("Description")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date())
            start_time = st.time_input("Start Time", value=datetime.now().time())
            start_datetime = datetime.combine(start_date, start_time)
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date())
            end_time = st.time_input("End Time", value=datetime.now().time())
            end_datetime = datetime.combine(end_date, end_time)

        max_participants = st.number_input("Max Participants", min_value=1, value=1)

        skills = sm.get_user_skills(current_user.id) 
        if not skills:
            st.error("You need at least one skill to create a course.")
            return
        
        skill_options = {skill.id: skill.name for skill in skills}
        skill_id = st.selectbox("Select Skill", list(skill_options.keys()), format_func=lambda x: skill_options[x])

        submitted = st.form_submit_button('Create Course')
        if submitted:
            success = cm.add_course(
                name=name,
                description=description,
                start_date=start_datetime,
                end_date=end_datetime,
                max_participants=max_participants,
                skill_id=skill_id,
                user_id=current_user.id 
            )
            if success:
                st.success(f"Course '{name}' created successfully.")
                st.session_state['course_added'] = True
            else:
                st.warning("A course for this skill already exists.")


def show_my_courses():
    st.subheader("Mano įgūdžiai", anchor=False)
    current_user = st.session_state.get('current_user')

    if current_user:
        user_id = current_user.id
        courses = cm.get_my_courses(user_id)

        if courses:
            course_data = {
                'Select': [False] * len(courses), 
                'Name': [course.name for course in courses],
                'Description': [course.description for course in courses],
                'Start Date': [course.start_date for course in courses], 
                'End Date': [course.end_date for course in courses], 
                'Max Participants': [course.max_participants for course in courses],
                'Skill ID': [course.skill_id for course in courses], 
                'Pt to Next Level': [sm.points_to_next_level(course.skill.name) for course in courses]
            }
            df_courses = pd.DataFrame(course_data)

            edited_courses = st.data_editor(df_courses, num_rows="fixed", key="course_table", hide_index=True, disabled=("Name", "Description", "Start Date", "End Date", "Max Participants", "Skill ID", "Pt to Next Level"))
            
        else:
            st.write("No courses yet")
            if st.button("Add course?", key='addcourse'):
                st.session_state['current_page'] = 'add-course'
                st.rerun()
    else:
        st.write("User not logged in")

def show_available_courses():
    ...

def show_my_registrations():
    st.subheader("Mano registracijos", anchor=False)
    st.write ("No courses yet")