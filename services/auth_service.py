from config import (
    DEMO_USERS
)


# ==========================================
# GET USER
# ==========================================

def get_user(
    username
):
    """
    Obtiene los datos de un usuario.
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


# ==========================================
# AUTHENTICATE
# ==========================================

def authenticate(
    username,
    password
):
    """
    Valida usuario y contraseña.

    Retorna:

        dict -> usuario válido

        None -> autenticación inválida
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


# ==========================================
# GET ROLE
# ==========================================

def get_role(
    username
):
    """
    Obtiene el rol de un usuario.
    """

    user = get_user(
        username
    )

    if not user:

        return None

    return user.get(
        "role"
    )


# ==========================================
# USER EXISTS
# ==========================================

def user_exists(
    username
):
    """
    Verifica si un usuario existe.
    """

    return (
        get_user(
            username
        )
        is not None
    )


# ==========================================
# USER LIST
# ==========================================

def list_users():
    """
    Lista usuarios
    disponibles en el sistema.
    """

    return list(
        DEMO_USERS.keys()
    )


# ==========================================
# ROLE VALIDATION
# ==========================================

def has_role(
    username,
    role
):
    """
    Verifica si un usuario
    pertenece a un rol.
    """

    user_role = get_role(
        username
    )

    return (
        user_role == role
    )


# ==========================================
# ROLE CHECKS
# ==========================================

def is_director(
    username
):

    return has_role(
        username,
        "director"
    )


def is_finance(
    username
):

    return has_role(
        username,
        "finance"
    )


def is_manager(
    username
):

    return has_role(
        username,
        "manager"
    )


def is_warehouse(
    username
):

    return has_role(
        username,
        "warehouse"
    )


def is_admin(
    username
):

    return has_role(
        username,
        "admin"
    )