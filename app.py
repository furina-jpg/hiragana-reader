from flask import Flask, request, jsonify, render_template
import numpy

app = Flask(__name__) # initializes my code as an app

@app.route('/')
def load(): # loads the interface
    return render_template('interface/interface.html')

@app.route('/read', methods=['POST']) # reading submitted pixel data
def read(): 
    data = request.get_json() # gets the data from the request
    map = data['map']

    # temporary: flatten map into a sum
    mapsum = numpy.sum(map)

    return jsonify({"result":mapsum})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) # runs the app on port 10000