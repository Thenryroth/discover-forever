from flask import Flask, request

app = Flask(__name__)

@app.route('/auth',methods=['GET'])
def hello_world():
    return 'Hello World'
