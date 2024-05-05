# Embedded Mahjong Bot
Designed to work on **Raspberry Pi 4**. It is a bot player that detects Mahjong tiles and plays a tile each round.

Several aspects of our work include:
* training *Yolo-v9* models to achieve high accuracy on the classification of the Mahjong tiles shot on *Pi Camera*
* designing artifical intelligence algorithms that determine which Mahjong tile to play during each round of game with goal of maximizing winning probability
* building the physical bot station with a *movable robot arm*
* creating automation scripts that integrate all parts of the project

We render at the end a bot player that can play with three other human players and together hold a game of Mahjong.

### Usage
The following command automates of the process of taking a picture with Pi Camera and then generating detections of the Mahjong tiles in the picture. It is to be called from root directory.
```
python integrated/camera_onnx_infer.py -shoot -json
```
This command uses an `onnx` model exported from an instance of `Yolo-v9` model. We trained the yolo model ourselves.

### Resources:
* https://universe.roboflow.com/test01-8ymsa/4a41f234e48d49b5b335f25643ca0293

### Acknowledgements:
* https://github.com/WongKinYiu/yolov9
* https://github.com/danielsyahputra/yolov9-onnx