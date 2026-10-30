from flask import (
    Flask,
    render_template
)

from config import (
    AZURE_OPENAI_DEPLOYMENT,
    MAX_UPLOAD_SIZE_MB
)

# =====================================
# ROUTES
# =====================================

from routes.chat_routes import (
    chat_bp
)

from routes.invoice_routes import (
    invoice_bp
)

from routes.project_routes import (
    project_bp
)

from routes.executive_routes import (
    executive_bp
)

from routes.customer_routes import (
    customer_bp
)

from routes.admin_routes import (
    admin_bp
)

from routes.sample_data_routes import (
    sample_bp
)

from routes.auth_routes import (
    auth_bp
)

from routes.errors import (
    register_handlers
)


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.secret_key = (
        "rioclaro-secret-key"
    )

    app.config[
        "MAX_CONTENT_LENGTH"
    ] = (
        MAX_UPLOAD_SIZE_MB
        * 1024
        * 1024
    )

    # =====================================
    # HOME
    # =====================================

    @app.route("/")
    def home():

        return render_template(
            "index.html"
        )

    # =====================================
    # LOGIN
    # =====================================

    @app.route("/login")
    def login_page():

        return render_template(
            "login.html"
        )

    # =====================================
    # HEALTH
    # =====================================

    @app.route("/health")
    def health():

        return {

            "status":
                "healthy",

            "application":
                "Rio Claro AI Assistant",

            "deployment":
                AZURE_OPENAI_DEPLOYMENT,

            "provider":
                "Azure OpenAI"

        }, 200

    # =====================================
    # AUTH
    # =====================================

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    # =====================================
    # CHAT
    # =====================================

    app.register_blueprint(
        chat_bp,
        url_prefix="/api/chat"
    )

    # =====================================
    # FACTURAS
    # =====================================

    app.register_blueprint(
        invoice_bp,
        url_prefix="/api/invoice"
    )

    # =====================================
    # PROYECTO
    # =====================================

    app.register_blueprint(
        project_bp,
        url_prefix="/api/project"
    )

    # =====================================
    # DIRECTOR GENERAL
    # =====================================

    app.register_blueprint(
        executive_bp,
        url_prefix="/api/executive"
    )

    # =====================================
    # GERENCIA
    # =====================================

    app.register_blueprint(
        customer_bp,
        url_prefix="/api/customer"
    )

    # =====================================
    # SISTEMAS
    # =====================================

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )

    # =====================================
    # SAMPLE DATA
    # =====================================

    app.register_blueprint(
        sample_bp,
        url_prefix="/api/sample"
    )

    # =====================================
    # ERROR HANDLERS
    # =====================================

    register_handlers(
        app
    )

    return app


app = create_app()

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True
    )