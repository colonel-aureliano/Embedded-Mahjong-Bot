import csv
import os
import shutil
import random

# This script groups the images into folders based on their labels, then moves a percentage of the images to a validation directory.
# Some important variables to set:
# - train_grouped_dir: The name of the directory where the grouped training images will be stored.
# - val_grouped_dir: The name of the directory where the grouped validation images will be stored.
# - data_dir: The path to the data directory containing the images and the CSV file.
# - val_percentage: The percentage of images to move to the validation directory.

do_group = True
do_split = True
train_grouped_dir = "train_grouped"
val_grouped_dir = "val_grouped"

# Set the path to the data directory
data_dir_parent = "/Users/Yanny/Documents/Cornell/2023-2024/Spring 2024/ECE 5725/embedded-mahjong-bot/tile_classifier/data/"
data_dir = data_dir_parent + "Apr26shot"

if do_group:
  try: 
    shutil.rmtree(train_grouped_dir)
    shutil.rmtree(val_grouped_dir)
  except FileNotFoundError:
    pass

  def group(csv_file, image_dir, target_dir):
    # Create the train directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    count = 0
    with open(csv_file, "r") as file:
      reader = csv.DictReader(file)
      for row in reader:
        label = row["class"]
        image_name = row["filename"]
        image_path = os.path.join(image_dir, f"{image_name}")
        train_label_dir = os.path.join(target_dir, label)

        # Create the label directory if it doesn't exist
        os.makedirs(train_label_dir, exist_ok=True)

        # Copy the image file to the train directory
        shutil.copy(image_path, train_label_dir)

  group(data_dir+"/data.csv", data_dir+"/output", train_grouped_dir)

############################################

if do_split:
  val_percentage = 0.2

  # Create the validation directory if it doesn't exist
  os.makedirs(val_grouped_dir, exist_ok=True)

  # Get the list of JPG files in the grouped data directory
  files_path = train_grouped_dir

  # Get the list of folders in the files path
  folders = [folder for folder in os.listdir(files_path) if os.path.isdir(os.path.join(files_path, folder))]

  # Iterate over each folder
  for folder in folders:
    folder_path = os.path.join(files_path, folder)
    # Get the list of JPG files in the folder
    jpg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]
    # Shuffle the list of JPG files
    random.shuffle(jpg_files)
    # Calculate the number of files to move to the validation directory
    num_files = len(jpg_files)
    num_val_files = max(1,int(num_files * val_percentage))
    
    # Move the files to the validation directory
    for file in jpg_files[:num_val_files]:
      src = os.path.join(folder_path, file)
      os.makedirs(os.path.join(val_grouped_dir, folder), exist_ok=True)
      dst = os.path.join(val_grouped_dir, folder, file)
      shutil.move(src, dst)
    
    print(f"{num_val_files} files moved to the validation directory for folder {folder}.")

