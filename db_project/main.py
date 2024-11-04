import streamlit as st
import sqlalchemy
import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
st.title('My First Streamlit App') # streamlit run db_project/main.py