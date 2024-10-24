import firebase_admin 
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
load_dotenv()

# get credentials from .env
credential_firebase = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# check if firebase is not initialized
if not firebase_admin._apps:
    # Initialize the app with a service account, granting admin privileges
    cred = credentials.Certificate(credential_firebase)
    app = firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
print("Database connected")
