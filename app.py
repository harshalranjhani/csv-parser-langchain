import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# Set the FastAPI endpoint
FASTAPI_UPLOAD_ENDPOINT = "http://0.0.0.0:8080/upload"

# Define the Streamlit app layout
st.title("CSV Upload and Processing App")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Display the contents of the uploaded file
    st.write("Uploaded file contents:")
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Submit button
    if st.button("Submit"):
        # Convert the uploaded file to a binary format to send via HTTP
        with st.spinner('Uploading and processing...'):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(FASTAPI_UPLOAD_ENDPOINT, files=files)
            
            if response.status_code == 200:
                # Read the CSV content from the response
                result_file_content = response.content
                processed_df = pd.read_csv(BytesIO(result_file_content))

                st.success("File processed successfully!")

                # Display the processed file
                st.write("Processed file contents:")
                st.dataframe(processed_df)

                # Provide a download button for the processed file
                st.download_button(
                    label="Download Processed CSV",
                    data=result_file_content,
                    file_name='resulting_data.csv',
                    mime='text/csv'
                )
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
