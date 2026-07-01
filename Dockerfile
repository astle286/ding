FROM python:3.10-slim

WORKDIR /app
COPY app.py /app
COPY templates /app/templates

RUN pip install flask psycopg2-binary

EXPOSE 1432
CMD ["python", "app.py"]
