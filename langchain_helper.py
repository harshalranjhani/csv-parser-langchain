import io
from db import engine
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import pandas as pd
import asyncio

# Load environment variables
load_dotenv()

# Define the prompt template
prompt_template = PromptTemplate(template="Is the following company a technology company? {description}\nAnswer 'yes' or 'no':")

# Initialize the OpenAI LLM
llm = OpenAI(temperature=0.7, max_tokens=50)

# Create the LLMChain
chain = LLMChain(prompt=prompt_template, llm=llm)

# Asynchronous function to call the LLM for each description
async def async_run_chain(description):
    return await asyncio.to_thread(chain.run, {"description": description})

# Function to call the LLM for each batch
async def call_llm_batch(descriptions):
    results = []
    for description in descriptions:
        task = asyncio.create_task(async_run_chain(description))
        results.append(task)
    
    responses = await asyncio.gather(*results)
    return [response.lower().strip() for response in responses]

async def process_inputs(input_list):
    try:
        batch_size = 5
        results = []

        for i in range(0, len(input_list), batch_size):
            batch = input_list[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1}")

            # Process the batch asynchronously
            batch_results = await call_llm_batch(batch)
            results.extend(batch_results)

    except Exception as e:
        print(f"An error occurred in process_inputs: {e}")
        results = []
    return results
