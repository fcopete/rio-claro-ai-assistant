from azure.core.credentials import (
    AzureKeyCredential
)

from azure.ai.documentintelligence import (
    DocumentIntelligenceClient
)

from config import (
    DOCUMENT_INTELLIGENCE_ENDPOINT,
    DOCUMENT_INTELLIGENCE_KEY
)

client = (
    DocumentIntelligenceClient(
        endpoint=
        DOCUMENT_INTELLIGENCE_ENDPOINT,

        credential=
        AzureKeyCredential(
            DOCUMENT_INTELLIGENCE_KEY
        )
    )
)


def analyze_invoice(
    uploaded_file
):

    poller = (
        client.begin_analyze_document(
            "prebuilt-invoice",
            uploaded_file.read()
        )
    )

    result = poller.result()

    return {
        "documents":
            len(result.documents)
    }
