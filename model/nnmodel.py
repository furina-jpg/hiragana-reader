# this is totally skibidi sugoi sauce

import torch, json
from datetime import datetime

def save_data(map, label):
    with open('data/data.json', 'a') as database:
        json.dump({'map': map, 'label': label}, database)
        database.write('\n')