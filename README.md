# Embedded Mahjong Bot
![Station](website/images/station.jpg)

A bot player that detects Mahjong tiles and plays a tile each round. Designed to work on **Raspberry Pi 4** with a Pi Camera and a rack of Mahjong tiles facing it.

Several aspects of our work include:
* training Yolo-v9 models to achieve high accuracy on the classification of the Mahjong tiles shot on Pi Camera
* designing artifical intelligence algorithms that determine which Mahjong tile to play during each round of game with goal of maximizing winning probability
* building the physical bot station with a movable robot arm indicating which tile the bot intends to play in each round
* creating automation scripts that integrate all parts of the project 

We render at the end a bot player that can play with three other human players and together hold a game of Mahjong.

### Usage
It is recommended to consult `installation.txt` first for installation steps.

#### Main Usage
To run the bot player, call from root directory
```
sudo python integrated/main.py 
```
The possible command arguments are `cmd` to confine to command line interaction only, and `img` to output prediction image with confidence levels displayed.

#### Test Usages
1. The following command automates of the process of taking a picture with Pi Camera and then generating detections of the Mahjong tiles in the picture. It is to be called from root directory.
```
python integrated/camera_onnx_infer.py -shoot -json
```
This command uses an `onnx` model exported from an instance of `Yolo-v9` model. The model weights we trained are stored at `tile_classifier/onnx/weights/best-v4-800-half-fp32.onnx`.
`shoot` and `json` inform the script to immediately shoot using Pi Camera, do inference, and store the results to a json file. 
Other possible arguments in place of `shoot ` are `shoot-wait` which waits on an enter from command line to shoot the photo, and `single` which does not take new photo but instead reads existing photo and performs inference.

2. The following command runs the playing algorithm; it determines which tile to play given 14 tiles.
```
python player/test.py
```
Uncommenting some lines of code in the script will also test the hand parititioning algorithm. To partition a hand is to divide the 14 tiles into sequences, triplets, couplets, quadruplets, or singles. The playing algorithm uses the partition algorithm and performs scoring on each of the tiles based on it. The tile with least score is played.

3. The following command tests whether the PyGame library can successfully manipulate PiTFT display.
```
python integrated/tft_display.py
```
If unsuccessful, consider chaning the OS of the Pi. We used **Bullseye** 64-bit OS with PyGame version 1.9.6 and Python version 3.9.2. We were unable to make Bookworm OS work with PyGame version 2.5.2 adn Python version 3.11.2 to display to PiTFT.

4. The following command loads an ONNX model and performs inference on a source image.
```
cd tile_classifier/onnx
python main.py
```
See the script itself for required command line arguments.

### Resources
* https://universe.roboflow.com/test01-8ymsa/4a41f234e48d49b5b335f25643ca0293

### Acknowledgements
* https://github.com/WongKinYiu/yolov9
* https://github.com/danielsyahputra/yolov9-onnx
* https://github.com/JohnnyLiang1018/MahjongAI/tree/master/offline_mahjong
