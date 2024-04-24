import streamlit as st
import app as ai
import textwrap

st.title("☁️Cloud Project Generator")


certification = st.selectbox(
    'Microsoft Azure Certification',
    ('AZ-104', 'AZ-204', 'AZ-305', 'AZ-400'))

level = st.selectbox(
    'Project Level',
    ('beginner', 'intermediate', 'advanced'))


if certification and level:
    response = ai.project_idea(certification, level)
    st.markdown(response)
