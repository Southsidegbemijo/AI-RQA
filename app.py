import streamlit as st
import pandas as pd
import io

survey_df = pd.read_csv('SURVEY G1-G7 in new docx format.csv', encoding='utf-8')


def check_input(input_text):
    for index, row in survey_df.iterrows():
        if str(input_text).lower() in str(row['Interviewee']).lower():
            return row['Interviewer']
    return None


def modify_excel(df):
    new_df = df.copy()
    new_header = new_df.iloc[2]
    new_df = new_df.iloc[3:]
    new_df.columns = new_header
    new_df.reset_index(drop=True, inplace=True)

    chosen_cols = ['Participants',
                   'Provider characteristcs',
                   'Health System characteristics (academics; bed capacity also)',
                   'comparision of LUS with CXR and CT',
                   'Value equation: quality/cost/efficiency/patient satisfaction (Hosp leaders-background for implementation)',
                   'Clinical utility & efficiency-Provider perspective',
                   'Patient/Physican interaction in LUS',
                   'Workflow (with subcoding [bolded]: access equipment, order vs encounter-based; uploading & saving images; type of equipment.  End user need to acquire and use',
                   'training',
                   'credientialing /quality assurance infrastructure',
                   'Finanicial Impact'
                   ]

    new_df = new_df[chosen_cols]

    for index, row in new_df.iterrows():
        for col in new_df.columns:
            if isinstance(row[col], str) and len(row[col]) > 5:
                text = row[col].strip()
                formatted_text = text.split(':')[1].strip() if ':' in text else text
                interviewer = check_input(formatted_text)
                if interviewer:
                    new_text = f"Interviewer Original Question ==> {interviewer} \nGiven Answers ==> {text}"
                    new_df.at[index, col] = new_text

    return new_df


def main():
    st.title("Document Question Generator")
    st.write("This tool Generates the questions for the excel file inside every row")
    uploaded_file = st.file_uploader("Upload the Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.write("### Original DataFrame:")
            st.write(df)

            if st.button("Modify and Download"):
                modified_df = modify_excel(df)

                # Save modified DataFrame to BytesIO buffer
                buffer = io.BytesIO()
                modified_df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)

                # Download modified DataFrame as Excel file
                st.write("###  Modified Excel File:")
                st.write(modified_df)
                st.download_button(
                    label="Download Modified Excel File",
                    data=buffer,
                    file_name="modified_excel.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

                st.success("File has been modified , click the button above 👆 to download!")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
