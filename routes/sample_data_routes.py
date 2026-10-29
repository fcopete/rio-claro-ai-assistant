from flask import Blueprint, jsonify
from services.sample_data_service import load_sample_data
sample_bp=Blueprint("sample",__name__)
@sample_bp.route("/all")
def all_data(): return jsonify(load_sample_data())
