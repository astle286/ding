from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Adjust host/port/user/password/dbname to match your local SQL setup
DB_CONFIG = {
    "host": "host.docker.internal",  # works on Mac/Windows; on Linux use machine IP
    "port": 5432,
    "user": "postgres",
    "password": "dingdong",
    "dbname": "dingdb"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Example query: insert "astle" into a table
        cur.execute("INSERT INTO names (value) VALUES (%s)", ("astle",))
        conn.commit()
        cur.close()
        conn.close()
        return "Inserted 'astle' successfully!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1432)
