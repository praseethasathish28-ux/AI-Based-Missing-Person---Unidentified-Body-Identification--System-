AI-Based Missing Person & Unidentified Body Identification System

📌 Overview
This project is a Flask-based AI system designed to assist in identifying missing persons and unidentified bodies through multi-stage database matching.
The system simulates verification across:
Police database
Hospital records
CCTV records
Morgue database
Future tracking system

🚀 Features
Image upload functionality
Multi-stage database matching logic
Structured folder automation
JSON-based record storage
Audio response generation (gTTS)
Clean Flask backend architecture

🛠️ Technologies Used
Python
Flask
HTML
JSON
gTTS
Werkzeug

📂 Project Structure
Copy code

missing_person_ai/
│
├── templates/
├── app.py
├── missing_records.json
├── .gitignore
└── README.md

▶️ How to Run
Install dependencies:
Copy code

pip install flask gtts werkzeug
Run:
Copy code

python app.py
Open in browser:
Copy code

http://127.0.0.1:5000/
