# AI-Based Log Investigation Framework for Next-Generation Cyber Forensics

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## 📌 Overview

The **AI Log Forensic Platform** is a comprehensive, next-generation Security Information and Event Management (SIEM) framework designed to streamline cyber forensic investigations. It enables security analysts to collect, monitor, and analyze logs from multiple endpoint systems efficiently, culminating in the automated generation of court-ready forensic PDF reports.

## ✨ Key Features

*   **📊 Centralized Dashboard & Monitoring:** Real-time visibility into registered endpoint systems, online/offline status, and critical security alerts.
*   **🔍 Advanced Log Ingestion & Filtering:** Categorizes and filters logs across four critical domains:
    *   `Application`: App errors, events, and performance metrics
    *   `System`: OS, kernel, and system services
    *   `Network`: Network traffic, firewalls, and DNS
    *   `Security`: Authentication, encryption, and policies
*   **📄 Automated Forensic PDF Reports:** One-click generation of professional, structured forensic reports. Includes executive summaries, incident detection, complete forensic timelines, and evidence integrity certification.
*   **🔒 Secure & Multi-Tenant Architecture:** Ensures isolated data views so users only see authorized systems, backed by secure Role-Based Access Control (RBAC).

## 🚀 Quick Start Guide

### Prerequisites
Make sure you have Python installed on your system.

### 1. Initial Setup
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/NithishNK123/AI-Based-Log-Investigation-Framework-For-Next---Generation-Cyber-Forensics.git
cd AI-Based-Log-Investigation-Framework-For-Next---Generation-Cyber-Forensics
```
*(If your code is inside the `ai-log-forensic-platform` directory, navigate there first).*

Initialize a fresh database (this safely creates the schema while preserving user accounts):
```bash
python reset_db.py
```

### 2. Run the Application
Start the Flask web server:
```bash
python run.py
```

### 3. Access the Platform
Open your web browser and navigate to: http://localhost:5000

**Default Roles & Credentials:**
*   **Administrator**: `admin` / `admin123`
*   **Security Analyst**: `analyst` / `analyst123`

## 💻 Usage & Workflow

1.  **Dashboard View**: Upon login, view your connected systems and any active high-risk alerts.
2.  **System Tracking**: Check the `Systems` tab to see active endpoints and their last seen status.
3.  **Log Investigation**: Navigate to the `Logs` tab. Use the advanced filtering (Keyword, Severity Level, Log Type) to isolate specific events and trace attack vectors.
4.  **Report Generation**: Go to the `Reports` tab, select the target system, apply necessary filters (e.g., "Network"), and click **Generate Report**. Download the professional PDF summary directly to your machine.

## 🛡️ Security & Integrity

This platform is built with evidence preservation in mind:
*   **Isolation**: Strict data separation preventing cross-system data leakage.
*   **Integrity Verification**: Reports come with certification formatting to assure data has not been tampered with.
*   **Safe Resets**: The `reset_db.py` tool performs isolated data wipes without breaking the authentication schemas.

## 📚 Documentation
For deeper technical insights, please refer to the internal documentation files included in the repository:
*   `TECHNICAL_SUMMARY.md`: Database schemas, architectural data flows, and code structure.
*   `IMPLEMENTATION_GUIDE.md` / `VISUAL_WALKTHROUGH.md`: Detailed guides and step-by-step usage.
*   `README_START_HERE.md`: Full platform overview.
