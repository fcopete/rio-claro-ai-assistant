from flask import Blueprint, jsonify

executive_bp = Blueprint("executive", __name__)

@executive_bp.route("/sales-summary")
def sales_summary():
    return jsonify({
        "success": True,
        "branches": [
            {"branch": "Monterrey", "sales": 154220},
            {"branch": "León", "sales": 128940},
            {"branch": "CDMX", "sales": 199330}
        ],
        "total_sales": 482490
    })
