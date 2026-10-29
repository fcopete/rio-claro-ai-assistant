from flask import jsonify
def register_handlers(app):
    @app.errorhandler(404)
    def nf(e): return jsonify({"success":False,"message":"Route not found"}),404
