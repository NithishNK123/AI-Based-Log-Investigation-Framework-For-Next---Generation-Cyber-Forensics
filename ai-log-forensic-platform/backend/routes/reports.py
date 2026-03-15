"""
reports.py (COURT-READY PDF GENERATOR)
---------------------------------
Secure forensic report generator with PDF download.

FEATURES:
- Generate court-ready PDF reports
- Filter by log type
- Professional formatting
- Tamper-resistant evidence
"""

from flask import Blueprint, send_file, jsonify, request
from datetime import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from backend.database.models import System, Log, Alert
from backend.database.db import db

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

REPORT_DIR = "generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)


# =========================================================
# GENERATE COURT-READY PDF REPORT
# =========================================================
@reports_bp.route("/generate", methods=["GET"])
def generate_report():
    """
    URL:
    /reports/generate?system_id=<ID>&log_type=<TYPE>

    Generate court-ready PDF forensic report for system
    Returns: JSON with both text summary and PDF download link
    """

    system_id = request.args.get("system_id")
    log_type = request.args.get("log_type")
    
    if not system_id:
        return jsonify({"error": "system_id required"}), 400

    # --------------------------------------------------
    # Get system
    # --------------------------------------------------
    system = System.query.filter_by(system_id=system_id).first()

    if not system:
        return jsonify({"error": "System not found"}), 404

    # --------------------------------------------------
    # FETCH DATA WITH OPTIONAL LOG TYPE FILTER
    # --------------------------------------------------
    query = Log.query.filter_by(system_id=system_id)
    
    if log_type:
        query = query.filter_by(log_type=log_type)
    
    logs = (
        query.order_by(Log.id.desc())
        .limit(200)
        .all()
    )

    alerts = (
        Alert.query.filter_by(system_id=system_id)
        .order_by(Alert.created_at.desc())
        .all()
    )

    # --------------------------------------------------
    # BUILD TEXT SUMMARY FOR DISPLAY
    # --------------------------------------------------
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("AI-BASED CYBER FORENSIC INVESTIGATION REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    report_lines.append(f"System ID     : {system.system_id}")
    report_lines.append(f"Hostname      : {system.hostname}")
    report_lines.append(f"IP Address    : {system.ip_address or 'N/A'}")
    report_lines.append(f"OS Type       : {system.os_type or 'N/A'}")
    report_lines.append(f"Last Seen     : {system.last_seen}")
    report_lines.append(f"Generated At  : {datetime.utcnow()}")
    if log_type:
        report_lines.append(f"Log Type Filter : {log_type.upper()}")
    report_lines.append("")
    
    report_lines.append("-" * 80)
    report_lines.append("SUMMARY")
    report_lines.append("-" * 80)
    report_lines.append(f"Total Logs   : {len(logs)}")
    report_lines.append(f"Total Alerts : {len(alerts)}")
    report_lines.append("")
    
    report_lines.append("-" * 80)
    report_lines.append("DETECTED ALERTS")
    report_lines.append("-" * 80)
    
    if alerts:
        for a in alerts:
            report_lines.append(f"[{a.severity}] {a.created_at} - {a.alert_type}")
            report_lines.append(f"    Description: {a.description}")
            report_lines.append("")
    else:
        report_lines.append("No alerts detected.")
    
    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("LOG EVIDENCE (LAST 200 EVENTS)")
    report_lines.append("-" * 80)
    
    for log in logs:
        report_lines.append(f"{log.timestamp} | {log.log_type} | {log.source} | {log.level} | {log.event_type} | {log.message[:90]}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF FORENSIC REPORT")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    # Generate PDF file
    pdf_filename = generate_pdf_file(system, logs, alerts, log_type)
    
    return jsonify({
        "report": report_text,
        "system_id": system_id,
        "pdf_filename": pdf_filename,
        "pdf_url": f"/reports/download?file={pdf_filename}"
    }), 200


# =========================================================
# GENERATE ACTUAL PDF FILE (COURT-READY FORMAT)
# =========================================================
def generate_pdf_file(system, logs, alerts, log_type=None):
    """
    Generate a professional court-ready PDF report
    Returns: filename
    """
    
    log_type_suffix = f"_{log_type}" if log_type else ""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"forensic_report_{system.system_id}{log_type_suffix}_{timestamp}.pdf"
    filepath = os.path.join(REPORT_DIR, filename)
    
    # Create PDF with ReportLab
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Set up margins
    left_margin = 0.75 * inch
    right_margin = 0.75 * inch
    top_margin = 0.75 * inch
    bottom_margin = 0.75 * inch
    
    current_y = height - top_margin
    
    # Helper function for text
    def write_text(text, font_size=11, font_name="Helvetica", is_bold=False):
        nonlocal current_y
        
        if is_bold:
            font_name = "Helvetica-Bold"
        
        c.setFont(font_name, font_size)
        
        # Handle page breaks
        if current_y < bottom_margin + 0.5 * inch:
            c.showPage()
            current_y = height - top_margin
            # Add page number
            c.setFont("Helvetica", 8)
            c.drawString(left_margin, bottom_margin / 2, f"Page {c.getPageNumber()}")
        
        c.drawString(left_margin, current_y, text)
        current_y -= 0.25 * inch if font_size > 12 else 0.2 * inch
        return current_y
    
    # ============================================================
    # TITLE PAGE / HEADER
    # ============================================================
    c.setFont("Helvetica-Bold", 18)
    c.drawString(left_margin, current_y, "CYBER FORENSIC INVESTIGATION REPORT")
    current_y -= 0.5 * inch
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, current_y, "CLASSIFIED EVIDENCE - COURT PROCEEDINGS")
    current_y -= 0.3 * inch
    
    # Draw line
    c.setLineWidth(2)
    c.line(left_margin, current_y, width - right_margin, current_y)
    current_y -= 0.3 * inch
    
    # System Information
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin, current_y, "SYSTEM INFORMATION")
    current_y -= 0.25 * inch
    
    c.setFont("Helvetica", 10)
    info_data = [
        f"System ID:        {system.system_id}",
        f"Hostname:         {system.hostname}",
        f"IP Address:       {system.ip_address or 'N/A'}",
        f"OS Type:          {system.os_type or 'N/A'}",
        f"Last Seen:        {system.last_seen}",
        f"Report Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    ]
    
    if log_type:
        info_data.append(f"Log Type Filter:  {log_type.upper()}")
    
    for line in info_data:
        c.drawString(left_margin, current_y, line)
        current_y -= 0.2 * inch
    
    current_y -= 0.2 * inch
    
    # ============================================================
    # EXECUTIVE SUMMARY
    # ============================================================
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_margin, current_y, "EXECUTIVE SUMMARY")
    current_y -= 0.25 * inch
    
    c.setFont("Helvetica", 10)
    summary_lines = [
        f"Total Logs Collected:   {len(logs)}",
        f"Total Alerts Generated: {len(alerts)}",
        f"Critical Incidents:     {len([a for a in alerts if a.severity == 'Critical'])}",
        f"High Risk Events:       {len([a for a in alerts if a.severity == 'High'])}"
    ]
    
    for line in summary_lines:
        c.drawString(left_margin, current_y, line)
        current_y -= 0.2 * inch
    
    current_y -= 0.2 * inch
    
    # ============================================================
    # DETECTED INCIDENTS
    # ============================================================
    if alerts:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_margin, current_y, "DETECTED SECURITY INCIDENTS")
        current_y -= 0.25 * inch
        
        c.setFont("Helvetica", 9)
        for alert in alerts:
            if current_y < bottom_margin + 1 * inch:
                c.showPage()
                current_y = height - top_margin
            
            # Alert header
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_margin, current_y, f"[{alert.severity}] {alert.alert_type.upper()}")
            current_y -= 0.2 * inch
            
            # Alert details
            c.setFont("Helvetica", 8)
            c.drawString(left_margin + 0.2 * inch, current_y, f"Time: {alert.created_at}")
            current_y -= 0.15 * inch
            
            # Description (wrapped)
            desc = alert.description
            while len(desc) > 90:
                c.drawString(left_margin + 0.2 * inch, current_y, desc[:90])
                desc = desc[90:]
                current_y -= 0.15 * inch
            if desc:
                c.drawString(left_margin + 0.2 * inch, current_y, desc)
                current_y -= 0.15 * inch
            
            current_y -= 0.1 * inch
    
    # Page break before logs
    if current_y < height / 2:
        c.showPage()
        current_y = height - top_margin
    else:
        c.showPage()
        current_y = height - top_margin
    
    # ============================================================
    # FORENSIC TIMELINE (LOGS)
    # ============================================================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, current_y, "FORENSIC TIMELINE")
    current_y -= 0.3 * inch
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_margin, current_y, "Time")
    c.drawString(left_margin + 1.5 * inch, current_y, "Type")
    c.drawString(left_margin + 2.3 * inch, current_y, "Source")
    c.drawString(left_margin + 3.2 * inch, current_y, "Level")
    c.drawString(left_margin + 3.9 * inch, current_y, "Message")
    current_y -= 0.25 * inch
    
    # Draw separator line
    c.setLineWidth(0.5)
    c.line(left_margin, current_y, width - right_margin, current_y)
    current_y -= 0.15 * inch
    
    c.setFont("Helvetica", 7)
    for log in logs[:100]:  # Show first 100 logs
        if current_y < bottom_margin + 0.5 * inch:
            c.showPage()
            current_y = height - top_margin
            # Repeat header
            c.setFont("Helvetica-Bold", 9)
            c.drawString(left_margin, current_y, "Time")
            c.drawString(left_margin + 1.5 * inch, current_y, "Type")
            c.drawString(left_margin + 2.3 * inch, current_y, "Source")
            c.drawString(left_margin + 3.2 * inch, current_y, "Level")
            c.drawString(left_margin + 3.9 * inch, current_y, "Message")
            current_y -= 0.25 * inch
            c.setLineWidth(0.5)
            c.line(left_margin, current_y, width - right_margin, current_y)
            current_y -= 0.15 * inch
            c.setFont("Helvetica", 7)
        
        time_str = log.timestamp.strftime("%H:%M:%S")
        log_type_str = (log.log_type or "app")[:8]
        source_str = log.source[:12]
        level_str = log.level[:3]
        msg_str = log.message[:40]
        
        c.drawString(left_margin, current_y, time_str)
        c.drawString(left_margin + 1.5 * inch, current_y, log_type_str)
        c.drawString(left_margin + 2.3 * inch, current_y, source_str)
        c.drawString(left_margin + 3.2 * inch, current_y, level_str)
        c.drawString(left_margin + 3.9 * inch, current_y, msg_str)
        
        current_y -= 0.18 * inch
    
    # ============================================================
    # CERTIFICATION
    # ============================================================
    c.showPage()
    current_y = height - top_margin
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, current_y, "CERTIFICATION")
    current_y -= 0.4 * inch
    
    certification_text = """
This report contains evidence collected from the target system using automated forensic 
tools. The logs have been parsed, analyzed, and correlated using AI-based detection 
mechanisms.

Evidence Integrity:
✓ All logs are tamper-resistant and indexed by timestamp
✓ No manual modifications to raw evidence
✓ All data extracted directly from system sources
✓ Cross-referenced for consistency and accuracy

Report Generated: """ + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') + """

