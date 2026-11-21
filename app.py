import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "myapp"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

@app.route("/health")
def health():
    return "OK", 200

@app.route("/api/data")
def api_data():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    cur.close()
    conn.close()
    return jsonify({"status": "connected"})

@app.route("/api/items/count")
def items_count():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT);")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM items;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return str(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
