import torch
from torchvision import datasets, models
from torchvision.transforms import v2 as transforms_v2
from torch.utils.data import DataLoader
import json
import sys
import os

# Assuming the model architecture is already defined
model = models.mobilenet_v2(weights="MobileNet_V2_Weights.DEFAULT")
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 42)  # Adjust for your number of classes

model.load_state_dict(torch.load('mahjong_mobilenet_v2_state_dict.pth'))
model.eval()  # Set the model to evaluation mode

############################################

val_transforms = transforms_v2.Compose([
    transforms_v2.Resize((224, 224)),
    transforms_v2.Compose([transforms_v2.ToImage(), transforms_v2.ToDtype(torch.float32, scale=True)]),
    transforms_v2.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

from torchvision.io import read_image

def predict_image(image_path, model, transform, device):
    model.eval()
    image = read_image(image_path)
    image = transform(image)  # Apply the same transforms as for training/validation
    image = image.unsqueeze(0)
    # image = image.to(device)  # Add batch dimension and send to device

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        predicted_idx = predicted.item()

    return predicted_idx  # Or return class label if you have a idx-to-class mapping

## group below code into a function
def do_single_image_pred(image_path, model, transform, device):    

    predicted_idx = predict_image(image_path, model, val_transforms, "")
    # print(f'Predicted class index: {predicted_idx}')

    # Load class_to_idx mapping from a JSON file
    with open('class_to_idx.json', 'r') as json_file:
        class_to_idx = json.load(json_file)

    # Invert the dictionary to create an index to class mapping
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    predicted_class = idx_to_class[predicted_idx]
    return predicted_class

def do_folder_pred(folder_path, model, transform, device):
    # Get the list of JPG files in the folder
    jpg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpeg")]
    # record all predicts and name of file in a tuple in a list
    predicts = []
    for file in jpg_files:
        image_path = os.path.join(folder_path, file)
        # call do_single_image_pred
        predict = do_single_image_pred(image_path, model, transform, device)
        predicts.append((file, predict))
    return predicts

## read command line arguments, if "-single" is present, parse second argument as image path and call do_single_image_pred, else if "-folder" is present, call do_folder_pred
if len(sys.argv) > 1:
    if sys.argv[1] == "-single":
        pred = do_single_image_pred(sys.argv[2], model, val_transforms, "")
        print(pred)
    elif sys.argv[1] == "-folder":
        preds = do_folder_pred(sys.argv[2], model, val_transforms, "")
        # store all preds in a txt file
        with open("predictions.txt", "w") as f:
            for pred in preds:
                f.write(f"{pred[0]}: {pred[1]}\n")
    else:
        print("Please provide a valid option: -single for single image prediction, -folder for folder prediction.")
        sys.exit(1)