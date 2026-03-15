# 🎨 Quick Reference - Page-by-Page Guide

## PAGE 1: DASHBOARD 📊
```
┌────────────────────────────────────────────────────┐
│ 🔘 SOC DASHBOARD - AI Log Forensics               │
├────────────────────────────────────────────────────┤
│                                                    │
│  STATS (Top Row):                                 │
│  ┌──────┐  ┌──────┐  ┌──────┐                     │
│  │   0  │  │   0  │  │   0  │                     │
│  │ Syst │  │ Logs │  │Alert │                     │
│  └──────┘  └──────┘  └──────┘                     │
│                                                    │
│  REGISTERED SYSTEMS:                              │
│  ┌──────────┬──────────┬──────────────────┐       │
│  │ System ID│ Hostname │ Last Seen        │       │
│  ├──────────┼──────────┼──────────────────┤       │
│  │ f04b20e2 │ agent    │ 2026-01-20 04:20 │       │
│  │ 44373a8c │ agent    │ 2026-01-19 11:58 │       │
│  │ b4868edb │ agent    │ 2026-01-19 11:58 │       │
│  └──────────┴──────────┴──────────────────┘       │
│                                                    │
│  SECURITY ALERTS:                                 │
│  ┌────────────┬──────────────┬───────────────┐    │
│  │ System ID  │ Description  │ Time          │    │
│  ├────────────┼──────────────┼───────────────┤    │
│  │ f04b20e2   │ MALWARE_    │ 2026-01-20    │    │
│  │            │ ACTIVITY    │ 03:51:41      │    │
│  │ f04b20e2   │ MALWARE_    │ 2026-01-20    │    │
│  │            │ ACTIVITY    │ 03:51:40      │    │
│  └────────────┴──────────────┴───────────────┘    │
│                                                    │
└────────────────────────────────────────────────────┘

SIDEBAR:
[Dashboard]  ← You are here
[Systems]
[Logs]
[Reports]
[Logout]
```

**What to do here:**
- ✓ Monitor overall system health
- ✓ See which systems are registered
- ✓ View latest security alerts
- ✓ Quick status check

---

## PAGE 2: SYSTEMS 🖥️
```
┌────────────────────────────────────────────────────┐
│ 🖥️ REGISTERED SYSTEMS                             │
├────────────────────────────────────────────────────┤
│                                                    │
│  ENDPOINT SYSTEMS:                                │
│  ┌─────────────┬──────────┬──────────┬────────┐   │
│  │ System ID   │ Hostname │ Last Seen│ Status │   │
│  ├─────────────┼──────────┼──────────┼────────┤   │
│  │ f04b20e2... │ agent    │ 04:20:41 │ONLINE  │   │
│  │ 44373a8c... │ agent    │ 11:58:10 │ONLINE  │   │
│  │ b4868edb... │ agent    │ 11:58:08 │ONLINE  │   │
│  │ cc14cbe4... │ agent    │ 11:58:06 │ONLINE  │   │
│  │ 9a0042a7... │ agent    │ 11:58:05 │ONLINE  │   │
│  │ bcbcaeeb... │ agent    │ 11:58:03 │ONLINE  │   │
│  │ c56c6aa0... │ agent    │ 11:57:14 │ONLINE  │   │
│  └─────────────┴──────────┴──────────┴────────┘   │
│                                                    │
│  All systems are connected and sending logs       │
│                                                    │
└────────────────────────────────────────────────────┘

SIDEBAR:
[Dashboard]
[Systems]  ← You are here
[Logs]
[Reports]
[Logout]
```

**What to do here:**
- ✓ See all registered endpoint systems
- ✓ Check which systems are ONLINE/OFFLINE
- ✓ Monitor last check-in time
- ✓ Manage system list

---

## PAGE 3: LOGS 📜
```
┌────────────────────────────────────────────────────┐
│ 📜 LOG VIEWER                                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  FILTERS:                                         │
│  [Search keyword  ] [All Levels ▼] [All Types ▼]│
│  [Last N hours   ] [Apply]                       │
│                                                    │
│  All Levels Options:                              │
│  - INFO, WARNING, ERROR, CRITICAL                 │
│                                                    │
│  All Types Options: ← NEW!                        │
│  - All Log Types                                  │
│  - Application (app errors, events)               │
│  - System (OS, kernel, services)                  │
│  - Network (traffic, firewall, DNS)               │
│  - Security (auth, encryption, policies)          │
│                                                    │
│  LOGS TABLE:                                      │
│  ┌──────┬────────┬─────────┬────────┬──────┬──────┐│
│  │Time  │ System │LogType  │ Source │Level │ Msg  ││
│  ├──────┼────────┼─────────┼────────┼──────┼──────┤│
│  │10:30 │f04b20e │app      │app.log │ INFO │ ... ││
│  │10:31 │44373a8 │network  │fw.log  │ERROR │ ... ││
│  │10:32 │b4868ed │system   │syslog  │WARN  │ ... ││
│  └──────┴────────┴─────────┴────────┴──────┴──────┘│
│                                                    │
│  (Auto-refreshes every 30 seconds)               │
│                                                    │
└────────────────────────────────────────────────────┘

SIDEBAR:
[Dashboard]
[Systems]
[Logs]  ← You are here
[Reports]
[Logout]
```

