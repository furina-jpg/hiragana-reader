# this is totally skibidi sugoi sauce

import torch, json
from datetime import datetime

def save_data(map, label):
    sample = {'map': map, 'label': label}
    with open('data/data.json', 'a') as f:
        json.dump(sample, f)
        f.write('\n')