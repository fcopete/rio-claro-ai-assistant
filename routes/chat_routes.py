from flask import Blueprint,request,jsonify
chat_bp=Blueprint("chat",__name__)
@chat_bp.route("/ask",methods=["POST"])
def ask(): return jsonify({"success":True,"answer":"Demo"})
