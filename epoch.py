import torch, torch.nn as nn, torch.optim as optim, csv, random, os
from nnmodel import HGCNN 

# Load & format training data, order it randomly
def format_data(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            row = [int(r.strip()) for r in row if r.strip()]
            X = torch.tensor(row[:-1], dtype=torch.float32).view(1, 28, 28)
            y = torch.tensor(row[-1], dtype=torch.long)
            data.append((X, y))
    
    random.shuffle(data)  # ✨ Shuffles in-place
    return data

# Define model
model = HGCNN()

# this is only for when i change the number of filters/the kernel sizes in the model and i have to delete the old param.pth
if os.path.exists('param.pth'):
    model.load_state_dict(torch.load('param.pth'))
else:
    print("No pre-trained model found, starting from scratch.")
    model.eval()

# initialize loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

# Wash noise by reinitializing
def reset_weights(m):
    if hasattr(m, 'reset_parameters'):
        m.reset_parameters()
model.apply(reset_weights)

scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=6, gamma=0.7)

# Training loop
model.train()
EPOCHS = 48
for epoch in range(EPOCHS):
    # Prepare data
    total_loss = 0.0
    data = format_data("training_data.csv")
    for X_i, y_i in data:
        optimizer.zero_grad()
        output = model(X_i.unsqueeze(0))
        loss = criterion(output, y_i.unsqueeze(0))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    scheduler.step() 
    print(f"Epoch {epoch+1} || Average loss: {total_loss / len(data):.4f}")

# Save weights
torch.save(model.state_dict(), "param.pth")
print("Model retrained and weights saved.")