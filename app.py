from flask import Flask, render_template

from routes.chat_routes import chat_bp
from routes.invoice_routes import invoice_bp
from routes.project_routes import project_bp
from routes.errors import register_handlers

from config import (
    AZURE_OPENAI_DEPLOYMENT
)


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config["MAX_CONTENT_LENGTH"] = (
        10 * 1024 * 1024
    )

    @app.route("/")
    def home():

        return render_template(
            "index.html"
        )

    @app.route("/health")
    def health():

        return {
            "status": "healthy",
            "application":
                "Rio Claro AI Assistant",
            "deployment":
                AZURE_OPENAI_DEPLOYMENT
        }, 200

    app.register_blueprint(
        chat_bp,
        url_prefix="/api/chat"
    )

    app.register_blueprint(
        invoice_bp,
        url_prefix="/api/invoice"
    )

    app.register_blueprint(
        project_bp,
        url_prefix="/api/project"
    )

    register_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
