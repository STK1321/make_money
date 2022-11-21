import cv2
import glob
import subprocess
from argparse import Namespace
from apiclient import  http 
from gtts import gTTS 
from PIL import Image, ImageDraw, ImageFont

from Edit_Video import get_authenticated_service, initialize_upload

def animate_single_line(base_background_image, input_string, line_y_position, start_frame):
  fnt = ImageFont.truetype('arial.ttf', 25)
  input_string = '' + input_string
  for i in range(len(input_string)):
    
    d = ImageDraw.Draw(base_background_image)
    d.text((50,line_y_position), input_string[:i], font=fnt, fill=(255,255,255))
      
    base_background_image.save(f'./content_files/black_480p_{(i + start_frame):05}.png')
  return i + start_frame
def get_frame_list():
  img_list = []
  for filename in sorted(glob.glob('./content_files/*.png')):
    img = cv2.imread(filename)
    img_list.append(img)
  return img_list

def create_video_from_frames(frame_list, frame_size, filename):
  out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 15, frame_size)
  for i in range(len(frame_list)):
    frame_idx = i
    out.write(frame_list[frame_idx])

  out.release()

FRAME_SIZE = (720,480)
img_list = []


for filename in sorted(glob.glob('./content_files/*.png')):
    img = cv2.imread(filename)
    img_list.append(img)

alto,ancho=img.shape[:2]
out = cv2.VideoWriter("peubavideo1.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 15, (ancho,alto))
print(alto,ancho)
for i in range(len(img_list)):
    frame_idx = i
    out.write(img_list[frame_idx])

out.release()