from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import os
from pathlib import Path

__all__ = ('celery_app',)

BASE_DIR = Path(__file__).resolve().parent.parent
cred_path = os.path.join(BASE_DIR, "boida_firebase_admin.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
