from flask import Flask, request, jsonify, render_template
import numpy

app = Flask(__name__) # initializes my code as an app

@app.route('/')
def load():
    return render_template('interface.html')

@app.route('/', methods=['POST'])
def read():
    return jsonify({"result":4})
