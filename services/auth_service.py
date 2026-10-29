import os

USERS = {

    "DIRGEN": {
        "password":
            os.getenv(
                "DIRGEN_PASSWORD"
            ),
        "role":
            "director"
    },

    "COBRANZA": {
        "password":
            os.getenv(
                "COBRANZA_PASSWORD"
            ),
        "role":
            "finance"
    },

    "GERENCIA": {
        "password":
            os.getenv(
                "GERENCIA_PASSWORD"
            ),
        "role":
            "manager"
    },

    "BODEGA": {
        "password":
            os.getenv(
                "BODEGA_PASSWORD"
            ),
        "role":
            "warehouse"
    },

    "SISTEMAS": {
        "password":
            os.getenv(
                "SISTEMAS_PASSWORD"
            ),
        "role":
            "admin"
    }
}
