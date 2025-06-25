from flask import Flask, request, jsonify, render_template
import numpy

app = Flask(__name__) # initializes my code as an app

@app.route('/')
def load(): # loads the interface
    return render_template('interface.html')

@app.route('/read', methods=['POST']) # reading submitted pixel data
def read_data(): 
    data = request.get_json() # gets the data from the request
    map = data['map']

    mapsum = numpy.sum(map) # temporary: flatten map into a sum

    if map:
        return jsonify({'result':mapsum}) # returns result
    return jsonify({'result':'Error'}) # retunrs error if array fails to be read

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) # runs the app on port 10000