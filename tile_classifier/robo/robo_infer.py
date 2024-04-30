import json
import sys
from PIL import Image

def retreive_robo(model_at):
    sys.path.append(model_at)
    import robo # type: ignore
    return robo.model()

############################################

def predict_image(image_path, model):
    img = Image.open(image_path)
    return model(img)

def do_single_image_pred(image_path, model):    

    predicted_dict = predict_image(image_path, model)
    predicted_list = predicted_dict['predictions']

    # Load class_to_idx mapping from a JSON file
    with open(model_at+'idx_to_class.json', 'r') as json_file:
        class_mapping = json.load(json_file)
    
    # print(predicted_list)

    predicted_list.sort(key=lambda x: x.get("x"))

    return_list = []

    for i in range(len(predicted_list)):
        data = predicted_list[i]
        if ( i != 0 and data['x'] - predicted_list[i-1]['x'] < 40):
            continue

        data.pop("class_id", None)
        data.pop("detection_id", None)

        class_value = data["class"]
        data["class_name"] = class_mapping[class_value]

        return_list.append(data)
    
if __name__ == "__main__":
# read command line arguments, if "-single" is present, parse second argument as image path and call do_single_image_pred
    model_at = ""
    model = retreive_robo(model_at)
    if len(sys.argv) > 1:
        if sys.argv[1] == "-single":
            pred = do_single_image_pred(sys.argv[2], model)
            # print(pred)
            with open("predictions.txt", "w") as json_file:
                json.dump(pred, json_file, indent=4) 
        else:
            print("Please provide a valid option: -single for single image prediction.")
            sys.exit(1)