import cv2
import glob
import subprocess
from argparse import Namespace
from apiclient import  http 
from gtts import gTTS 
from PIL import Image, ImageDraw, ImageFont

from upload_video import get_authenticated_service, initialize_upload

def animate_single_line(base_background_image, input_string, line_y_position, start_frame):
  fnt = ImageFont.truetype('arial.ttf', 60)
  input_string = '' + input_string
  for i in range(len(input_string)):
    
    d = ImageDraw.Draw(base_background_image)
    d.text((50,line_y_position), input_string[:i], font=fnt, fill=(0,0,0))
      
    base_background_image.save(f'./content_files/black_1080p_{(i + start_frame):05}.png')
  return i + start_frame

def get_frame_list():
  img_list = []
  for filename in sorted(glob.glob('./content_files/*.png')):
    img = cv2.imread(filename)
    img_list.append(img)  
  return img_list

def create_video_from_frames(frame_list, frame_size, filename):
  print(f'creando video con {frame_size}')
  out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 15, frame_size)
  
  for i in range(len(frame_list)):
    
    frame_idx = i
    out.write(frame_list[frame_idx])
  
  out.release()

def create_audio(input_strings, filename):
  audio_text = ''.join(input_strings)
  myobj = gTTS(text=audio_text) 
  myobj.save(filename) 
  
def mux_audio_and_video(video_filename, audio_filename, output_filename):  
  cmd = f'ffmpeg -y -i {audio_filename}  -r 30 -i {video_filename} -filter:a aresample=async=1 -c:a flac -c:v copy {output_filename}'
  subprocess.call(cmd, shell=True)                           
  print('Muxing Done')

if __name__ == "__main__":
  
  LINE_HEIGHT = 35
  INPUT_STRINGS = [
    'Hello Soy Hubot! ', 
    'I create this video for you',
    '.', # This extra period adds a slight pause in the audio
    'Welcome to DevKingo Bot!'
    '                                                     '
    ]
  VIDEO_FILENAME = 'content_files/hello_world.avi'
  AUDIO_FILENAME = 'content_files/hello_world.mp3'
  OUTPUT_FILENAME = 'hello_world_video_and_audio.mkv'

  frame = 0
  
  #background_img = Image.new('RGB', FRAME_SIZE, color = 'black')
  background_img=Image.open("si.jpg")
  FRAME_SIZE = (1920,1080)
  #background_img.thumbnail(FRAME_SIZE)
  background_img.resize(FRAME_SIZE)
  background_img.save("si1.png")
  
  ancho,alto=background_img.size
  FRAME_SIZE = ( ancho,alto)

  print(f' ingreso  {ancho},{alto}')

  for string_idx, input_string in enumerate(INPUT_STRINGS):
    print(FRAME_SIZE[1]/2)
    line_y_position = FRAME_SIZE[1]/2 - LINE_HEIGHT * (0.5 + len(INPUT_STRINGS) / 2) + LINE_HEIGHT * string_idx
    frame = 1 + animate_single_line(background_img, input_string, line_y_position, frame)

  frame_list = get_frame_list()
  create_video_from_frames(frame_list, FRAME_SIZE, VIDEO_FILENAME)

  create_audio(INPUT_STRINGS, AUDIO_FILENAME)
  mux_audio_and_video(VIDEO_FILENAME, AUDIO_FILENAME, OUTPUT_FILENAME)


    