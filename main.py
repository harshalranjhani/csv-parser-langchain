from fastapi import FastAPI, File, UploadFile
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData
import io
from db import engine
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define the prompt template
prompt_template = PromptTemplate(template="Is the following company a technology company? {description}\nAnswer 'yes' or 'no':")

# Initialize the OpenAI LLM
llm = OpenAI(temperature=0.7)

# Create the LLMChain
chain = LLMChain(prompt=prompt_template, llm=llm)

def call_llm_to_check_tech_company(description):
    response = chain.run({"description": description})
    answer = response.lower().strip()
    print(f"Description: {description}, Answer: {answer}")
    return "yes" if answer == "yes" else "no"

@app.post("/uploadcsv")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    content = file.file.read()
    df = pd.read_csv(io.BytesIO(content))

    # Add "Technology Company" column
    df['Technology Company'] = df['Description'].apply(lambda d: call_llm_to_check_tech_company(d))
    
    # Dynamically create table schema
    metadata = MetaData()
    columns = [Column(c, String) for c in df.columns]
    schema_table = Table('companies', metadata, Column('id', Integer, primary_key=True, autoincrement=True), *columns)
    
    # Create schema in SQLite
    metadata.create_all(engine)
    
    return {"message": "CSV processed and schema created"}