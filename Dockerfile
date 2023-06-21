FROM python:3.11.4-alpine3.18

WORKDIR /app 

COPY requirements.txt requirements.txt 

RUN pip3 install --no-cache-dir -r requirements.txt 

COPY . . 

EXPOSE 12345

CMD ["python", "main.py"]