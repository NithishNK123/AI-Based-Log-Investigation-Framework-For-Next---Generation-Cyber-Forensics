# ⚡ Command Reference - All Commands You Need

## 🚀 Getting Started

### 1. Reset Database (Fresh Start)
```bash
cd ai-log-forensic-platform
python reset_db.py
```
**What it does:**
- Deletes all old logs, alerts, systems
- Keeps user accounts (safe mode)
- Creates fresh database with log_type support
- Recreates admin and analyst users

**Expected output:**
```
✓ Database tables created
✓ Admin user created: username='admin', password='admin123'
✓ Analyst user created: username='analyst', password='analyst123'
✅ Database setup complete!
```

---

### 2. Run the Application
```bash
python run.py
```
**What it does:**
- Starts Flask development server
- Loads all routes and blueprints
- Initializes database tables
- Starts listening on http://localhost:5000

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**Then open:**
- http://localhost:5000 in web browser
- Login with admin/admin123

---

### 3. Send Logs from Local Agent
```bash
cd local-agent
python agent.py
```
**What it does:**
- Collects logs from local system
- Sends to central API
- Registers system if not exists
- Continues running and collecting

**To stop:**
- Press CTRL+C

---

## 🔧 Database Commands

### Backup Database
```bash
cp ai-log-forensic-platform/instance/forensic.db forensic.db.backup
```

### Restore Database
```bash
cp forensic.db.backup ai-log-forensic-platform/instance/forensic.db
```

### Reset Everything
```bash
cd ai-log-forensic-platform
python reset_db.py
```

### Access Database CLI
```bash
sqlite3 instance/forensic.db
```
Then in SQLite prompt:
```sql
-- View all tables
.tables

-- Count logs
SELECT COUNT(*) FROM logs;

-- View log types
SELECT DISTINCT log_type FROM logs;

-- Count by system
SELECT system_id, COUNT(*) FROM logs GROUP BY system_id;
```

---

## 🌐 API Commands

### Send Logs via API
```bash
curl -X POST http://localhost:5000/api/logs \
  -H "Authorization: test-agent-key" \
  -H "Content-Type: application/json" \
  -d '{
    "system_id": "test-system-01",
    "logs": [
      {
        "timestamp": "2026-01-23T10:30:00Z",
        "source": "app.log",
        "level": "INFO",
        "message": "Application started",
        "log_type": "application"
      },
      {
        "timestamp": "2026-01-23T10:31:00Z",
        "source": "firewall.log",
        "level": "CRITICAL",
        "message": "Port scan detected",
        "log_type": "network"
      }
    ]
  }'
```

### Get Systems
```bash
curl http://localhost:5000/dashboard/systems
```

### Get Logs (All)
```bash
curl http://localhost:5000/dashboard/logs
```

### Get Logs (Filtered by Type)
```bash
curl http://localhost:5000/dashboard/logs?log_type=network
```

### Get Logs (Filtered by Level)
```bash
curl http://localhost:5000/dashboard/logs?level=ERROR
```

### Get Logs (Multiple Filters)
```bash
curl http://localhost:5000/dashboard/logs?log_type=network&level=CRITICAL&hours=24
```

### Generate Report
```bash
curl http://localhost:5000/reports/generate?system_id=test-system-01
```

### Generate Filtered Report
```bash
curl http://localhost:5000/reports/generate?system_id=test-system-01&log_type=network
```

### Download PDF Report
```bash
curl http://localhost:5000/reports/download?file=forensic_report_test-system-01_network_20260123_103000.pdf -o report.pdf
```

---

## 📁 File/Folder Commands

### Create Reports Directory
```bash
mkdir -p ai-log-forensic-platform/generated_reports
```

### List Generated Reports
```bash
ls ai-log-forensic-platform/generated_reports/
```

### List Documentation
```bash
ls -la "Log Investigation"/*.md
```

### View Documentation
```bash
# On Windows
type "Log Investigation\FINAL_SUMMARY.md"

# On Mac/Linux
cat "Log Investigation/FINAL_SUMMARY.md"
```

---

## 🐍 Python Commands

### Check Python Version
```bash
python --version
```

### Create Virtual Environment (Optional)
```bash
python -m venv venv
```

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Install Requirements
```bash
cd ai-log-forensic-platform
pip install -r backend/requirements.txt
```

### List Installed Packages
```bash
pip list
```

---

## 🛠️ Development Commands

### Run in Debug Mode
```bash
# Set Flask app
set FLASK_APP=backend.app  # Windows
export FLASK_APP=backend.app  # Mac/Linux

# Run with debug
python -m flask run --debug
```

### Check Database Schema
```bash
sqlite3 ai-log-forensic-platform/instance/forensic.db ".schema"
```

### Check Database Integrity
```bash
sqlite3 ai-log-forensic-platform/instance/forensic.db "PRAGMA integrity_check;"
```

### Vacuum Database (Optimize)
```bash
sqlite3 ai-log-forensic-platform/instance/forensic.db "VACUUM;"
```

---

## 📊 Testing Commands

### Test Log Ingestion
```bash
# 1. Send test logs
curl -X POST http://localhost:5000/api/logs \
  -H "Authorization: test-agent-key" \
  -H "Content-Type: application/json" \
  -d '{
    "system_id": "test-01",
    "logs": [{"timestamp": "2026-01-23T10:30:00Z", "source": "test.log", "level": "INFO", "message": "Test", "log_type": "application"}]
  }'

# 2. Check if stored
curl http://localhost:5000/dashboard/logs

# 3. Filter by type
curl http://localhost:5000/dashboard/logs?log_type=application
```

### Test Report Generation
```bash
# Generate report
curl http://localhost:5000/reports/generate?system_id=test-01&log_type=application

# Check if PDF created
ls ai-log-forensic-platform/generated_reports/
```

---

## 🔍 Debugging Commands

### Check Running Processes
```bash
# Windows
tasklist | findstr python

# Mac/Linux
ps aux | grep python
```

### Kill Process on Port 5000
```bash
# Windows
netstat -ano | findstr 5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### View Application Logs
```bash
# Check terminal where python run.py is running
# Logs appear in real-time
```

### Check Network Connectivity
```bash
# Test API is running
curl -v http://localhost:5000/api

# Test with auth
curl -v http://localhost:5000/api -H "Authorization: test-agent-key"
```

---

## 📝 Common Workflows

### Complete Investigation Workflow
```bash
# 1. Start fresh
python reset_db.py

# 2. Start application
python run.py
# (Keep running in terminal 1)

# 3. In new terminal, send logs
cd local-agent
python agent.py
# (Let it run for a minute, then stop with Ctrl+C)

# 4. View in dashboard
# Open http://localhost:5000
# Login with admin/admin123

# 5. Generate reports
curl http://localhost:5000/reports/generate?system_id=<ID>&log_type=network

# 6. Download PDF
curl http://localhost:5000/reports/download?file=<filename> -o report.pdf
```

---

## 🐛 Troubleshooting Commands

### Reset Everything from Scratch
```bash
# 1. Kill any running processes
# Ctrl+C in terminals

# 2. Reset database
cd ai-log-forensic-platform
python reset_db.py

# 3. Start fresh
python run.py
```

### Clear Old Reports
```bash
# Windows
cd ai-log-forensic-platform
rmdir /S /Q generated_reports
mkdir generated_reports

# Mac/Linux
cd ai-log-forensic-platform
rm -rf generated_reports
mkdir generated_reports
```

### Verify Installation
```bash
# Check Python
python --version

# Check Flask
python -c "import flask; print(flask.__version__)"

# Check SQLAlchemy
python -c "import sqlalchemy; print(sqlalchemy.__version__)"

# Check ReportLab
python -c "import reportlab; print(reportlab.Version)"
```

---

## 🎯 Quick Command Templates

### Template: Send Custom Logs
```bash
curl -X POST http://localhost:5000/api/logs \
  -H "Authorization: test-agent-key" \
  -H "Content-Type: application/json" \
  -d '{
    "system_id": "YOUR_SYSTEM_ID",
    "logs": [
      {
        "timestamp": "2026-01-23T TIME:HERE:00Z",
        "source": "YOUR_SOURCE",
        "level": "YOUR_LEVEL",
        "message": "YOUR_MESSAGE",
        "log_type": "application|system|network|security"
      }
    ]
  }'
```

### Template: Filter Logs
```bash
curl "http://localhost:5000/dashboard/logs?system_id=SYSTEM&log_type=TYPE&level=LEVEL&hours=HOURS"
```

### Template: Generate Report
```bash
curl "http://localhost:5000/reports/generate?system_id=SYSTEM&log_type=TYPE"
```

---

## 📋 Useful Terminal Shortcuts

### Windows PowerShell
```powershell
# Navigate
cd path\to\folder

# List files
dir

# Clear screen
cls

# Stop process (Ctrl+C)

# Run Python script
python script.py

# Check port
netstat -ano | findstr :5000
```

### Mac/Linux Terminal
```bash
# Navigate
cd path/to/folder

# List files
ls -la

# Clear screen
clear

# Stop process (Ctrl+C)

# Run Python script
python script.py

# Check port
lsof -i :5000
```

---

## ✅ Command Checklist

### First Time Setup
- [ ] `python reset_db.py`
- [ ] `python run.py`
- [ ] Open http://localhost:5000

### Each Session
- [ ] `cd ai-log-forensic-platform`
- [ ] `python run.py`
- [ ] Open http://localhost:5000

### Testing
- [ ] Send test logs via curl
- [ ] View in dashboard
- [ ] Filter by log type
- [ ] Generate and download PDF

### Troubleshooting
- [ ] Check `python --version`
- [ ] Check `netstat -ano | findstr 5000`
- [ ] Run `python reset_db.py`
- [ ] Restart with `python run.py`

---

## 🆘 Commands If Things Go Wrong

### Database Issues
```bash
# Backup and reset
cp ai-log-forensic-platform/instance/forensic.db forensic.db.bak
cd ai-log-forensic-platform
python reset_db.py
```

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or change port
python -m flask run --port 5001
```

### Module Not Found
```bash
# Install requirements
pip install -r backend/requirements.txt

# Or install specific package
pip install flask flask-sqlalchemy reportlab
```

### Permission Denied
```bash
# On Mac/Linux, make script executable
chmod +x reset_db.py

# Then run
python reset_db.py
```

---

**All commands ready to copy-paste!** 📋✨
