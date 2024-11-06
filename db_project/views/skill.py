import streamlit as st
import db_project.controllers.user_manager as um
from db_project.controllers.skills_manager import add_skill, get_user_skills, delete_skill
from db_project.db_setup import SessionLocal
from models.level import Level
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_levels(db: Session):
    return db.query(Level).all()

def add_skill():
    st.header("Add a New Skill")
    with get_db() as db:
        skill_name = st.text_input("Skill Name")
        skill_description = st.text_area("Skill Description")
        levels = fetch_levels(db)
        level_choice = st.selectbox("Select Level", [(lvl.id, lvl.name) for lvl in levels])

        if st.button("Add Skill"):
            level_id = level_choice[0]
            user_id = st.session_state['current_user'].id
            new_skill = add_skill(db, user_id, skill_name, skill_description, level_id)
            st.success(f"Skill '{new_skill.name}' added successfully")

def show_my_skills():
    st.header("Your Skills")
    with get_db() as db:
        user_id = st.session_state['current_user'].id
        skills = get_user_skills(db, user_id)
        for skill in skills:
            st.write(f"**{skill.name}**")
            st.write(f"Description: {skill.description}")
            st.write(f"Level:  {skill.level.name}")
            st.write("---")

def remove_skill():
    st.header("Delete_Skill")
    with get_db() as db:
        user_id = st.session_state['current_user'].id
        skills = get_user_skills(db, user_id)
        skill_choice = st.selectbox("Select skill to Delete", [(sk.id, sk.name) for sk in skills])

        if st.button("Delete Skill"):
            delete_skill(db, skill_choice[0], user_id)
            st.warning(f"Skill '{skill_choice[1]}' deleted")

