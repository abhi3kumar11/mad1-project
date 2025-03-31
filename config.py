import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
