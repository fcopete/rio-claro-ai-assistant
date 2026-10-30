from config import (
    DEMO_USERS
)


def authenticate(
    username,
    password
):

    user = DEMO_USERS.get(
        username
    )

    if not user:

        return None

    if (
        user["password"] !=
        password
    ):

        return None

    return {

        "username":
            username,

        "role":
            user["role"]
    }