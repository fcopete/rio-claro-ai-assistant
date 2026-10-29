from flask import Blueprint,jsonify
executive_bp=Blueprint("executive",__name__)
@executive_bp.route("/sales-summary")
def sales_summary():
    return jsonify({"success":True,"total_sales":482490})
