from flask import Flask
from src import displaymessage
app = Flask(__name__)

@app.route("/message")
def hello_world():
    displaymessage.test()
    return "Hello, World!"

if __name__ == '__main__':
   app.run()
