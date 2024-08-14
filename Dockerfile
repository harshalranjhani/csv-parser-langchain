FROM python:3.9

WORKDIR /

COPY . /

RUN pip install --no-cache-dir fastapi sqlalchemy pandas uvicorn requests asyncio \
    langchain langchain-openai python-multipart python-dotenv streamlit

EXPOSE 80

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 & streamlit run app.py"]
