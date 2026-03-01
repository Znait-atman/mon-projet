from flask import Flask, jsonify
import os
import requests
import psycopg

app = Flask(__name__)

SERVICE_1_URL = os.getenv("SERVICE_1_URL", "http://service-1")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppass")

def get_conn():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        connect_timeout=3,
    )

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS requests_log (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT NOW(),
                    service1_message TEXT NOT NULL
                );
            """)
        conn.commit()

@app.get("/health")
def health():
    try:
        init_db()
        return jsonify(status="healthy", db="ok")
    except Exception as e:
        return jsonify(status="degraded", db="error", error=str(e)), 500

@app.get("/api/aggregate")
def aggregate():
    r = requests.get(f"{SERVICE_1_URL}/api/hello", timeout=3)
    msg = r.json().get("message", "no-message")

    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO requests_log(service1_message) VALUES (%s)", (msg,))
        conn.commit()

    return jsonify(
        service="service-2",
        called_service_1=True,
        service_1_response=r.json()
    )

@app.get("/api/stats")
def stats():
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM requests_log;")
            count = cur.fetchone()[0]
    return jsonify(total_aggregate_calls=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)