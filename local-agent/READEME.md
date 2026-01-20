🛡️ Local Log Collection Agent
AI-Based Log Investigation Framework for Cyber Forensics
📌 Overview

The Local Log Collection Agent is a lightweight background application designed to collect system and application logs from endpoint machines for cyber forensic analysis. The agent operates in offline mode, securely stores logs locally, and synchronizes them with a central AI-powered forensic platform once internet connectivity is available. This agent forms a critical component of the Artificial Intelligence–based Log Investigation Framework for Next-Generation Cyber Forensics.

🎯 Key Features

✅ Continuous log collection

✅ Offline-first (store-and-forward mechanism)

✅ Secure encrypted log transmission

✅ Linux and Windows support

✅ SQLite-based local storage

✅ Unique system identification

✅ Lightweight and non-intrusive

🧱 Architecture Role
[ Endpoint System ]
        ↓
[ Local Agent ]
        ↓ (Encrypted Logs)
[ Central Web Platform ]
        ↓
[ AI Log Analysis (LogAI) ]

🗂️ Project Structure
local-agent/
│
├── agent.py                 # Main agent controller
├── config/
│   └── agent_config.yaml    # Agent configuration
├── collectors/
│   ├── linux_logs.py        # Linux log collector
│   ├── windows_logs.py      # Windows Event Log collector
│   └── app_logs.py          # Application log collector
├── sender/
│   └── sync_logs.py         # Log synchronization module
├── storage/
│   └── local_logs.db        # SQLite database (auto-created)
├── utils/
│   ├── system_id.py         # Unique system identification
│   ├── formatter.py         # Log formatting
│   ├── encrypt.py           # Log encryption
│   └── logger.py            # Agent logging
├── requirements.txt         # Dependencies
└── README.md

🛠️ Technologies Used

Language: Python 3.9+

Database: SQLite

Encryption: AES (Fernet)

Protocols: HTTP/HTTPS

Platform: Linux / Windows

IDE: Visual Studio Code

⚙️ Installation
1️⃣ Clone the repository
git clone <repository-url>
cd local-agent

2️⃣ Install dependencies
pip install -r requirements.txt


On Windows:

python -m pywin32_postinstall

▶️ Configuration

Edit the configuration file:

📄 config/agent_config.yaml

server:
  url: "http://localhost:8000/api/logs"
  api_key: "TEST_API_KEY_123"

agent:
  sync_interval_seconds: 60
  max_lines_per_file: 50

🚀 Running the Agent
python agent.py


⚠️ On Linux, run with sudo if required:

sudo python agent.py

🔄 How It Works

Agent starts in background

Generates a unique system ID

Collects system and application logs

Stores logs locally when offline

Encrypts logs before transmission

Syncs logs to server when online

Deletes logs after successful upload

🔐 Security Considerations

Logs are encrypted before transmission

API key authentication is enforced

No plaintext log exposure

Offline storage prevents data loss

📄 Local Database

SQLite database: storage/local_logs.db

Automatically created on first run

Stores logs during offline mode

📊 Output

Structured logs sent to central platform

Logs available for:

Anomaly detection

Timeline reconstruction

Forensic reporting

🎤 Viva / Interview Explanation (One Line)

The local agent continuously collects endpoint logs, securely stores them during offline conditions, and synchronizes them with a centralized AI-based forensic platform for rapid cyber investigation.

🧪 Sample Application Log (Optional)

Create a test file:

sample_app.log


Example content:

User login successful
Invalid password attempt
Database connection established
Unauthorized access detected

📌 Limitations

Deep analysis is handled by the central server

Requires elevated permissions for some system logs

Prototype-grade security (extendable)

🚀 Future Enhancements

Agent auto-update

Log compression

Secure key rotation

Cloud endpoint support

Tamper detection

📜 License

This project is developed for academic and educational purposes.

🙌 Acknowledgements

Open-source Python community

LogAI (Salesforce)

Cybersecurity research references

🏁 Final Note

This local agent is designed to be simple, secure, and scalable, serving as the foundation for an AI-driven cyber forensic investigation platform.