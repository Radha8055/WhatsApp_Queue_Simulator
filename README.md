# WhatsApp_Queue_Simulator
WhatsApp Queue Simulator is a web-based messaging project built using Python, Flask, and SQLite. It simulates message processing through a queue, where messages move from QUEUED to SENT and then DELIVERED. The project demonstrates message queues, database management, status tracking, and basic web application development.
WhatsApp Queue Simulator

📌 Project Description

WhatsApp Queue Simulator is a web-based messaging application developed using Python, Flask, JavaScript, HTML, CSS, and SQLite. It simulates how messages are processed through a queue before being delivered to the receiver.

🚀 Features

- Send messages from one user to another
- Queue-based message processing
- Message status tracking
- Status flow: QUEUED → SENT → DELIVERED
- SQLite database for storing messages
- Simple and user-friendly web interface
- Automatic message processing with a short delay

🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

📂 Project Structure

WhatsApp-Queue-Simulator/
│
├── app.py
├── queue_manager.py
├── messages.db
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js

▶️ How to Run

1. Install Python on your computer.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required libraries:

pip install -r requirements.txt

5. Run the application:

python app.py

6. Open the URL shown in the terminal in your web browser.

🔄 Message Flow

User → Queue → SENT → DELIVERED

When a user sends a message, it is first added to the queue. The queue manager processes the message and updates its status until it is delivered.

🎯 Project Objective

The main objective of this project is to understand how message queues, database management, Flask web applications, and message status tracking work together in a messaging system.

📸 Output

Screenshots of the working application and message status are included in this repository.

👩‍💻 Developed By

Radha Sable
