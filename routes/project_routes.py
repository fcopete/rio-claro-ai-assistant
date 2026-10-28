from flask import (
    Blueprint,
    jsonify
)

from config import (
    AZURE_OPENAI_DEPLOYMENT
)

from services.chat_service import (
    test_connection
)

project_bp = Blueprint(
    "project",
    __name__
)


@project_bp.route("/info")
def info():

    return jsonify({

        "success": True,

        "project":
            "franciscocopete-ia-001",

        "application":
            "Rio Claro AI Assistant",

        "deployment":
            AZURE_OPENAI_DEPLOYMENT
    })


@project_bp.route("/test")
def test():

    try:

        test_connection()

        return jsonify({
            "success": True
        })

    except Exception as ex:

        return jsonify({
            "success": False,
            "message": str(ex)
        }), 500
