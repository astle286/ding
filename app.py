from flask import Flask, render_template, request
import psycopg2
import os

# Prometheus integration
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # exposes /metrics endpoint

# Custom metric: count DB inserts
insert_counter = Counter('db_inserts_total', 'Total inserts into names table')

# DB config from environment variables
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "dingdong"),
    "dbname": os.environ.get("DB_NAME", "dingdb")
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO names (value) VALUES (%s)", ("astle",))
        conn.commit()
        cur.close()
        conn.close()
        insert_counter.inc()  # increment Prometheus metric
        return "Inserted 'astle' successfully!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1432)
