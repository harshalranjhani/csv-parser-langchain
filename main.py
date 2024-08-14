from fastapi import FastAPI, File, UploadFile
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData
import io
from db import engine
from langchain_helper import process_inputs
from fastapi.responses import StreamingResponse

# Initialize FastAPI app
app = FastAPI()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    content = file.file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Get the descriptions from the CSV file
    descriptions = df['Description'].tolist()

    # Call the helper function to process the inputs and get the results (yes/no)
    result = await process_inputs(descriptions)

    # Add "Technology Company" column
    df['Technology Company'] = result
    
    # Convert DataFrame back to CSV data
    csv_data = df.to_csv(index=False).encode()

    # Define response headers to trigger download (this downloads the resulting CSV file)
    response = StreamingResponse(io.BytesIO(csv_data), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=resulting_data.csv"

    return response