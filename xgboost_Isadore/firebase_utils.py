#firebase_utils.py
import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
def initialize_firebase():
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db