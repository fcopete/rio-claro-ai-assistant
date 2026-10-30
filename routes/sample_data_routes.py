from flask import Blueprint, jsonify

from services.sample_data_service import (
    load_sample_data
)

sample_bp = Blueprint(
    "sample",
    __name__
)


@sample_bp.route(
    "/all",
    methods=["GET"]
)
def all_data():

    return jsonify(
        load_sample_data()
    )


@sample_bp.route(
    "/dashboard",
    methods=["GET"]
)
def dashboard():

    data = load_sample_data()

    return jsonify(
        data.get(
            "dashboard",
            {}
        )
    )


@sample_bp.route(
    "/sales",
    methods=["GET"]
)
def sales():

    data = load_sample_data()

    return jsonify(
        data.get(
            "executive_summary",
            {}
        )
    )


@sample_bp.route(
    "/customers",
    methods=["GET"]
)
def customers():

    data = load_sample_data()

    return jsonify(
        data.get(
            "customers",
            {}
        )
    )


@sample_bp.route(
    "/warehouse",
    methods=["GET"]
)
def warehouse():

    data = load_sample_data()

    return jsonify(
        data.get(
            "warehouse",
            {}
        )
    )


@sample_bp.route(
    "/invoices",
    methods=["GET"]
)
def invoices():

    data = load_sample_data()

    return jsonify(
        data.get(
            "invoices",
            []
        )
    )


@sample_bp.route(
    "/invoice-analysis",
    methods=["GET"]
)
def invoice_analysis():

    data = load_sample_data()

    return jsonify(
        data.get(
            "invoice_analysis",
            {}
        )
    )


@sample_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory():

    data = load_sample_data()

    warehouse_data = data.get(
        "warehouse",
        {}
    )

    return jsonify(
        warehouse_data.get(
            "inventory",
            []
        )
    )


@sample_bp.route(
    "/chat-examples",
    methods=["GET"]
)
def chat_examples():

    data = load_sample_data()

    return jsonify(
        data.get(
            "chat_examples",
            []
        )
    )


@sample_bp.route(
    "/roles",
    methods=["GET"]
)
def roles():

    data = load_sample_data()

    return jsonify(
        data.get(
            "roles",
            {}
        )
    )


@sample_bp.route(
    "/admin",
    methods=["GET"]
)
def admin():

    data = load_sample_data()

    return jsonify(
        data.get(
            "admin_status",
            {}
        )
    )