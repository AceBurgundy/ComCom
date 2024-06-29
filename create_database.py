from Engine import create_app
from flask import Flask
from Engine import db

app: Flask = create_app()

with app.app_context():
    db.create_all()
