
from PIL import Image, ImageDraw, ImageFont, ImageOps
from dataclasses import dataclass, field
from gtts import gTTS 
import subprocess
import cv2
import glob



RESURCES='./plantilla/'
DOWNLOADS='./content_files/'

@dataclass
class Edit:
    
  bacground:str
  resurces:str
  downloads:str
  nameout:str
  simple_background:str=field(init=False)
  logo:str=field(init=False)
  text_string:str
  font=ImageFont.truetype('arial.ttf', 60)
  imgsize:tuple=field(init=False)

  def __post_init__(self):
    self.simple_background=self.resurces+"fondo.png"
    self.logo=self.resurces+"CRIPTODEVKO.png"


  def backgrounEditImage(self):

    print('Proccess Image')
    background=Image.open(self.simple_background)
    ancho,alto=background.size
    #dibujo=ImageDraw.Draw(background)

    image=Image.open(self.downloads+self.bacground)
    resizeimg=ImageOps.contain(image,(ancho*3,alto*3),Image.Resampling.LANCZOS)
    
    hight,weight=image.size
    hight1,weight1=resizeimg.size
    #font=ImageFont.truetype('arial.ttf', 60)
    #str_news="Buena la rata como fue o que"
    
    #a,b,lenx,leny=dibujo.textbbox ((0,0),str_news,font=font)
    #anchof=lenx-a
    #altof=leny-b
    
    

    #ancho//2-hight//2,alto//2-weight//2
    print(hight,weight)
    print(hight1,weight1)
    if weight1>2200:
      background.paste(resizeimg,(-ancho,-alto//3))
      
    elif weight1>1800 and weight1<2200:
      background.paste(resizeimg,(-ancho,0))
      
    else:
      background.paste(resizeimg,(-ancho,alto//5))
      
    #paste the logo
    logo=Image.open((self.logo))
    background.paste(logo,(0,0),logo)
    #dibujo.text((552-anchof//2,952-altof//2),str_news,font=font,fill="white")
    #background.save(self.nameout)
    background.save(f'./media/{self.nameout}')
    
    print('--Done--')
    
  def edit_text(self):
    print('Proccess Text')
    imagen=Image.open(self.nameout)
    dibujo=ImageDraw.Draw(imagen)
    #font=ImageFont.truetype('arial.ttf', 60)
    #imagen.show()
    a,b,lenx,leny=dibujo.textbbox ((0,0),self.text_string,font=self.font)
    anchof=lenx-a
    altof=leny-b
    dibujo.text((552-anchof//2,952-altof//2),self.text_string,font=self.font,fill="white")
    imagen.save(self.nameout)
    print('--Done--')

  
  def break_fix(self,text:str, width:int, draw:object)->list:
    if not text:
        return
    lo = 0
    hi = len(text)
    #print(hi) 25 caracteres
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        #print(t)        
        #print(draw.textbbox((0,0), t,font=font))
        dimension = draw.textbbox((0,0),t, font=self.font)
        #print(t)
        w=dimension[2]-dimension[0]
        h=dimension[3]-dimension[1]
        if w <= width:
          #print(w,width)
          lo = mid
        else:
            hi = mid - 1

   
    t = text[:25]
    print(t)
    dimension = draw.textbbox((0,0),t, font=self.font)
    w=dimension[2]-dimension[0]
    h=dimension[3]-dimension[1]
    yield t, w, h
    yield from self.break_fix(text[lo:], width, draw)

  def fitText(self, color:str):      
      img=Image.open(f'./media/{self.nameout}')
      width = img.size[0] - 2
      font=ImageFont.truetype('arial.ttf', 20)
      print(width)
      draw = ImageDraw.Draw(img)
      pieces = list(self.break_fix(self.text_string,width, draw))
      height = sum(p[2] for p in pieces)
      if height > img.size[1]:
          raise ValueError("text doesn't fit")
      y = (img.size[1] - height) // 2
      for t, w, h in pieces:
          x = (img.size[0] - w) // 2
          draw.text((x, y), t, font=self.font, fill=color)
          y += h
      self.imgsize=img.size
      img.save(f'./media/{self.nameout[:-4]}.png')
      print('--Done--')

  def createAudio(self):
    audio_text = ''.join(self.text_string)
    myobj = gTTS(text=audio_text) 
    myobj.save(f'./media/{self.nameout[:-4]}.mp3') 
    print('--Audio Done--')
  
  def get_frame_list(self):
    img_list = []
    for filename in sorted(glob.glob('./media/*.png')):
      img = cv2.imread(filename)
      img_list.append(img)  
    return img_list

  def create_video_from_frames(self):
    frame_list=self.get_frame_list()    
    print(f'creando video con {self.imgsize}')
    out = cv2.VideoWriter(f'./media/{self.nameout[:-4]}.avi', cv2.VideoWriter_fourcc(*'XVID'), 15,self.imgsize)
    
    for i in range(len(frame_list)):
      
      frame_idx = i
      out.write(frame_list[frame_idx])
    
    out.release()

  def mux_audio_and_video(self):  
    cmd = f'ffmpeg -y -i ./media/{self.nameout[:-4]}.mp3  -r 30 -i ./media/{self.nameout[:-4]}.avi -filter:a aresample=async=1 -c:a flac -c:v copy {self.nameout[:-4]}.mp4'
    subprocess.call(cmd, shell=True)                           
    print('Muxing Done')

def main():
  imagen=Edit("si2.jpg",RESURCES,DOWNLOADS,"millosdavid.png","How can I get Money my br.")
  #imagen.backgrounEditImage()
  #imagen.edit_text()
  imagen.backgrounEditImage()
  #yellow RBG (255,255,0)
  imagen.fitText('white' )
  imagen.createAudio()
  imagen.create_video_from_frames()
  imagen.mux_audio_and_video()


if __name__=='__main__':
  main()
  
  