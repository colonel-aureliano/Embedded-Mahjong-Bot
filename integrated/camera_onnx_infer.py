import sys
sys.path.append('..')
from tile_classifier.yolov9-onnx import main

def retreive_onnx():
  weights_path = 
  return detector = YOLOv9(model_path=weights_path,
                      class_mapping_path=classes_path,
                      original_size=(w, h),
                      score_threshold=args.score_threshold,
                      conf_thresold=args.conf_threshold,
                      iou_threshold=args.iou_threshold,
                      device=args.device)

if __name__ == "__main__":
# read command line arguments, if "-single" is present, parse second argument as image path and call do_single_image_pred
# else, if "-shoot" is present, call ../camera/shoot_on_button.py to generate image and call do_single_image_pred
    detector = retreive_onnx()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-single":
            pred = do_single_image_pred(sys.argv[2], detector)
            print(pred)
            # with open("predictions.txt", "w") as json_file:
            #     json.dump(pred, json_file, indent=4) 
        elif sys.argv[1] == "-shoot":
            from camera import shoot_on_button
            shoot_on_button.no_button_shoot("shot_image")
            pred = do_single_image_pred("shot_image.jpg", detector)
            print(pred)
            # with open("predictions.txt", "w") as json_file:
            #     json.dump(pred, json_file, indent=4)

    else:
        print("Please provide a valid option: -single for single image prediction.")
        sys.exit(1)