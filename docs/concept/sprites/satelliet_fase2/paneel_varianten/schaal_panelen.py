# Panelen kleiner t.o.v. het lijf (uniform, verhoudingen van het paneel blijven); lijf/oog/antennes = model.png pixel voor pixel.
# Nabij paneel (R) schaalt rond zijn linkerbovenhoek: de linkerrand blijft op dezelfde lijn (lijf blijft bedekt) en het staafje blijft op de hoek uitkomen.
# Ver paneel (L) schaalt rond een punt achter het lijf, zodat het achter het lijf blijft steken.
import sys
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
im=Image.open('model.png').convert('RGB'); a=np.array(im)
W=1024
def poly(pts,pad=0):
  m=Image.new('L',(W,W),0); ImageDraw.Draw(m).polygon(pts,fill=255)
  m=np.array(m)>0
  return ndimage.binary_dilation(m,iterations=pad) if pad else m
fig=a.mean(2)<245
PR=[(705,250),(978,203),(652,872),(404,768)]
PLfull=[(226,300),(390,262),(380,420),(178,674),(38,654)]
# linkercontour van het lijf (y -> x): links daarvan is ver paneel, rechts lijf
cy=np.array([250,286,330,400,450,500,550,600,650,700]); cx=np.array([300,302,292,285,268,262,268,290,330,400])
xx,yy=np.meshgrid(np.arange(W),np.arange(W))
left_of_body=xx<np.interp(yy,cy,cx)-2
mR=poly(PR,6)&fig
mL=poly(PLfull,6)&fig&left_of_body
anch={'R':(705,252),'L':(330,330)}
# oude buitenrand van het nabije paneel ruim weghalen, maar niet links van zijn linkerrand (daar zit het lijf)
lx=705+(yy-250)*(404-705)/(768-250)
rmR=poly(PR,16)&fig&(xx>lx-5)
rmL=poly(PLfull,16)&fig&left_of_body
body=fig&~mR&~mL&~rmR&~rmL
for f in [float(x) for x in sys.argv[1].split(',')]:
  can=Image.new('RGB',(W,W),'white')
  def put(k,m):
    ax,ay=anch[k]; n=int(round(W*f))
    can.paste(im.resize((n,n),Image.NEAREST),(int(round(ax-ax*f)),int(round(ay-ay*f))),Image.fromarray((m*255).astype('uint8')).resize((n,n),Image.NEAREST))
  put('L',poly(PLfull,6)&fig)   # hele ver paneel incl. stuk achter lijf; lijf komt erover
  can.paste(im,(0,0),Image.fromarray((body*255).astype('uint8')))
  put('R',mR)
  ca=np.array(can); fg=ca.mean(2)<245
  lb,n=ndimage.label(fg,structure=np.ones((3,3))); ss=ndimage.sum(fg,lb,range(1,n+1)); keep=int(np.argmax(ss))+1
  ca[(lb!=keep)&fg]=255
  can=Image.fromarray(ca)
  can.save(f'paneel_varianten/panelen_{round(f*100)}.png')
