from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (3264, 2448)
# camera.rotation = 180

# camera.start_preview(alpha=200)

def see_preview():
  camera.start_preview()
  sleep(5)
  camera.capture('/home/pi/Desktop/Embedded-Mahjong-Bot/camera/image.jpg')
  camera.stop_preview()

def just_save_image(n):
  for i in range(n):
    camera.capture(f'/home/pi/Desktop/Embedded-Mahjong-Bot/camera/image{i}.jpg')

just_save_image(1)