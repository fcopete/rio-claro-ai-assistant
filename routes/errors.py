from flask import jsonify


def register_handlers(app):

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "message":
                "Route not found"
        }), 404

    @app.errorhandler(500)
    def internal(error):

        return jsonify({
            "success": False,
            "message":
                "Internal error"
        }), 500
