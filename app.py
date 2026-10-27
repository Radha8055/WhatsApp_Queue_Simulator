from flask import Flask, render_template, request, jsonify
import sqlite3
import uuid

from queue_manager import add_message
from database import init_db

app = Flask(__name__)

DB_NAME = "messages.db"


@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# SEND MESSAGE
# ==========================================

@app.route("/send", methods=["POST"])
def send_message():

    try:

        data = request.get_json()

        sender = data.get("sender", "").strip()
        receiver = data.get("receiver", "").strip()
        message = data.get("message", "").strip()

        if not sender or not receiver or not message:

            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        message_id = str(uuid.uuid4())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages
            (id, sender, receiver, message, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message_id,
            sender,
            receiver,
            message,
            "QUEUED"
        ))

        conn.commit()
        conn.close()

        # Add message to queue
        add_message(message_id)

        return jsonify({
            "success": True,
            "id": message_id,
            "status": "QUEUED"
        })

    except Exception as e:

        print("SEND ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================
# GET MESSAGES
# ==========================================

@app.route("/messages/<username>")
def get_messages(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, sender, receiver, message, status
        FROM messages
        WHERE sender = ? OR receiver = ?
        ORDER BY rowid ASC
    """, (username, username))

    messages = cursor.fetchall()

    conn.close()

    result = []

    for m in messages:

        result.append({
            "id": m[0],
            "sender": m[1],
            "receiver": m[2],
            "message": m[3],
            "status": m[4]
        })

    return jsonify(result)


# ==========================================
# READ RECEIPT
# ==========================================

@app.route("/read/<message_id>", methods=["POST"])
def mark_read(message_id):

    try:

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE messages
            SET status = 'READ'
            WHERE id = ?
            AND status != 'READ'
        """, (message_id,))

        conn.commit()

        updated = cursor.rowcount

        conn.close()

        return jsonify({
            "success": True,
            "status": "READ",
            "updated": updated
        })

    except Exception as e:

        print("READ ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================
# START FLASK
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )