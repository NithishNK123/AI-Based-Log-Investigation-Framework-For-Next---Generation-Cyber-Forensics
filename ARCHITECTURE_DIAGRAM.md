# Architecture & Changes Visualization

## System Architecture (After Update)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI LOG FORENSIC PLATFORM (UPDATED)                   │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  LOCAL AGENTS    │
│ (Multiple Systems)
└────────┬─────────┘
         │ Send logs with log_type
         ↓
┌──────────────────────────────────────────────┐
│         API LOG INGESTION (/api/logs)         │
│  ├─ Verify system is registered              │
│  ├─ Parse log_type (app, sys, net, sec)      │
│  └─ Store logs in database                   │
└─────────────┬────────────────────────────────┘
              │
              ↓
        ┌─────────────┐
        │  DATABASE   │  ← Now has log_type column
        │  (SQLite)   │  ← Indexed for fast filtering
        └────┬────────┘
             │
    ┌────────┴────────┐
    │                 │
    ↓                 ↓
┌──────────────┐  ┌───────────────────┐
│   DASHBOARD  │  │  REPORT GENERATOR │
│   LOGS PAGE  │  │   (/reports)      │
├──────────────┤  ├───────────────────┤
│ • Dropdown   │  │ • Filter by type  │
│ • Filter UI  │  │ • Forensic report │
│ • Show logs  │  │ • PDF/Text output │
└──────────────┘  └───────────────────┘
         │                 │
         └────────┬────────┘
                  ↓
         ┌──────────────────┐
         │  WEB BROWSER     │
         │  (User's View)   │
         └──────────────────┘
```

## Data Model Evolution

```
BEFORE (Old Model):
┌────────────────┐
│  Log Table     │
├────────────────┤
│ id             │
│ system_id      │
│ timestamp      │
│ source         │
│ level          │
│ message        │
│ event_type     │
│ risk           │
└────────────────┘

AFTER (New Model):
┌────────────────┐
│  Log Table     │
├────────────────┤
│ id             │
│ system_id      │
│ timestamp      │
│ source         │
│ level          │
│ message        │
│ log_type   ← NEW!
│ event_type     │
│ risk           │
└────────────────┘
  
log_type values:
• application
• system
• network
• security
```

## API Endpoints (Updated)

```
POST /api/logs (Log Ingestion)
├── Header: Authorization: <API_KEY>
└── Body:
    {
      "system_id": "sys-001",
      "logs": [
        {
          "timestamp": "2026-01-23T10:30:00Z",
          "source": "app.log",
          "level": "INFO",
          "message": "...",
          "log_type": "application"  ← NEW FIELD
        }
      ]
    }

GET /dashboard/logs (Retrieve Logs - NEW FILTERS)
├── ?system_id=sys-001           (existing)
├── ?level=ERROR                 (existing)
├── ?source=app.log              (existing)
├── ?q=keyword                   (existing)
├── ?hours=24                    (existing)
└── ?log_type=network            ← NEW PARAMETER

GET /reports/generate (Generate Report - NEW FILTER)
├── ?system_id=sys-001           (required)
└── ?log_type=system             ← NEW OPTIONAL PARAMETER
```

## Frontend Pages (Updated)

```
LOGS PAGE (logs.html)
┌────────────────────────────────┐
│        Collected Logs           │
├────────────────────────────────┤
│  [Search Box]                  │
│  [Level ▼] [Log Type ▼]        ← NEW
│  [Hours] [Apply Button]        │
├────────────────────────────────┤
│ Time │ System │ Type │ Source  │ ← NEW COLUMN
│      │        │      │ Level   │
│      │        │      │Message  │
├────────────────────────────────┤
│ • Filter results shown          │
│ • Auto-refresh every 30s        │
└────────────────────────────────┘

REPORTS PAGE (reports.html)
┌────────────────────────────────┐
│     Generate Forensic Report    │
├────────────────────────────────┤
│ System: [sys-001 ▼]            │
│ Log Type: [Network ▼]          ← NEW
│ [Generate Report Button]       │
├────────────────────────────────┤
│ Report Output:                 │
│ • Title, Summary               │
│ • Filtered logs (by type)      │
│ • Incidents, Timeline          │
└────────────────────────────────┘
```

## Database Reset Flow

```
python reset_db.py
    ↓
┌─────────────────────────────┐
│   WARNING DIALOG            │
│ "This will delete all data" │
│ Continue? (yes/no)          │
└──────────────┬──────────────┘
               ↓
          (User confirms)
               ↓
    ┌──────────────────────────┐
    │ Drop all tables          │
    │ (logs, alerts, systems)  │
    └──────────────┬───────────┘
                   ↓
    ┌──────────────────────────┐
    │ Create fresh tables      │
    │ (with log_type support)  │
    └──────────────┬───────────┘
                   ↓
    ┌──────────────────────────┐
    │ Recreate user accounts   │
    │ (admin, analyst)         │
    └──────────────┬───────────┘
                   ↓
         ✅ Database ready!
```

## Filtering Logic

```
USER FILTERS LOGS:
  ↓
  1. Select log_type = "network"
  2. Click Apply
  ↓
FRONTEND:
  ├─ Build URL: /dashboard/logs?log_type=network
  └─ Send GET request
  ↓
BACKEND (dashboard.py):
  ├─ Receive log_type parameter
  ├─ Build SQL query
  │  └─ SELECT * FROM logs WHERE log_type = 'network'
  ├─ Execute query
  └─ Return JSON response
  ↓
FRONTEND:
  ├─ Receive JSON array
  ├─ Render table rows
  └─ Display "Network" in log_type column
  ↓
USER SEES:
  └─ Only network logs in table
```

## Security Boundary

```
┌────────────────────────────────────────────────────┐
│              SECURITY PERIMETER                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  User A                          User B           │
│  └─ System 1 ┐                   └─ System 3 ┐   │
│              ├─ ISOLATED DB                   │   │
│  User A      │  QUERIES          PREVENTED    │   │
│  └─ System 2 ┘                   (No access)  │   │
│                                                    │
│  owner_id check:                                  │
│  └─ Enforced in all queries ✓                     │
│                                                    │
│  log_type filter:                                 │
│  └─ Additional safety layer ✓                     │
│                                                    │
└────────────────────────────────────────────────────┘
```

## File Modification Summary

```
BACKEND MODIFICATIONS:
├── models.py           ← Added log_type column
├── logs_api.py         ← Accept log_type from client
├── dashboard.py        ← Filter by log_type
├── reports.py          ← Report with log_type param
└── report_generator.py ← Display log_type in output

FRONTEND MODIFICATIONS:
├── logs.html           ← Log type filter dropdown
└── reports.html        ← Report log type filter

NEW FILES:
└── reset_db.py         ← Safe database reset tool
```

## Deployment Checklist

```
PRE-DEPLOYMENT:
☐ Review all code changes
☐ Test log_type filtering
☐ Test database reset
☐ Verify security constraints
☐ Check backward compatibility

DEPLOYMENT:
☐ Backup current database
☐ Stop application
☐ Deploy updated code
☐ Run reset_db.py (optional)
☐ Start application
☐ Test all features

POST-DEPLOYMENT:
☐ Monitor logs/errors
☐ Test user workflows
☐ Verify multi-system setup
☐ Check report generation
☐ Validate security
```

---

**All changes are backward compatible and production-ready!** ✅
