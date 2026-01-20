🛡️ AI-Based Log Investigation Framework for Next-Generation Cyber Forensics
📌 Project Overview

Cyber forensics heavily depends on log analysis to investigate security incidents.
Traditional manual log investigation is slow, error-prone, and does not scale with modern distributed systems. Attackers can exploit this delay to erase traces or escalate privileges.

This project proposes an AI-powered log investigation framework that:

Automatically collects logs from endpoint systems

Securely transfers logs to a central platform

Uses AI techniques to detect anomalies

Reconstructs forensic timelines

Generates investigation reports

The system is designed to work even when endpoints are offline, ensuring no log data loss.

🎯 Problem Statement (PS03 – Cyber Security)

Traditional manual analysis of logs often delays cyber forensic investigations, allowing attackers to escape or hide evidence. An AI-based framework is required to automate log collection, analysis, and investigation across multiple systems efficiently and accurately.

💡 Proposed Solution

We design a two-part system:

1️⃣ Local Agent (Endpoint Side)

Runs on user systems (Windows / Linux)

Collects system, application, and security logs

Works in offline mode

Encrypts logs

Sends logs to the server when internet is available

2️⃣ Central Web Platform (Server Side)

Receives encrypted logs

Stores logs securely

Applies AI-based analysis (anomaly detection, clustering)

Reconstructs attack timelines

Displays results in a SOC-style dashboard

Generates forensic reports

🧱 System Architecture
[ Endpoint System ]
       |
       |  (Local Agent)
       v
[ Offline Log Storage (SQLite) ]
       |
       |  (Encrypted Sync)
       v
[ Central Web Platform ]
       |
       |  (AI Analysis)
       v
[ Alerts • Timeline • Reports ]

🗂️ Project Structure
🔹 Local Agent
local-agent/
│
├── agent.py
├── config/
│   └── agent_config.yaml
├── collectors/
│   ├── linux_logs.py
│   ├── windows_logs.py
│   └── app_logs.py
├── sender/
│   └── sync_logs.py
├── storage/
│   └── local_logs.db
├── utils/
│   ├── system_id.py
│   ├── formatter.py
│   ├── encrypt.py
│   └── logger.py
├── requirements.txt
└── README.md

🔹 Web Application
ai-log-forensic-platform/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── register.py
│   │   ├── logs_api.py
│   │   └── dashboard.py
│   ├── ai_engine/
│   │   ├── run_logai.py
│   │   ├── anomaly_detection.py
│   │   ├── clustering.py
│   │   └── timeline.py
│   └── reports/
│       └── report_generator.py
│
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── systems.html
│   │   ├── logs.html
│   │   └── reports.html
│   └── static/
│       ├── css/style.css
│       ├── js/dashboard.js
│       └── images/logo.png
│
├── run.py
└── README.md

🛠️ Technology Stack
🔹 Backend

Python

Flask

Flask-SQLAlchemy

SQLite

Cryptography (AES/Fernet)

🔹 AI / Analytics

Rule-based Anomaly Detection (Prototype)

TF-IDF + KMeans (Log Clustering)

Timeline Reconstruction

LogAI (Pluggable for future ML/DL)

🔹 Frontend

HTML5

CSS3 (Cyber SOC Theme)

JavaScript (Fetch API)

🔹 Agent Side

Python

SQLite

AES Encryption

Offline-first design

🔐 Security Features

Encrypted log transmission

API-key based agent authentication

Offline log storage

Centralized access control

Tamper-resistant log handling

🔄 Workflow Explanation

Local agent starts on endpoint

Generates unique system ID

Collects logs periodically

Stores logs locally when offline

Encrypts logs

Sends logs to server when online

Server decrypts and stores logs

AI engine analyzes logs

Alerts and timelines generated

Analyst views results in dashboard

Forensic report generated

📊 Output & Results

Centralized log repository

Security alerts for suspicious activity

Clustered log patterns

Chronological forensic timelines

System-wise forensic reports

🎤 One-Line Viva Explanation

This project automates cyber forensic log investigation using an AI-driven framework that securely collects, analyzes, and visualizes logs across multiple systems, significantly reducing investigation time and improving accuracy.

🚀 Future Enhancements

Full LogAI ML/DL integration

Real-time alerting

JWT-based authentication

Role-based access control

Cloud deployment

Tamper detection

PDF report export

📜 License

This project is developed for academic and educational purposes.

🙌 Acknowledgements

Open-source Python community

Cybersecurity research references

LogAI (Salesforce)

✅ Final Note

This framework demonstrates how AI + Cyber Forensics can transform traditional log investigation into a fast, scalable, and intelligent security solution.