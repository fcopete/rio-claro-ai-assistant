from pathlib import Path

FILES = {}

FILES["app.py"] = r'''
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
'''

FILES["config.py"] = r'''
import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(
    variable_name
):

    value = os.getenv(
        variable_name
    )

    if not value:

        raise ValueError(
            f"Missing environment variable: "
            f"{variable_name}"
        )

    return value


AZURE_OPENAI_ENDPOINT = (
    get_required_env(
        "AZURE_OPENAI_ENDPOINT"
    )
)

AZURE_OPENAI_API_KEY = (
    get_required_env(
        "AZURE_OPENAI_API_KEY"
    )
)

AZURE_OPENAI_API_VERSION = (
    os.getenv(
        "AZURE_OPENAI_API_VERSION",
        "2024-12-01-preview"
    )
)

AZURE_OPENAI_DEPLOYMENT = (
    get_required_env(
        "AZURE_OPENAI_DEPLOYMENT"
    )
)

DOCUMENT_INTELLIGENCE_ENDPOINT = (
    get_required_env(
        "DOCUMENT_INTELLIGENCE_ENDPOINT"
    )
)

DOCUMENT_INTELLIGENCE_KEY = (
    get_required_env(
        "DOCUMENT_INTELLIGENCE_KEY"
    )
)
'''

FILES["routes/chat_routes.py"] = r'''
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
'''

FILES["routes/invoice_routes.py"] = r'''
from flask import (
    Blueprint,
    jsonify,
    request
)

from services.document_service import (
    analyze_invoice
)

invoice_bp = Blueprint(
    "invoice",
    __name__
)

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = (
        filename
        .rsplit(".", 1)[1]
        .lower()
    )

    return (
        extension in
        ALLOWED_EXTENSIONS
    )


@invoice_bp.route(
    "/upload",
    methods=["POST"]
)
def upload_invoice():

    try:

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "message":
                    "File not found"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message":
                    "Invalid file"
            }), 400

        if not allowed_file(
            file.filename
        ):

            return jsonify({
                "success": False,
                "message":
                    "Invalid file format"
            }), 400

        result = analyze_invoice(
            file
        )

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as ex:

        return jsonify({
            "success": False,
            "message": str(ex)
        }), 500
'''

FILES["routes/project_routes.py"] = r'''
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
'''

FILES["routes/errors.py"] = r'''
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
'''

FILES["services/chat_service.py"] = r'''
from openai import AzureOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

SYSTEM_PROMPT = """
You are Rio Claro assistant.
"""


def ask_chatbot(question):

    response = (
        client.chat.completions.create(
            model=
                AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {
                    "role":"system",
                    "content":
                    SYSTEM_PROMPT
                },
                {
                    "role":"user",
                    "content":
                    question
                }
            ]
        )
    )

    return (
        response
        .choices[0]
        .message.content
    )


def test_connection():

    client.chat.completions.create(
        model=
            AZURE_OPENAI_DEPLOYMENT,

        messages=[
            {
                "role":"user",
                "content":"test"
            }
        ],

        max_tokens=3
    )

    return True
'''

FILES["services/document_service.py"] = r'''
from azure.core.credentials import (
    AzureKeyCredential
)

from azure.ai.documentintelligence import (
    DocumentIntelligenceClient
)

from config import (
    DOCUMENT_INTELLIGENCE_ENDPOINT,
    DOCUMENT_INTELLIGENCE_KEY
)

client = (
    DocumentIntelligenceClient(
        endpoint=
        DOCUMENT_INTELLIGENCE_ENDPOINT,

        credential=
        AzureKeyCredential(
            DOCUMENT_INTELLIGENCE_KEY
        )
    )
)


def analyze_invoice(
    uploaded_file
):

    poller = (
        client.begin_analyze_document(
            "prebuilt-invoice",
            uploaded_file.read()
        )
    )

    result = poller.result()

    return {
        "documents":
            len(result.documents)
    }
'''

FILES["services/search_service.py"] = r'''
class SearchService:

    def search(
        self,
        query
    ):
        return []
'''
# crear archivos

for filename, content in FILES.items():

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )

print(
    "Proyecto Python generado correctamente."
)