**What to do here:**
- ✓ View all collected logs
- ✓ Filter by level (INFO, WARNING, ERROR, CRITICAL)
- ✓ Filter by log type (Application, System, Network, Security) ← NEW!
- ✓ Search for keywords
- ✓ Filter by time range
- ✓ Export for analysis

---

## PAGE 4: REPORTS 📄
```
┌────────────────────────────────────────────────────┐
│ 📄 FORENSIC REPORTS                                │
├────────────────────────────────────────────────────┤
│                                                    │
│  CONTROLS:                                        │
│  Select System: [f04b20e2-9bdd... ▼]              │
│  Filter By Log Type: [All Log Types ▼]            │
│  [Generate Report]                                │
│                                                    │
│  Filter By Log Type Options: ← NEW!               │
│  - All Log Types                                  │
│  - Application                                    │
│  - System                                         │
│  - Network                                        │
│  - Security                                       │
│                                                    │
│  AFTER GENERATION:                                │
│                                                    │
│  [📥 DOWNLOAD PDF REPORT] ← GREEN BUTTON!         │
│  ┌──────────────────────────────────────────────┐ │
│  │ CYBER FORENSIC INVESTIGATION REPORT          │ │
│  │ ════════════════════════════════════════════ │ │
│  │ System ID:      f04b20e2-9bdd-4af0...        │ │
│  │ Hostname:       agent                        │ │
│  │ Log Type:       NETWORK                      │ │
│  │ Generated:      2026-01-23 10:45 UTC         │ │
│  │                                              │ │
│  │ SUMMARY                                      │ │
│  │ Total Logs: 5                                │ │
│  │ Total Alerts: 1                              │ │
│  │ Critical Incidents: 1                        │ │
│  │                                              │ │
│  │ DETECTED INCIDENTS                           │ │
│  │ [CRITICAL] Port scan from 192.168.1.100      │ │
│  │                                              │ │
│  │ FORENSIC TIMELINE                            │ │
│  │ 10:30:15 | network | fw.log | ERROR | ...    │ │
│  │ 10:31:45 | network | fw.log | CRIT  | ...    │ │
│  │                                              │ │
│  │ CERTIFICATION                                │ │
│  │ Evidence Integrity: ✓                        │ │
│  │ Tamper-Resistant: ✓                          │ │
│  │ Court-Ready: ✓                               │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  PDF Downloads To: Downloads/                     │
│  forensic_report_f04b20e2_network_20260123...pdf  │
│                                                    │
└────────────────────────────────────────────────────┘

SIDEBAR:
[Dashboard]
[Systems]
[Logs]
[Reports]  ← You are here
[Logout]
```

**What to do here:**
- ✓ Select system to report on
- ✓ Filter by log type (Application, System, Network, Security) ← NEW!
- ✓ Generate forensic report
- ✓ Download professional PDF
- ✓ Use for court/SOC team
- ✓ Share for compliance audit

---

## 🎯 Typical Investigation Workflow

```
START: Security Alert on Dashboard
   ↓
STEP 1: Go to Systems page
   └─ Confirm system is ONLINE
   └─ Note system ID and hostname
   ↓
STEP 2: Go to Logs page
   └─ Select system from dropdown
   └─ Select log type (Network if attack, Security if malware, etc.)
   └─ Set time range (last 1 hour, last 24 hours)
   └─ Click Apply
   └─ Review logs in table
   ↓
STEP 3: Go to Reports page
   └─ Select same system
   └─ Select same log type
   └─ Click "Generate Report"
   ↓
STEP 4: Review & Download
   └─ Read text summary
   └─ Check "Download PDF Report" button
   └─ Click to save PDF
   └─ PDF ready for:
      - Court proceedings
      - SOC team briefing
      - Legal discovery
      - Audit documentation
   ↓
END: Evidence collected and ready
```

---

## 🔑 Key Concepts

### Log Types (NEW!) 🎯
- **Application**: App errors, events, performance
- **System**: OS, kernel, system services
- **Network**: Network traffic, firewall, DNS
- **Security**: Authentication, encryption, policies

### Alert Severity Levels 🚨
- **CRITICAL**: Immediate threat
- **High**: Serious concern
- **Medium**: Notable event
- **Low**: Minor issue

### Report Types 📊
- **Text Summary**: Human-readable overview
- **PDF Report**: Professional, court-ready
- **Filtered**: By log type for focus
- **Comprehensive**: All logs combined

---

## ⚡ Quick Actions

| Want to... | Go to... | Do this... |
|-----------|---------|-----------|
| See alerts | Dashboard | Look at "Security Alerts" table |
| Check system status | Systems | See "ONLINE/OFFLINE" column |
| Find specific logs | Logs | Use keyword search + filters |
| Filter by type | Logs | Select from "Log Type" dropdown |
| Generate report | Reports | Select system + type + Download |
| Create PDF | Reports | Click "Download PDF Report" button |

---

**Master the platform in 5 minutes!** ✅
