from queue import Queue
import sqlite3
import threading
import time

message_queue = Queue()

DB_NAME = "messages.db"


# ==========================================
# ADD MESSAGE TO QUEUE
# ==========================================

def add_message(message_id):

    message_queue.put(message_id)


# ==========================================
# PROCESS MESSAGE QUEUE
# ==========================================

def process_messages():

    while True:

        message_id = message_queue.get()

        try:

            # ==================================
            # QUEUED -> SENT
            # ==================================

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE messages
                SET status = 'SENT'
                WHERE id = ?
                AND status = 'QUEUED'
            """, (message_id,))

            conn.commit()
            conn.close()


            # Wait for delivery simulation
            time.sleep(2)


            # ==================================
            # SENT -> DELIVERED
            # READ असेल तर बदलू नका
            # ==================================

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE messages
                SET status = 'DELIVERED'
                WHERE id = ?
                AND status = 'SENT'
            """, (message_id,))

            conn.commit()
            conn.close()


        except Exception as e:

            print("QUEUE ERROR:", e)


        finally:

            message_queue.task_done()


# ==========================================
# START BACKGROUND WORKER
# ==========================================

worker = threading.Thread(
    target=process_messages,
    daemon=True
)

worker.start()