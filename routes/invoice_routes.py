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
