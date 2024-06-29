from Engine import create_app, socket_io
from flask import Flask

app: Flask = create_app()

if __name__ == "__main__":
    socket_io.run(app, debug=True, use_reloader=False, log_output=True)