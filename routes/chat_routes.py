from flask import (
    Blueprint,
    jsonify,
    request
)

from services.chat_service import (
    ask_chatbot
)

chat_bp = Blueprint(
    "chat",
    __name__
)


@chat_bp.route(
    "/ask",
    methods=["POST"]
)
def ask():

    try:

        body = request.get_json()

        if not body:

            return jsonify({
                "success": False,
                "message":
                    "JSON payload required"
            }), 400

        question = (
            body.get(
                "question",
                ""
            ).strip()
        )

        if not question:

            return jsonify({
                "success": False,
                "message":
                    "Question is required"
            }), 400

        answer = ask_chatbot(
            question
        )

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as ex:

        return jsonify({
            "success": False,
            "message": str(ex)
        }), 500
