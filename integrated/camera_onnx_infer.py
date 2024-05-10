import sys
import cv2
import json
import numpy as np

sys.path.append('')
from tile_classifier.onnx.yolov9 import YOLOv9
import time

class Infer:


    def __init__(self):
        self.photo_path = "integrated/shot_image.jpg"
        self.predictions_path = "integrated/predictions.json"
        self.detector = self.retreive_onnx()

    def inferred_detections(self, detector, image_path, generate_image=False):
        image = cv2.imread(image_path)

        begin = time.time()
        detections = detector.detect(image)
        end = time.time()
        elapsed = end - begin
        print(f"Prediction time: {elapsed} seconds")
        
        if (generate_image):
            detector.draw_detections(image, detections=detections)
            # output_path = f"predicted_{image_path}"
            output_path = "predicted.jpg"
            if (cv2.imwrite(output_path, image)):
                print(f"Prediction image saved in predicted.jpg")
            else:
                print("Prediction image save unsuccessful")

        return detections

    def retreive_onnx(self):
        weights_path = "tile_classifier/onnx/weights/best-v4-800-half-fp32.onnx"
        classes_path = "tile_classifier/onnx/weights/class_labels.yaml"
        h,w = 2464,3280
        # h,w = 80, 800
        # score_threshold = 0.1
        conf_threshold = 0.4
        iou_threshold = 0.4   # intersection over union threshold
        device = "cpu"
        return YOLOv9(model_path=weights_path,
                        class_mapping_path=classes_path,
                        original_size=(w, h),
                        # score_threshold=score_threshold, # use default 0.1
                        conf_thresold=conf_threshold,
                        iou_threshold=iou_threshold,
                        device=device)

    def shoot_detect_to_json(self,predictions_path,generate_image = False):
        self.prediction_path = predictions_path
        self.run(["", "-shoot", "-json"], generate_image)

    def run(self,args,generate_image = False):
        if len(args) <= 1 or args[1] not in ["-single", "-shoot-wait", '-shoot']:
            print("Please provide a valid option: -single for single image prediction, -shoot for taking a photo with Pi Camera then do prediction, -shoot-wait for taking a photo with Pi Camera upon input then do prediction.")
            print("Add -json to store output.")
            sys.exit(1)

        if args[1] == "-single":
            pass
        elif args[1] == "-shoot-wait":
            from camera import shoot_on_button
            shoot_on_button.no_button_shoot(self.photo_path, True)
            print('Shot and saved at '+self.photo_path)
        elif args[1] == "-shoot":
            from camera import shoot_on_button
            shoot_on_button.no_button_shoot(self.photo_path, False)
            print('Shot and saved at '+self.photo_path)

        pred : list[dict] = self.inferred_detections(self.detector, self.photo_path, generate_image or len(args) > 2 and args[2] == '-generate-image')
        pred.sort(key=lambda d: d['box'][0])

        if len(args) > 2 and args[2] == '-json':
            for d in pred:
                for key, value in d.items():
                    if isinstance(value, np.ndarray):
                        d[key] = value.tolist()
                    elif isinstance(value, np.int64):
                        d[key] = int(value)
                    elif isinstance(value, np.intc):
                        d[key] = int(value)
                    elif isinstance(value, np.float32):
                        d[key] = float(value)
            with open(self.predictions_path, "w") as json_file:
                json.dump(pred, json_file, indent=4)
                print(f"Predictions stored at {self.predictions_path}")
        else:
            print(f"Found {len(pred)} tiles")
            for d in pred:
                print(d)

if __name__ == "__main__":
    infer = Infer()
    infer.run(sys.argv)