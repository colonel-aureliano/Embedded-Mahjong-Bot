import torch
from torchvision import datasets, models
from torchvision.transforms import v2 as transforms_v2
from torch.utils.data import DataLoader

# Define transformations for the train and validation sets
train_transforms = transforms_v2.Compose([
    transforms_v2.Resize((224, 224)),  # Resize images to fit the model
    transforms_v2.RandomHorizontalFlip(),  # Random horizontal flip
    transforms_v2.Compose([transforms_v2.ToImage(), transforms_v2.ToDtype(torch.float32, scale=True)]),  # Convert images to tensor
    transforms_v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalize images
])

val_transforms = transforms_v2.Compose([
    transforms_v2.Resize((224, 224)),
    transforms_v2.Compose([transforms_v2.ToImage(), transforms_v2.ToDtype(torch.float32, scale=True)]),
    transforms_v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the datasets
train_data = datasets.ImageFolder('data/train_grouped', transform=train_transforms)
val_data = datasets.ImageFolder('data/val_grouped', transform=val_transforms)

# Define the DataLoaders
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

# ================================================

model = models.mobilenet_v2(pretrained=True)  # Load pretrained MobileNetV2

# Freeze all the layers in the base model
for param in model.parameters():
    param.requires_grad = False

# Modify the classifier to fit the number of classes
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 60)  # Assume 60 classes for mahjong tiles

# Check if GPU is available and move the model to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# ================================================

import torch.optim as optim

criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.01)  # Optimize only the classifier

def train_model(model, criterion, optimizer, train_loader, val_loader, epochs=10):
    for epoch in range(epochs):
        model.train()  # Set model to training mode
        running_loss = 0.0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}')

        # Validation step
        model.eval()  # Set model to evaluation mode
        with torch.no_grad():
            correct = 0
            total = 0
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print(f'Validation Accuracy: {100 * correct / total}%')

train_model(model, criterion, optimizer, train_loader, val_loader)

torch.save(model.state_dict(), 'mahjong_mobilenet_v2_state_dict.pth')
torch.save(model, 'mahjong_mobilenet_v2_full_model.pth')