from flask import Blueprint, jsonify
from services.sample_data_service import load_sample_data
customer_bp=Blueprint("customer",__name__)
@customer_bp.route("/pending")
def pending_customers(): return jsonify(load_sample_data()["customers"])
