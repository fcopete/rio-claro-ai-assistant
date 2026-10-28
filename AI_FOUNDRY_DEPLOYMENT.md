Deployment Guide
Proyecto
franciscocopete-ia-001

Azure OpenAI
Variables requeridas:

AZURE_OPENAI_ENDPOINT

AZURE_OPENAI_API_KEY

AZURE_OPENAI_API_VERSION

AZURE_OPENAI_DEPLOYMENT
Azure AI Document Intelligence
DOCUMENT_INTELLIGENCE_ENDPOINT

DOCUMENT_INTELLIGENCE_KEY
Startup Command
gunicorn --bind=0.0.0.0 --timeout 600 app:app
Validación
Health:

GET /health
Chat:

POST /api/chat/ask
Facturas:

POST /api/invoice/upload
