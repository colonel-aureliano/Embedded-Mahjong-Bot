import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = Picamera2()
camera.resolution = (3264, 2448)
# camera.rotation = 180
camera_config=camera.create_preview_configuration()
camera.configure(camera_config)
camera.start()

def see_preview():
  # camera.start_preview(Preview.QTGL)
  sleep(5)
  camera.capture_file('/home/pi/Desktop/Embedded-Mahjong-Bot/camera/image.jpg')

def just_shoot(name):
  camera.capture_file(f'/home/pi/Desktop/Embedded-Mahjong-Bot/camera/{name}.jpg')

def GPIO23_callback(channel): 
  just_shoot("test")
  print('Button 23 pressed.')

GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300) 

try:
	print ("Waiting for falling edge on port 27" )
	GPIO.wait_for_edge(27, GPIO.FALLING) 
except KeyboardInterrupt:
	GPIO.cleanup()