FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi sqlalchemy pandas uvicorn

EXPOSE 80

ENV NAME World

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
