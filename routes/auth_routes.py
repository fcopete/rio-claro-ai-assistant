from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from services.auth_service import (
    authenticate,
    get_role,
    user_exists,
    list_users
)

auth_bp = Blueprint(
    "auth",
    __name__
)

# ==========================================
# LOGIN
# ==========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        payload = (
            request.get_json()
        )

        if not payload:

            return jsonify({

                "success": False,

                "message":
                    "JSON payload required"

            }), 400

        username = (
            payload
            .get(
                "username",
                ""
            )
            .strip()
            .upper()
        )

        password = (
            payload
            .get(
                "password",
                ""
            )
            .strip()
        )

        if not username:

            return jsonify({

                "success": False,

                "message":
                    "Username required"

            }), 400

        if not password:

            return jsonify({

                "success": False,

                "message":
                    "Password required"

            }), 400

        user = authenticate(
            username,
            password
        )

        if not user:

            return jsonify({

                "success": False,

                "message":
                    "Credenciales inválidas"

            }), 401

        session.clear()

        session["authenticated"] = True
        session["user"] = user["username"]
        session["role"] = user["role"]

        return jsonify({

            "success": True,

            "authenticated":
                True,

            "user":
                user["username"],

            "role":
                user["role"]

        })

    except Exception as ex:

        return jsonify({

            "success": False,

            "message":
                str(ex)

        }), 500


# ==========================================
# LOGOUT
# ==========================================

@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():

    try:

        session.clear()

        return jsonify({

            "success": True,

            "message":
                "Sesión finalizada"

        })

    except Exception as ex:

        return jsonify({

            "success": False,

            "message":
                str(ex)

        }), 500


# ==========================================
# CURRENT USER
# ==========================================

@auth_bp.route(
    "/me",
    methods=["GET"]
)
def me():

    try:

        return jsonify({

            "authenticated":
                bool(
                    session.get(
                        "authenticated"
                    )
                ),

            "user":
                session.get(
                    "user"
                ),

            "role":
                session.get(
                    "role"
                )
        })

    except Exception as ex:

        return jsonify({

            "success": False,

            "message":
                str(ex)

        }), 500


# ==========================================
# VALIDATE SESSION
# ==========================================

@auth_bp.route(
    "/validate",
    methods=["GET"]
)
def validate():

    authenticated = (
        session.get(
            "authenticated",
            False
        )
    )

    if not authenticated:

        return jsonify({

            "success": False,

            "authenticated":
                False

        }), 401

    return jsonify({

        "success": True,

        "authenticated":
            True,

        "user":
            session.get(
                "user"
            ),

        "role":
            session.get(
                "role"
            )
    })


# ==========================================
# ROLE
# ==========================================

@auth_bp.route(
    "/role",
    methods=["GET"]
)
def role():

    if not session.get(
        "authenticated"
    ):

        return jsonify({

            "success": False,

            "message":
                "Not authenticated"

        }), 401

    return jsonify({

        "success": True,

        "role":
            session.get(
                "role"
            )
    })


# ==========================================
# USERS (DEMO)
# ==========================================

@auth_bp.route(
    "/users",
    methods=["GET"]
)
def users():

    return jsonify({

        "success": True,

        "users":
            list_users()
    })


# ==========================================
# USER EXISTS
# ==========================================

@auth_bp.route(
    "/exists/<username>",
    methods=["GET"]
)
def exists(
    username
):

    return jsonify({

        "success": True,

        "exists":
            user_exists(
                username
            )
    })


# ==========================================
# ROLE LOOKUP
# ==========================================

@auth_bp.route(
    "/user-role/<username>",
    methods=["GET"]
)
def user_role(
    username
):

    role = get_role(
        username
    )

    return jsonify({

        "success": True,

        "role":
            role
    })