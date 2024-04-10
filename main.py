import streamlit as st
import pandas as pd

df = pd.read_csv('SURVEY G1-G7 as docx.csv')


# Streamlit app
st.title('Question Finder')

user_input = st.text_input('Enter a phrase to match:')


def check_input(input_text):
    for index, row in df.iterrows():
        if str(input_text).lower() in str(row['Interviewee']).lower():
            return [row['Interviewer'], row["Participant ID"]]
    return None

# Check if input matches
if user_input:
    matched_question = check_input(user_input)
    print(matched_question)
    if matched_question:
        st.write("**Interviewer Question:** ",matched_question[0])
        st.write("**ID:** ",matched_question[1])
    else:
        st.warning('No matching question found.')
