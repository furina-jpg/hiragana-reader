from flask import Flask, request, jsonify, render_template
from nnmodel import HGCNN, lossfunc, optimizer
import torch, torch.nn as nn, torch.nn.functional as func, torch.optim as optim

app = Flask(__name__) # initializes app

# creating the hiragana dictionaries for later
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
model.load_state_dict(torch.load('param.pth')) # loads the model weights from model.pth
# model.eval() # only necessary when inferring, not training !!!
lossfunc = nn.CrossEntropyLoss() # loss function for training, cross entropy loss
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=0.0005) # optimizer for training, stochastic gradient descent

# loads the interface
@app.route('/')
def load(): 
    return render_template('interface.html')

# reading submitted pixel data
@app.route('/read', methods=['POST']) 
def predict(): 
    data = request.get_json() # gets the data from the request
    map = data['map']
    label = input_dict[data['label']] # converts user input to an integer label

    y = torch.tensor([label], dtype=torch.long)
    
    maptensor = torch.tensor(map, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    # with torch.no_grad(): # no need to track gradients for inference, necessary for training !!!
    output = model(maptensor) # runs the model on the input data
    loss = lossfunc(output, y)
    optimizer.zero_grad() # zeroes the gradients before backpropagation
    loss.backward() # backpropagates the loss
    optimizer.step() # updates the model weights
    probs = func.softmax(output, dim=1)  # convert output activations to probabilities
    confidence, prediction = torch.max(probs, dim=1)

    # saving the model state and training data
    torch.save(model.state_dict(), "param.pth")
    with open("training_data.csv", "a") as f:
        flat = [str(px) for row in map for px in row]
        f.write(", ".join(flat + [str(label)]) + "\n")

    return jsonify({
        'result': hiragana_dict[prediction],
        "confidence": float(confidence.item())
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000) # runs the app on port 10000