from flask import Blueprint,jsonify
project_bp=Blueprint("project",__name__)
@project_bp.route("/info")
def info(): return jsonify({"project":"franciscocopete-ia-001"})
