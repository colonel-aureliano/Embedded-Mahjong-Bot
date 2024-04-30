from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
camera.resolution = (3264, 2448)
# camera.rotation = 180

# camera.start_preview(alpha=200)
camera_config=camera.create_preview_configuration()
camera.configure(camera_config)

def see_preview():
  sleep(5)
  # camera.start_preview(Preview.QTGL)
  camera.capture_file('image.jpg')

def just_save_image(name):
  camera.capture_file(f'{name}.jpg')

camera.start()
just_save_image("test2")