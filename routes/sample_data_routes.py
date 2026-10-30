from flask import (
    Blueprint,
    jsonify
)

from services.sample_data_service import (
    load_sample_data
)

sample_bp = Blueprint(
    "sample",
    __name__
)

# ==========================================
# TODOS LOS DATOS
# ==========================================

@sample_bp.route(
    "/all",
    methods=["GET"]
)
def all_data():

    data = load_sample_data()

    return jsonify(data)


# ==========================================
# DASHBOARD
# ==========================================

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


# ==========================================
# VENTAS EJECUTIVAS
# ==========================================

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


# ==========================================
# CLIENTES
# ==========================================

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


# ==========================================
# INVENTARIO / BODEGA
# ==========================================

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


# ==========================================
# FACTURAS
# ==========================================

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


# ==========================================
# ANALISIS IA DEMO
# ==========================================

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


# ==========================================
# ADMINISTRACION
# ==========================================

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


# ==========================================
# INVENTARIO COMPLETO
# ==========================================

@sample_bp.route(
    "/inventory",
    methods=["GET"]
)
def inventory():

    data = load_sample_data()

    warehouse = data.get(
        "warehouse",
 