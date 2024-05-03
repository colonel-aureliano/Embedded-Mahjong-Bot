from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()

# camera.start_preview(alpha=200)
camera_config=camera.create_still_configuration()
camera.configure(camera_config)

def see_preview():
  sleep(5)
  # camera.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
  camera.capture_file('image.jpg')

def just_save_image(name):
  camera.capture_file(f'{name}.jpg')

camera.start()
just_save_image("camera_trial")