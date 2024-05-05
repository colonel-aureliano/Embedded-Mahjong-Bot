from picamera2 import Picamera2, Preview
from time import sleep
import os
import sys

def see_preview():
    sleep(5)
    # camera.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1))
    camera.capture_file('image.jpg')

def just_save_image(name):
    camera.capture_file(f'{name}.jpg')

def cvt_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0

def find_available_index(base_name, extension='jpg', path='.', start_index=0):
    index = start_index
    while True:
        file_name = f'{base_name}_{index}.{extension}'
        if not os.path.exists(file_name):
            return index
        index += 1


if __name__ == "__main__":
    camera = Picamera2()

    # camera.start_preview(alpha=200)
    camera_config=camera.create_still_configuration()
    camera.configure(camera_config)
    photo_name = 'mahjong'
    next_index = 0
    camera.start()

    while True:
        if (len(sys.argv) > 1 and sys.argv[1] != 'single'): total = cvt_int(input())
        else: total = 1
        if (total == 0):
            print('photo taking ends')
            break
        for i in range(0,total):
            next_index = find_available_index(photo_name,start_index=next_index)
            file_name = photo_name + '_' + str(next_index)
            just_save_image(file_name)
            next_index += 1
        print(f'taking {total} images done')
        

