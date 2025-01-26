FROM python:3.8-slim

WORKDIR /app

COPY  requirements.txt /app
COPY main.py /app
COPY data.py /app


RUN pip install requests pandas plotly pymongo streamlit

CMD ["streamlit", "run", "main.py"]