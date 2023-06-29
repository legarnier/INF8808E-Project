'''
    Contains the server to run our application.
'''
from app import app

server = app.server


if __name__ == "__main__":
    app.run_server(port=8050)
