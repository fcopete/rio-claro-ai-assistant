from flask import Blueprint, jsonify
from services.sample_data_service import load_sample_data
admin_bp=Blueprint("admin",__name__)
@admin_bp.route("/status")
def status(): return jsonify(load_sample_data()["admin_status"])
