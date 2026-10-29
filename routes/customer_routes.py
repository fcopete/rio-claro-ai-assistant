from flask import Blueprint,jsonify
customer_bp=Blueprint("customer",__name__)
@customer_bp.route("/pending")
def pending_customers():
    return jsonify({"success":True,"pending_cases":27})
