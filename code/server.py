'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe
from app import app

server = app.server


if __name__ == "__main__":
    app.run_server(port=8050)
