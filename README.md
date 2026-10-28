Río Claro AI Assistant
Aplicación empresarial basada en:

Flask 3.x
Azure OpenAI
Azure AI Document Intelligence
Azure App Service
Microsoft AI Foundry
Funcionalidades
Chat IA
POST /api/chat/ask

Procesamiento de Facturas
POST /api/invoice/upload

Estado
GET /health

Información del Proyecto
GET /api/project/info

Test de Conectividad
GET /api/project/test

Instalación
Crear entorno virtual:

python -m venv .venv
Activar:

Windows

.venv\Scripts\activate
Linux / Mac

source .venv/bin/activate
Instalar dependencias:

pip install -r requirements.txt
Variables de entorno
Copiar:

.env.example
a:

.env
y completar:

AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
DOCUMENT_INTELLIGENCE_ENDPOINT
DOCUMENT_INTELLIGENCE_KEY
Ejecución
python app.py
Aplicación:

http://localhost:5000
Azure App Service
Startup Command:

gunicorn --bind=0.0.0.0 --timeout 600 app:app
APIs
GET /

GET /healths

POST /api/chat/ask

POST /api/invoice/upload

GET /api/project/info

GET /api/project/test