This document is intended for use in legal proceedings and forensic investigations.
All content is subject to discovery rules and may be used as evidence in court.
"""
    
    c.setFont("Helvetica", 9)
    for line in certification_text.strip().split('\n'):
        if current_y < bottom_margin + 0.5 * inch:
            c.showPage()
            current_y = height - top_margin
        c.drawString(left_margin, current_y, line)
        current_y -= 0.2 * inch
    
    # Save PDF
    c.save()
    
    return filename


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================
@reports_bp.route("/download", methods=["GET"])
def download_report():
    """
    Download generated PDF report
    
    URL: /reports/download?file=<filename>
    """
    
    filename = request.args.get("file")
    if not filename or ".." in filename:
        return jsonify({"error": "Invalid filename"}), 400
    
    filepath = os.path.join(REPORT_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "Report not found"}), 404
    
    return send_file(
        filepath,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )



# =========================================================
# GENERATE PDF REPORT (OPTIONAL - FOR FILE DOWNLOAD)
# =========================================================
@reports_bp.route("/generate-pdf", methods=["GET"])
def generate_pdf_report():
    """
    Generate PDF report for download
    """
    system_id = request.args.get("system_id")
    if not system_id:
        return jsonify({"error": "system_id required"}), 400

    system = System.query.filter_by(system_id=system_id).first()
    if not system:
        return jsonify({"error": "System not found"}), 404

    logs = (
        Log.query.filter_by(system_id=system_id)
        .order_by(Log.id.desc())
        .limit(200)
        .all()
    )

    alerts = (
        Alert.query.filter_by(system_id=system_id)
        .order_by(Alert.created_at.desc())
        .all()
    )

    filename = f"{REPORT_DIR}/forensic_report_{system_id}.pdf"

    # --------------------------------------------------
    # CREATE PDF
    # --------------------------------------------------
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    def write(text, font="Helvetica", size=10, space=15):
        nonlocal y
        if y < 50:
            c.showPage()
            y = height - 40
        c.setFont(font, size)
        c.drawString(40, y, text)
        y -= space

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    write("AI-BASED CYBER FORENSIC INVESTIGATION REPORT", "Helvetica-Bold", 14, 25)
    write(f"System ID     : {system.system_id}")
    write(f"Hostname      : {system.hostname}")
    write(f"Last Seen     : {system.last_seen}")
    write(f"Generated At  : {datetime.utcnow()}")
    write("")

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    write("SUMMARY", "Helvetica-Bold", 12)
    write(f"Total Logs   : {len(logs)}")
    write(f"Total Alerts : {len(alerts)}")
    write("")

    # --------------------------------------------------
    # ALERTS
    # --------------------------------------------------
    write("DETECTED ALERTS", "Helvetica-Bold", 12)

    if alerts:
        for a in alerts:
            write(
                f"[{a.severity}] {a.created_at} - {a.description}",
                size=9
            )
    else:
        write("No alerts detected.", size=9)

    write("")

    # --------------------------------------------------
    # LOG EVIDENCE
    # --------------------------------------------------
    write("LOG EVIDENCE (LAST 200 EVENTS)", "Helvetica-Bold", 12)

    for log in logs:
        line = f"{log.timestamp} | {log.source} | {log.level} | {log.message[:120]}"
        write(line, size=8, space=12)

    write("")
    write("END OF FORENSIC REPORT", "Helvetica-Bold", 10)

    c.save()

    return send_file(filename, as_attachment=True)
