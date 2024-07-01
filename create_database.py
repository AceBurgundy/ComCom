from typing import List
from Engine import create_app
from flask import Flask
from Engine import db
import os

def create_database() -> None:
    app: Flask = create_app()

    with app.app_context():
        db.create_all()

def recreate_database() -> None:
    folder_path: str = "instance"

    if not os.path.exists(folder_path) and not os.path.isdir(folder_path):
        print("Skipping deletion of database as the 'instance' folder does not exist. Creating a new database")
        create_database()
        return

    # List the files in the folder
    files: List[str] = os.listdir(folder_path)

    # Check if there are files in the folder
    if len(files) <= 0:
        print("The folder is empty. Creating new database.")
        create_database()
        return

    first_file: str = files[0]
    file_path: str = os.path.join(folder_path, first_file)

    os.remove(file_path)
    create_database()

if __name__ == '__main__':
    recreate_database()