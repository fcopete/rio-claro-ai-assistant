from flask import Blueprint, request, jsonify
from services.document_service import analyze_invoice
from services.invoice_ai_service import analyze_invoice_risk
invoice_bp=Blueprint("invoice",__name__)
@invoice_bp.route("/upload",methods=["POST"])
def upload_invoice():
    file=request.files["file"]
    return jsonify({"success":True,"data":analyze_invoice(file)})
@invoice_bp.route("/analyze",methods=["POST"])
def ai_analysis():
    payload=request.get_json()
    return jsonify({"success":True,"analysis":analyze_invoice_risk(payload.get("invoice",{}),payload.get("history",[]))})
