from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/status")
def status():
    return {
        "system": "ok",
        "azure_openai": "ok",
        "document_ai": "ok"
    }
