from config import (
    DEMO_USERS
)


def get_user(
    username
):
    """
    Obtiene un usuario desde
    la configuración.
    """

    if not username:
        return None

    username = (
        username
        .strip()
        .upper()
    )

    return DEMO_USERS.get(
        username
    )


def authenticate(
    username,
    password
):
    """
    Valida usuario y contraseña.

    Retorna:
        dict -> usuario válido
        None -> autenticación fallida
    """

    user = get_user(
        username
    )

    if not user:

        return None

    stored_password = (
        user.get(
            "password"
        )
    )

    if (
        stored_password !=
        password
    ):

        return None

    return {

        "username":
            username.upper(),

        "role":
            user.get(
                "role"
            )
    }


def get_role(
    username
):
    """
    Obtiene únicamente el rol
    asociado al usuario.
    """

    user = get_user(
        username
    )

    if not user:

        return None

    return user.get(
        "role"
    )


def user_exists(
    username
):
    """
    Verifica existencia de usuario.
    """

    return (
        get_user(
            username
        )
        is not None
    )


def list_users():
    """
    Retorna usuarios disponibles.
    Útil para ambiente demo.
    """

    return list(
        DEMO_USERS.keys()
    )