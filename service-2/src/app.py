from flask import Flask, jsonify, request
import psycopg
import os

app = Flask(__name__)

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
                CREATE TABLE IF NOT EXISTS scores (
                    id SERIAL PRIMARY KEY,
                    player VARCHAR(100) NOT NULL,
                    score INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
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

@app.post("/api/score")
def add_score():
    data = request.get_json()
    player = data.get('player')
    score = data.get('score')
    if not player or score is None:
        return jsonify({"error": "player and score required"}), 400
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO scores (player, score) VALUES (%s, %s)", (player, score))
        conn.commit()
    return jsonify({"status": "ok"})

@app.get("/api/stats")
def stats():
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), COALESCE(AVG(score),0), COALESCE(MAX(score),0) FROM scores;")
            count, avg, max_score = cur.fetchone()
    return jsonify(total_games=count, average_score=float(avg), max_score=max_score)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)