# vel_r1.png en diff_r1_8x.png
import sys,numpy as np; sys.path.insert(0,'maker'); from pal import PAL
from PIL import Image, ImageDraw
def rgba(R):
  a=np.zeros((64,64,4),'uint8')
  for y in range(64):
    for x in range(64):
      c=R[y][x]
      if c!='.': a[y,x]=(*PAL[c],255)
  return Image.fromarray(a)
def op(im,bg=(255,255,255)):
  b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
R=[l.rstrip('\n') for l in open('maker/raster_r1.txt')]
O=[l.rstrip('\n') for l in open('onderlaag56.txt')]
spr=rgba(R); ond=rgba(O)
m0=Image.open('r8_bol_r7.png').convert('RGB'); P=400; model=Image.new('RGB',(m0.width+2*P,m0.height+2*P),(255,255,255)); model.paste(m0,(P,P)); S=(973-144)/56
def mcrop(x0,y0,x1,y1,z):
  box=(P+144+(x0-4)*S,P+215+(y0-19)*S,P+144+(x1-4)*S,P+215+(y1-19)*S)
  return model.crop(tuple(int(round(v)) for v in box)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def oog(R,var):
  R=[list(r) for r in R]
  if var=='B':  # fase 1 (Surskit-kraaloog) pixel voor pixel: # w # / # # #
    for (x,y),c in {(11,45):'c',(12,45):'c',(10,46):'#',(11,46):'w',(12,46):'#',(10,47):'#',(11,47):'#',(12,47):'#'}.items(): R[y][x]=c
  if var=='C':  # modelvorm (P met lichtpunt): .# / #w / ##
    for (x,y),c in {(12,45):'#',(11,46):'#',(12,46):'w',(11,47):'#',(12,47):'#'}.items(): R[y][x]=c
  return [''.join(r) for r in R]
W=1700; H=1500; vel=Image.new('RGB',(W,H),(236,236,236)); d=ImageDraw.Draw(vel)
def lab(x,y,t): d.text((x,y),t,fill=(0,0,0))
lab(10,5,'r1 (8x)'); vel.paste(op(spr).resize((512,512),Image.NEAREST),(10,20))
lab(540,5,'model (8x, uitsnede op het 64-raster)'); vel.paste(mcrop(0,0,64,64,8),(540,20))
lab(1070,5,'onderlaag56 (8x)'); vel.paste(op(ond).resize((512,512),Image.NEAREST),(1070,20))
# close-ups 12x
y0=550
lab(10,y0,'bol 12x: model | r1'); vel.paste(mcrop(19,18,45,43,12),(10,y0+15)); vel.paste(op(spr.crop((19,18,45,43))).resize((312,300),Image.NEAREST),(330,y0+15))
lab(670,y0,'kop 12x: model | r1'); vel.paste(mcrop(3,35,25,58,12),(670,y0+15)); vel.paste(op(spr.crop((3,35,25,58))).resize((264,276),Image.NEAREST),(944,y0+15))
# oogvarianten
y1=880; lab(10,y1,'oog A (r1, onderlaag) | B (fase 1, Surskit-kraaloog) | C (modelvorm met lichtpunt): kop 12x en 1x')
for i,v in enumerate('ABC'):
  im=rgba(oog(R,v)); vel.paste(op(im.crop((3,40,22,54))).resize((228,168),Image.NEAREST),(10+i*330,y1+15)); lab(10+i*330,y1+185,v)
  vel.paste(op(im),(240+i*330,y1+15)); vel.paste(op(im,(40,40,48)),(240+i*330,y1+85))
# 1x licht/donker
y2=1100; lab(10,y2,'1x op licht en donker, 2x')
vel.paste(op(spr),(10,y2+15)); vel.paste(op(spr,(40,40,48)),(84,y2+15)); vel.paste(op(spr).resize((128,128),Image.NEAREST),(160,y2+15)); vel.paste(op(spr,(40,40,48)).resize((128,128),Image.NEAREST),(300,y2+15))
m1=Image.open('meet/model_1x.png').convert('RGB'); lab(440,y2,'model 1x (oud vierkant silhouet)'); vel.paste(m1,(440,y2+15))
vel.save('maker/vel_r1.png')
# diffkaart
D=op(spr).copy(); px=D.load()
for y in range(64):
  for x in range(64):
    if R[y][x]!=O[y][x]: px[x,y]=(230,30,30)
o=Image.new('RGB',(3*512+40,530),(255,255,255)); dd=ImageDraw.Draw(o)
for i,(t,im) in enumerate((('onderlaag56',op(ond)),('r1',op(spr)),('gewijzigd (rood)',D))):
  o.paste(im.resize((512,512),Image.NEAREST),(i*532,18)); dd.text((i*532,2),t,fill=(0,0,0))
o.save('maker/diff_r1_8x.png')
for v in 'BC': open(f'maker/raster_r1_oog{v}.txt','w').write('\n'.join(oog(R,v))+'\n')
