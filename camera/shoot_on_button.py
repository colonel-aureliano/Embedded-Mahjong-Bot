import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = Picamera2()
camera_config=camera.create_still_configuration()
camera.configure(camera_config)
camera.start()

def see_preview():
  # camera.start_preview(Preview.QTGL)
  sleep(5)
  camera.capture_file('image.jpg')

filename = "test"

def just_shoot(name):
  camera.capture_file(f'{name}.jpg')

def GPIO23_callback(channel): 
  global filename
  just_shoot(filename)
  print('Button 23 pressed.')

GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300) 

def shoot_and_return(name):
  try:
    global filename
    filename = name
    print ("Press Button 27 to quit. Press Button 23 to take a photo." )
    GPIO.wait_for_edge(27, GPIO.FALLING) 
  except KeyboardInterrupt:
    GPIO.cleanup()

def no_button_shoot(name, wait):
  try:
    global filename
    filename = name
    if (wait): input("Press return to take photo.")
    just_shoot(filename)
    print('Shot and saved at '+filename+".jpg")
  except KeyboardInterrupt:
    GPIO.cleanup()