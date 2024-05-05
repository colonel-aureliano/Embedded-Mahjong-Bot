import sys
import cv2
import json
import numpy as np

sys.path.append('')
from tile_classifier.onnx.yolov9 import YOLOv9
import time

def inferred_detections(detector, image_path):
    image = cv2.imread(image_path)

    begin = time.time()
    detections = detector.detect(image)
    end = time.time()
    elapsed = end - begin
    print(f"Time elapsed: {elapsed} seconds")

    return detections

def retreive_onnx():
    weights_path = "tile_classifier/onnx/weights/best_striped_V3_800_gelan-c.onnx"
    classes_path = "tile_classifier/onnx/weights/class_labels.yaml"
    h,w = 2464,3280
    # h,w = 80, 800
    score_threshold = 0.1
    conf_threshold = 0.4
    iou_threshold = 0.4
    device = "cpu"
    return YOLOv9(model_path=weights_path,
                      class_mapping_path=classes_path,
                      original_size=(w, h),
                      score_threshold=score_threshold,
                      conf_thresold=conf_threshold,
                      iou_threshold=iou_threshold,
                      device=device)

if __name__ == "__main__":
# read command line arguments, if "-single" is present, parse second argument as image path and call do_single_image_pred
# else, if "-shoot" is present, call ../camera/shoot_on_button.py to generate image and call do_single_image_pred
    detector = retreive_onnx()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-single":
            pred = inferred_detections(detector,"shot_image.jpg")
            # print(pred)
        elif sys.argv[1] == "-shoot":
            from camera import shoot_on_button
            shoot_on_button.no_button_shoot("shot_image")
            pred = inferred_detections(detector, "shot_image.jpg")
            # print(pred)
        else: 
            print("Please provide a valid option: -single for single image prediction, -shoot for take photo with Pi Camera then do prediction.")
            sys.exit(1)
        if len(sys.argv) > 2 and sys.argv[2] == '-json':
            for d in pred:
                for key, value in d.items():
                    if isinstance(value, np.ndarray):
                        d[key] = value.tolist()
                    elif isinstance(value, np.int64):
                        d[key] = int(value)
                    elif isinstance(value, np.float32):
                        d[key] = float(value)
            with open("predictions.json", "w") as json_file:
                json.dump(pred, json_file, indent=4)
    else:
        print("Please provide a valid option: -single for single image prediction, -shoot for take photo with Pi Camera then do prediction.")
        sys.exit(1)