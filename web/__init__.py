# dummyapp/app/__init__.py
from flask import Flask
app = Flask(__name__)
from app import views
