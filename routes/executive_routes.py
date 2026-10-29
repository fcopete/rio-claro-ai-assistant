from flask import Blueprint, jsonify
from services.sample_data_service import load_sample_data
executive_bp=Blueprint("executive",__name__)
@executive_bp.route("/sales-summary")
def sales_summary(): return jsonify(load_sample_data()["executive_summary"])
