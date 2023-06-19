FROM python:3.11.4-alpine3.18

EXPOSE 12345

WORKDIR /app 

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt 

COPY . . 

CMD ["uvicorn", "main:app", "--port", "12345"]