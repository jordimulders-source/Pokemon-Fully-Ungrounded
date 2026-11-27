# vel r6: hoofd 12x: r6 | model (zelfde schaal, gezicht gelijk 1,28x, niet uitgerekt) | r4 v1 | modeluitsnede x330-640 y130-430; hele sprite 3x en 1x
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104); MY,MX=-21,-2
def rgb(o,bg=(255,255,255)): return Image.fromarray(np.array([[bg if v==0 else PAL3[v] for v in r] for r in o],np.uint8))
o=np.load('r6/pachamama_r6.npy'); r4=np.load('r4/pachamama_r4.npy')
y0,y1,x0,x1=10,32,18,40; S=12; W,H=(x1-x0)*S,(y1-y0)*S
mg=Image.open('r4/natief_g2.png').convert('RGB').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize((W,H),Image.LANCZOS)
uit=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB').crop((330,130,640,430)); uit=uit.resize((int(uit.width*H/uit.height),H),Image.LANCZOS)
K=[('r6',rgb(o[y0:y1,x0:x1]).resize((W,H),Image.NEAREST)),('model, zelfde schaal (gezicht 1,28x gelijk)',mg),('r4 v1',rgb(r4[y0:y1,x0:x1]).resize((W,H),Image.NEAREST)),('model uitsnede x330-640 y130-430',uit)]
tw=sum(im.width+8 for _,im in K); vel=Image.new('RGB',(max(tw,700),16+H+20+200),(235,235,235)); d=ImageDraw.Draw(vel); x=0
for t,im in K: vel.paste(im,(x,16)); d.text((x+3,2),t,fill=0); x+=im.width+8
y2=16+H+20; d.text((3,y2-14),'r6 hele sprite 3x en 1x',fill=0)
vel.paste(rgb(o).resize((192,192),Image.NEAREST),(0,y2))
for i,bg in enumerate(((255,255,255),(248,248,240),(40,40,48),(0,0,0))): vel.paste(rgb(o,bg),(210+i*72,y2+64))
vel.save('r6/vel.png'); print(vel.size)
