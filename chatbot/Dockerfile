FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
