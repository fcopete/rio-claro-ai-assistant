from flask import Blueprint,jsonify
invoice_bp=Blueprint("invoice",__name__)
@invoice_bp.route("/upload",methods=["POST"])
def upload(): return jsonify({"success":True,"data":{}})
