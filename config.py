import os
from dotenv import load_dotenv
load_dotenv()

def get_required_env(variable_name):
    value=os.getenv(variable_name)
    if not value: raise ValueError(f"Missing required environment variable: {variable_name}")
    return value

def get_optional_env(variable_name, default_value=None):
    return os.getenv(variable_name, default_value)
APP_NAME="Rio Claro AI Assistant"
APP_VERSION="1.0.0"
APP_ENV=get_optional_env("FLASK_ENV","production")
DEBUG_MODE=get_optional_env("FLASK_DEBUG","false").lower()=="true"
SECRET_KEY=get_optional_env("SECRET_KEY","rioclaro-secret-key")
MAX_UPLOAD_SIZE_MB=10
MAX_CONTENT_LENGTH=MAX_UPLOAD_SIZE_MB*1024*1024
ALLOWED_EXTENSIONS={"pdf","png","jpg","jpeg"}
AZURE_OPENAI_ENDPOINT=get_required_env("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY=get_required_env("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION=get_optional_env("AZURE_OPENAI_API_VERSION","2024-12-01-preview")
AZURE_OPENAI_DEPLOYMENT=get_required_env("AZURE_OPENAI_DEPLOYMENT")
DOCUMENT_INTELLIGENCE_ENDPOINT=get_required_env("DOCUMENT_INTELLIGENCE_ENDPOINT")
DOCUMENT_INTELLIGENCE_KEY=get_required_env("DOCUMENT_INTELLIGENCE_KEY")
SAMPLE_DATA_FILE=os.path.join('data','sample_data.json')
MAX_CHAT_HISTORY=20
MAX_CHAT_RESPONSE_TOKENS=1000
CHAT_TEMPERATURE=0.3
