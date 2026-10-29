from flask import Blueprint

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/pending")
def pending_customers():
    return {"pending_cases": 27}
