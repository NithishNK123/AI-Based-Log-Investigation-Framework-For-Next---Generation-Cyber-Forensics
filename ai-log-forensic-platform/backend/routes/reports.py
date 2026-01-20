"""
reports.py (FINAL VERSION)
--------------------------
Generates forensic investigation reports for systems.

Features:
- Secure system-based reports
- Downloadable forensic report
- Includes logs, alerts, summary
- Examiner-ready format
"""

from flask import Blueprint, send_file, jsonify, request
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from backend.database.models import System, Log, Alert

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

REPORT_DIR = "generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)


# =========================================================
# GENERATE REPORT (PDF)
# =========================================================
@reports_bp.route("/generate", methods=["GET"])
def generate_report():
    """
    URL:
    /reports/generate?system_id=<ID>
    """

    system_id = request.args.get("system_id")
    if not system_id:
        return jsonify({"error": "system_id required"}), 400

    system = System.query.filter_by(system_id=system_id).first()
    if not system:
        return jsonify({"error": "System not found"}), 404

    logs = Log.query.filter_by(system_id=system_id).order_by(Log.id.desc()).limit(100).all()
    alerts = Alert.query.filter_by(system_id=system_id).order_by(Alert.created_at.desc()).all()

    filename = f"{REPORT_DIR}/forensic_report_{system_id}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "AI-BASED CYBER FORENSIC INVESTIGATION REPORT")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"System ID   : {system.system_id}")
    y -= 15
    c.drawString(40, y, f"Hostname    : {system.hostname}")
    y -= 15
    c.drawString(40, y, f"Last Seen   : {system.last_seen}")
    y -= 15
    c.drawString(40, y, f"Generated   : {datetime.utcnow()}")
    y -= 25

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "SUMMARY")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Total Logs   : {len(logs)}")
    y -= 15
    c.drawString(40, y, f"Total Alerts : {len(alerts)}")
    y -= 25

    # --------------------------------------------------
    # ALERTS
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "DETECTED ALERTS")
    y -= 20
    c.setFont("Helvetica", 9)

    if alerts:
        for a in alerts:
            if y < 50:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 9)

            c.drawString(40, y, f"[{a.severity}] {a.created_at} - {a.description}")
            y -= 15
    else:
        c.drawString(40, y, "No alerts detected")
        y -= 15

    y -= 20

    # --------------------------------------------------
    # LOG EVIDENCE
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "LOG EVIDENCE (LAST 50 EVENTS)")
    y -= 20
    c.setFont("Helvetica", 8)

    for log in logs[:50]:
        if y < 50:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 8)

        line = f"{log.timestamp} | {log.source} | {log.level} | {log.message[:100]}"
        c.drawString(40, y, line)
        y -= 12

    c.save()

    return send_file(filename, as_attachment=True)
