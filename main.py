from fastapi import FastAPI, File, UploadFile
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import io
import requests
from db import Base, engine, SessionLocal

# Initiate FastAPI app
app = FastAPI()

def call_llm_to_check_tech_company(description):
    # TODO
    return "yes"

@app.post("/uploadcsv")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    content = file.file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Add "Technology Company" column
    df['Technology Company'] = df['Description'].apply(lambda d: call_llm_to_check_tech_company(d))
    
    # Dynamically create table schema using the column names from the CSV
    metadata = MetaData()
    columns = [Column(c, String) for c in df.columns]
    schema_table = Table('companies', metadata, Column('id', Integer, primary_key=True, autoincrement=True), *columns)
    
    # Create schema in SQLite
    metadata.create_all(engine)
    
    return {"message": "CSV processed and schema created"}