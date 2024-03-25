import streamlit as st
import app as ai
import textwrap

st.title("☁️Cloud Instructor")

"""
query = st.text_area(
            label="Ask me, how can I help you?",
            max_chars=500,
            key="question"
            )
"""

certification = st.selectbox(
    'Microsoft Azure Certification',
    ('AZ-900', 'AZ-104', 'AZ-305', 'AZ-400'))

level = st.selectbox(
    'Project Level',
    ('beginner', 'intermediate', 'advanced'))


if certification and level:
  response = ai.project_idea(certification, level)
  st.markdown(response)
