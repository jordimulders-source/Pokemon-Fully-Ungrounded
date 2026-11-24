# schaduwplan.py: r11 | licht/midden/schaduw-kaart r11 | kaart r10 | Gnomad | Gnomad-kaart, op 8x
import numpy as np; from PIL import Image, ImageDraw
from kaart import *
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
r11=Image.open('gnometrotter_rock.png'); r10=Image.open('../sprite_r10/gnometrotter_rock.png'); gd=Image.open(D+'gnomad/af/gnomad.png')
s=8; P=[(r11.convert('RGB'),'r11'),(beeld(niveaus_gnome(np.array(r11))),'r11: licht/midden/schaduw'),(beeld(niveaus_gnome(np.array(r10))),'r10: licht/midden/schaduw'),
   (gd.convert('RGB'),'Gnomad'),(beeld(niveaus_gnomad(np.array(gd))),'Gnomad: licht/midden/schaduw')]
W=Image.new('RGB',(len(P)*(64*s+12),64*s+40),(255,255,255)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate(P):
    W.paste(im.resize((64*s,64*s),0),(i*(64*s+12),30)); d.text((i*(64*s+12)+4,8),t,fill=(0,0,0))
d.text((4,64*s+30-12),'geel = licht/hooglicht   grijs = midden   blauw = schaduw   donker = lijn',fill=(0,0,0))
W.save('schaduwplan.png')
