from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from services.auth_service import (
    authenticate
)

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        payload = (
            request.get_json()
        )

        username = (
            payload.get(
                "username",
                ""
            )
            .strip()
            .upper()
        )

        password = (
            payload.get(
                "password",
                ""
            )
            .strip()
        )

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

        session["user"] = (
            username
        )

        session["role"] = (
            user["role"]
        )

        return jsonify({

            "success": True,

            "user":
                username,

            "role":
                user["role"]

        })

    except Exception as ex:

        return jsonify({

            "success": False,

            "message":
                str(ex)

        }), 500


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():

    session.clear()

    return jsonify({

        "success": True

    })


@auth_bp.route(
    "/me",
    methods=["GET"]
)
def me():

    return jsonify({

        "authenticated":
            bool(
                session.get(
                    "user"
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


@auth_bp.route(
    "/validate",
    methods=["GET"]
)
def validate():

    if not session.get(
        "user"
    ):

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