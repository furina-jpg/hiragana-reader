# hey! this is where the most learning happened for me; going into this project, i had no idea
# how to connect my javascript to my python, let alone even use any of these packages. a lot of youtube,
# reading docs, asking chatgpt, and banging my head on my computer later, we're here.

# a lot of code is commneted out because it was originally used for writing the training data;
# you're free to look around if you want

from flask import Flask, request, jsonify, render_template
from nnmodel import HGCNN
import torch, torch.nn as nn, torch.nn.functional as func, torch.optim as optim, os

app = Flask(__name__) # initializes app?

# creating the input/output hiragana dictionaries for later
input_dict = {
    'a': 0, 'i': 1, 'u': 2, 'e': 3, 'o': 4,
    'ka': 5, 'ki': 6, 'ku': 7, 'ke': 8, 'ko': 9,
    'sa': 10, 'shi': 11, 'su': 12, 'se': 13, 'so': 14,
    'ta': 15, 'chi': 16, 'tsu': 17, 'te': 18, 'to': 19,
    'na': 20, 'ni': 21, 'nu': 22, 'ne': 23, 'no': 24,
    'ha': 25, 'hi': 26, 'hu': 27, 'he': 28, 'ho': 29,
    'ma': 30, 'mi': 31, 'mu': 32, 'me': 33, 'mo': 34,
    'ya': 35, 'yu': 36, 'yo': 37,
    'ra': 38, 'ri': 39, 'ru': 40, 're': 41, 'ro': 42,
    'wa': 43, 'wo': 44, 'n': 45,
}
hiragana_dict = {
    0: 'あ a', 1: 'い i', 2: 'う u', 3: 'え e', 4: 'お o',
    5: 'か ka', 6: 'き ki', 7: 'く ku', 8: 'け ke', 9: 'こ ko',
    10: 'さ sa', 11: 'し shi', 12: 'す su', 13: 'せ se', 14: 'そ so',
    15: 'た ta', 16: 'ち chi', 17: 'つ tsu', 18: 'て te', 19: 'と to',
    20: 'な na', 21: 'に ni', 22: 'ぬ nu', 23: 'ね ne', 24: 'の no',
    25: 'は ha', 26: 'ひ hi', 27: 'ふ hu', 28: 'へ he', 29: 'ほ ho',
    30: 'ま ma', 31: 'み mi', 32: 'む mu', 33: 'め me', 34: 'も mo',
    35: 'や ya', 36: 'ゆ yu', 37: 'よ yo',
    38: 'ら ra', 39: 'り ri', 40: 'る ru', 41: 'れ re', 42: 'ろ ro',
    43: 'わ wa', 44: 'を wo', 45: 'ん n',
}

# creating an instance of HGCNN
model = HGCNN()
if os.path.exists('param.pth'):
    model.load_state_dict(torch.load('param.pth')) # loads the model weights from param.pth
model.eval() # necessary for inference, not training
# model.train() # used for training, not inference. enables dropout and normalization

# so this is how they load the html/css/js apparently
@app.route('/')
def load(): 
    return render_template('interface.html')

# reading submitted pixel map
@app.route('/read', methods=['POST']) 
def predict(): 
    data = request.get_json() # gets the data from the request
    map = data['map']

    # the below was used for reading the labels

    # label = input_dict[data['label'].strip()] 
    # if not label in input_dict.values(): # checks if the label is valid
    #    return jsonify({
    #        'result': 'n/a',
    #        'confidence': 0.00,
    #        'error': 'Invalid label provided.'
    #    })

    maptensor = torch.tensor(map, dtype=torch.float32).unsqueeze(0).unsqueeze(0) # converts map to a pytorch-readable tensor

    with torch.no_grad(): # stops computer from calculating gradients since backprop isn't happening during inference, saves memory. enabled for inference, not for training
        output = model(maptensor) # runs my neural network on the input data
        confidence, prediction = torch.max(func.softmax(output, dim=1), dim=1) # converts output activations to probabilities & thus confidences
    # note that the above values are tensors & need to be converted to native python ints to be operated on
    # this is done with <thingy>.item()

    # the below was used for writing my maps & labels to a .csv file for training
    # there was originally a line for saving the state of the model, but i turned it off because
    # i was writing certain characters more than others and that was creating issues (esp since i was using SGD)

    # saving the model state, loss, & training data
    # with open("training_data.csv", "a") as f:
    #     flat = [str(px) for row in map for px in row]
    #     f.write(", ".join(flat + [str(label)]) + "\n")

    return jsonify({
        'result': hiragana_dict[prediction.item()],
        'confidence': round(confidence.item()*100, 2),
        'error': ''
        }) # sends back the result, a confidence as a percentage, and no error

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) # runs the app on port 10000 or something