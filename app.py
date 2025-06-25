from flask import Flask, request, jsonify, render_template
import numpy

app = Flask(__name__) # initializes my code as an app

@app.route('/')
def load():
    return render_template('interface.html')

@app.route('/', methods=['POST'])
def read():
    return jsonify({"result":4})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)