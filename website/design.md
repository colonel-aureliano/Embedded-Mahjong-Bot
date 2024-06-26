## Design and Implementation

Our code comprises four primary modules: **tile_classifier**, **camera**, **player**, and **integrated**. The first module leverages Yolo-v9 for image classification. The camera module controls the Pi Camera. The player module contains algorithms that govern the moves of the bot player. The integrated module assembles previous three modules and collaborates with GPIO pins and the PiTFT to create an interactive bot player.

### Tile Classifier

We developed these modules sequentially, starting with the tile classifier. Our objective was to train an image recognition model capable of identifying the suit and type of Mahjong tiles from photos shot with Pi Camera. We experimented with several open-source models, including MobileNet-v2, Yolo-v7, and Yolo-v9, as well as pre-trained models from Roboflow. The latter does target Mahjong tiles, however, it achieves only approximately 70% accuracy. We would like to much higher accuracy because we want to avoid scenarios where the bot player mistakenly identifies a winning hand due to incorrect tile recognition.

Yolo-v9 emerged as the most accurate, achieving nearly 100% accuracy. However, it is important that we believe the quality and quantity of our training data proved more decisive to our success than the model's inherent capabilities. We had generated substantial training data by manually photographing and labeling Mahjong tiles, producing around 150 original images. Then, using data augmentation techniques, we automated the rotation and lighting adjustments of these photos, ultimately expanding our dataset to approximately 1000 images. The training process involves running for 100 epochs on an RTX 4090, which took about 25 minutes. We now have a highly effective model that can detect all 14 tiles at once from a photo. These 14 tiles are to be the ones on the tile rack facing the bot player.

### Pi Camera

Since the goal of the project is to shoot photos with Pi Camera, we utilized it directly to generate the training set. This ensures consistency in properties like resolution and light sensitivity. The camera module includes scripts to configure the Pi Camera. We employed the picamera2 library, which allows us to easily manipulate the Pi Camera to capture high-resolution images or to also display live image previews.

### Player Algorithm

The algorithm that governs the player's moves uses reinforcement learning and assigns reward to the successful completion of a triplet or a couplet. A triplet in Mahjong is a sequence of 3 tiles or identical 3 tiles. To win in Mahjong is to have 4 triplets and 1 couplet. The player strategizes based on its current 14 tiles which one it wishes to get rid of with the goal of maximizing its future reward. In other words, it wishes to throw away a tile that is least contributive to the forming of a triplet or a couplet. The transition probability is defined in terms of the probability of receiving a specific tile in the next round. For a tile $t$, since there are only 4 copies of any tile, this probability is 

$$\frac{4 - \text{copies of $t$ bot already hold}} {\text{total number of tiles remaining in the deck}}$$

Remaining tiles in the deck are the ones not held by any other player in the game nor have already been played by any player. Played tiles cannot be retrieved per the rules of Mahjong. Both copies of $t$ bot already hold and total number of tiles remaining in the deck are properties of a specific state $s$. That is, the state $s$ encodes the tiles the bot currently hold, all the tiles played by other players, and all tiles remaining to be drawn from the deck. Therefore effectively, the probability can be written as $P(t | s)$.

Then, to calculate the value of any state under a policy $\pi$ (the target parameter to train), we use the following formula:

$$ V^{\pi}(s) = r(s, \pi(s)) + \gamma * \sum_{t \in tiles} P(t | s) * V^{\pi}((s \setminus \pi(s)) \cup {t}) $$

The value of a state indicates the bot's current advantage. The goal is to transition towards more advantageous states. With this formulation, we can apply reinforcement learning training techniques, the details of which we will not discuss here. Ultimately, the training process produces a policy that is a function of the state.

### Integrated

The integrated module contains the following functions that bring together the software and hardware portions of this project:

* A script that automates the photo taking process, the passing of the photo to the inference model, and the generation of predicted results.
* A script that monitors and responds to user inputs on GPIO pins.
* A script that uses the PyGame library to control PiTFT displays and prompts users for inputs.
* A script that signals to servo degree of turn which matches the location of the tile the player decides to play.
  
The main script connects all these componenets together and produces the following procedure for each round of game:

1. Displays to user ready status on the PiTFT. Prompts user to indicate readiness through pressing a GPIO pin.
2. Once button is pressed, begin playing by:
   1. Taking a photo with the Pi Camera
   2. Infer the tiles in the photo by passing it to the tile classifier
   3. Decide on which tile to play through calling the player algorithm (also check if bot has won)
   4. Indicate with the servo and PiTFT display which tile it intends to play
3. Wait for user to confirm the result. Then move to next round of game.
   
## Testing

Testing is modularized as well. Each module needs to be tested in order to ensure it performs its intended function. 

* Tile classifier: We need to ensure the trained model can reach near perfect accuracy regardless of the physical surrounding. We test the model by the test set in the train-valid-test split we had performed while processing our training dataset. During training, the model is able to report near perfect accuracy on the test set in the last several epochs. Then, we experimented with the trained model ourselves. We had varied the surrounding from the surrounding used when generating the training data set. One important factor turns out to be lighting. The Pi Camera turns out to be very sensitive to light, but we want to make sure that in less ideal lighting, the model can also perform well. Therefore, upon testing the model with less ideal lighting, we discover that some errors are prone to be made on the peripheries of images. We then retrained the model with more such error-prone samples.
* Player: The player module is difficult to test in that we lack a well-defined intuition for what the right tile to play is. For a human, it takes a lot of experience with Mahjong to be able to determine whether a move is well-made or not. When the algorithm plays counter-intuitive to us, we cannot tell whether it was because of our limited ability at deduction or the algorithm's error. Therefore we resort to glass-box examining of its evaluation of the value of various states to see if the evaluation logically correspond with our formulation above. For example, it is fitting that a near-winning hand should have a much higher value than a starter hand, and that the algorithm should determine to play the non-contribuitng tile in the near-winning hand instead of a contributive one. It is also easy to compare among the few non-contributing tiles which one should lead to the greatest gains.
* Integrated: The components of this module have been each unit-tested. Each has been ran repeatedly on their own to make sure their behavior is as expected. The inference script supports different command line arguments that facilitate high-granularity testing. The hardware parts are each tested as well, including the GPIO pins and the PiTFT. We adjust the fonts and the coordinates of the prompts so that they appear at desired places and are significant to the user.

The principle of modularity is essential to the construction of our project. It allows incremental efforts and makes it easier to locate blame when something doesn't work as expected. It also allows us to divide up work amongst ourselves.