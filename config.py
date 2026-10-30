import os

from dotenv import (
    load_dotenv
)

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# HELPERS
# ==================================================

def get_required_env(
    variable_name
):

    value = os.getenv(
        variable_name
    )

    if not value:

        raise ValueError(
            f"Missing required environment variable: "
            f"{variable_name}"
        )

    return value


def get_optional_env(
    variable_name,
    default_value=None
):

    return os.getenv(
        variable_name,
        default_value
    )


# ==================================================
# APPLICATION
# ==================================================

APP_NAME = (
    get_optional_env(
        "APP_NAME",
        "Rio Claro AI Assistant"
    )
)

APP_VERSION = (
    get_optional_env(
        "APP_VERSION",
        "1.0.0"
    )
)

SECRET_KEY = (
    get_optional_env(
        "SECRET_KEY",
        "rioclaro-secret-key"
    )
)

FLASK_ENV = (
    get_optional_env(
        "FLASK_ENV",
        "production"
    )
)

FLASK_DEBUG = (
    get_optional_env(
        "FLASK_DEBUG",
        "false"
    ).lower()
    == "true"
)


# ==================================================
# FILES
# ==================================================

MAX_UPLOAD_SIZE_MB = int(
    get_optional_env(
        "MAX_UPLOAD_SIZE_MB",
        10
    )
)

MAX_CONTENT_LENGTH = (
    MAX_UPLOAD_SIZE_MB
    * 1024
    * 1024
)

ALLOWED_EXTENSIONS = {

    "pdf",

    "png",

    "jpg",

    "jpeg"
}


# ==================================================
# AZURE OPENAI
# ==================================================

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
    get_optional_env(
        "AZURE_OPENAI_API_VERSION",
        "2024-12-01-preview"
    )
)

AZURE_OPENAI_DEPLOYMENT = (
    get_required_env(
        "AZURE_OPENAI_DEPLOYMENT"
    )
)


# ==================================================
# DOCUMENT INTELLIGENCE
# ==================================================

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


# ==================================================
# CHAT SETTINGS
# ==================================================

MAX_CHAT_HISTORY = int(
    get_optional_env(
        "MAX_CHAT_HISTORY",
        20
    )
)

MAX_CHAT_RESPONSE_TOKENS = int(
    get_optional_env(
        "MAX_CHAT_RESPONSE_TOKENS",
        1000
    )
)

CHAT_TEMPERATURE = float(
    get_optional_env(
        "CHAT_TEMPERATURE",
        0.3
    )
)


# ==================================================
# SAMPLE DATA
# ==================================================

SAMPLE_DATA_FILE = (
    get_optional_env(
        "SAMPLE_DATA_FILE",
        "data/sample_data.json"
    )
)


# ==================================================
# SYSTEM
# ==================================================

HEALTH_STATUS_OK = (
    "healthy"
)

HEALTH_STATUS_ERROR = (
    "error"
)

SYSTEM_PROVIDER = (
    "Azure OpenAI"
)


# ==================================================
# ROLES
# ==================================================

ROLE_DIRECTOR = (
    "director"
)

ROLE_FINANCE = (
    "finance"
)

ROLE_MANAGER = (
    "manager"
)

ROLE_WAREHOUSE = (
    "warehouse"
)

ROLE_ADMIN = (
    "admin"
)


# ==================================================
# USERS
# ==================================================
# Para producción se recomienda mover estas
# credenciales a variables de entorno.
# ==================================================

DEMO_USERS = {

    "DIRGEN": {

        "password":
            get_optional_env(
                "DIRGEN_PASSWORD",
                "D1rG3n.2018"
            ),

        "role":
            ROLE_DIRECTOR
    },

    "COBRANZA": {

        "password":
            get_optional_env(
                "COBRANZA_PASSWORD",
                "C0BR4.2018"
            ),

        "role":
            ROLE_FINANCE
    },

    "GERENCIA": {

        "password":
            get_optional_env(
                "GERENCIA_PASSWORD",
                "G3r3n.2018"
            ),

        "role":
            ROLE_MANAGER
    },

    "BODEGA": {

        "password":
            get_optional_env(
                "BODEGA_PASSWORD",
                "B0D3.2018"
            ),

        "role":
            ROLE_WAREHOUSE
    },

    "SISTEMAS": {

        "password":
            get_optional_env(
                "SISTEMAS_PASSWORD",
                "S1st.2018"
            ),

        "role":
            ROLE_ADMIN
    }
}


# ==================================================
# EXECUTIVE DASHBOARD
# ==================================================

DEFAULT_BRANCHES = (

    get_optional_env(

        "DEFAULT_BRANCHES",

        (
            "Monterrey,"
            "León,"
            "CDMX,"
            "Guadalajara,"
            "Querétaro,"
            "Puebla"
        )
    )

).split(",")


# ==================================================
# FINANCE
# ==================================================

HIGH_RISK_THRESHOLD = int(
    get_optional_env(
        "HIGH_RISK_THRESHOLD",
        100000
    )
)

MEDIUM_RISK_THRESHOLD = int(
    get_optional_env(
        "MEDIUM_RISK_THRESHOLD",
        50000
    )
)


# ==================================================
# CUSTOMERS
# ==================================================

PENDING_CUSTOMER_DAYS = int(
    get_optional_env(
        "PENDING_CUSTOMER_DAYS",
        7
    )
)


# ==================================================
# WAREHOUSE
# ==================================================

LOW_STOCK_THRESHOLD = int(
    get_optional_env(
        "LOW_STOCK_THRESHOLD",
        50
    )
)


# ==================================================
# FEATURE FLAGS
# ==================================================

ENABLE_SPEECH_RECOGNITION = (
    get_optional_env(
        "ENABLE_SPEECH_RECOGNITION",
        "true"
    ).lower()
    == "true"
)

ENABLE_SAMPLE_DATA = (
    get_optional_env(
        "ENABLE_SAMPLE_DATA",
        "true"
    ).lower()
    == "true"
)

ENABLE_INVOICE_AI_ANALYSIS = (
    get_optional_env(
        "ENABLE_INVOICE_AI_ANALYSIS",
        "true"
    ).lower()
    == "true"
)

ENABLE_EXECUTIVE_DASHBOARD = (
    get_optional_env(
        "ENABLE_EXECUTIVE_DASHBOARD",
        "true"
    ).lower()
    == "true"
)