FROM python:3.11-alpine3.18

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host=0.0.0.0", "--port=8000"]
