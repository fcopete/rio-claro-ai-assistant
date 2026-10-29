import os

from dotenv import (
    load_dotenv
)

load_dotenv()


def get_required_env(
    variable_name
):

    value = os.getenv(
        variable_name
    )

    if not value:

        raise ValueError(
            f"Missing environment variable: "
            f"{variable_name}"
        )

    return value


# ======================================
# AZURE OPENAI
# ======================================

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
    os.getenv(
        "AZURE_OPENAI_API_VERSION",
        "2024-12-01-preview"
    )
)

AZURE_OPENAI_DEPLOYMENT = (
    get_required_env(
        "AZURE_OPENAI_DEPLOYMENT"
    )
)

# ======================================
# DOCUMENT INTELLIGENCE
# ======================================

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

# ======================================
# GENERAL APP SETTINGS
# ======================================

MAX_UPLOAD_SIZE_MB = 10

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}
