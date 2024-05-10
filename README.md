# Embedded Mahjong Bot
A bot player that detects Mahjong tiles and plays a tile each round. Designed to work on **Raspberry Pi 4** with a Pi Camera and a rack of Mahjong tiles facing it.

Several aspects of our work include:
* training Yolo-v9 models to achieve high accuracy on the classification of the Mahjong tiles shot on Pi Camera
* designing artifical intelligence algorithms that determine which Mahjong tile to play during each round of game with goal of maximizing winning probability
* building the physical bot station with a movable robot arm indicating which tile the bot intends to play in each round
* creating automation scripts that integrate all parts of the project 

We render at the end a bot player that can play with three other human players and together hold a game of Mahjong.

### Usage
It is recommended to consult installation.txt first for installation steps.


#### Main Usage
To run the bot player, call from root directory
```
sudo python integrated/main.py 
```
The possible command arguments are `cmd` to confine to command line interaction only, and `img` to output prediction image with confidence levels displayed.

#### Test Usages
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
* https://github.com/JohnnyLiang1018/MahjongAI/tree/master/offline_mahjong