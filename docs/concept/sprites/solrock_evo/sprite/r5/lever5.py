import numpy as np, sys; from PIL import Image, ImageDraw
sys.path.insert(0,'..'); from npy2png import save
from toon_gezicht import PAL, rgba, gezicht, modelgezicht
o=np.load('schoon5.npy'); r4=np.load('../r4/sprite.npy'); kaal=np.load('../kaal.npy')
save(o,'sprite.png',PAL+[(0,0,0)]*(16-len(PAL))); np.save('sprite.npy',o)
ZONE=np.zeros((64,64),bool); ZONE[21:47,14:37]=True
d=o!=r4
print('r5 vs r4: totaal',int(d.sum()),'| buiten gezichtszone (x14-36,y21-46):',int((d&~ZONE).sum()),'| kleuren',len(np.unique(o)))
OOG=np.zeros_like(ZONE); OOG[28:37,16:24]=True; OOG[29:39,25:34]=True
print('ogen (2x-blokken) vs kale reductie:',int(((o!=kaal)&OOG).sum()),'van',int(OOG.sum()),'| plaat buiten ogen vs kaal:',int(((o!=kaal)&ZONE&~OOG).sum()))
L=(232,236,224,255); D=(40,44,64,255)
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
m=Image.open('../../referenties/model.png').convert('RGBA')
mod=m.crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((64,64),Image.LANCZOS)
ov=Image.open('/tmp/_ov.png') if False else None
import subprocess; subprocess.run(['python3','overlay.py','sprite.npy','overlay.png'],check=True)
ov=Image.open('overlay.png')
W=512;pad=12
g4,g5,gm=gezicht(r4),gezicht(o),modelgezicht()
H=pad+14+W+pad+14+g5.height+pad+14+140
vel=Image.new('RGBA',(3*W+4*pad,H),(255,255,255,255)); dr=ImageDraw.Draw(vel)
for k,(im,t) in enumerate([(rgba(o,L).resize((W,W),Image.NEAREST),'r5 (8x)'),(mod.resize((W,W),Image.NEAREST),'model verkleind (8x)'),(ov,'overlay: r5-contour (rood), zwart (blauw), lichte rand (oranje) over het model')]):
    dr.text((pad+k*(W+pad),pad),t,fill=(0,0,0)); vel.paste(im,(pad+k*(W+pad),pad+14))
y=pad+14+W+pad
for k,(im,t) in enumerate([(g4,'gezicht r4 (16x)'),(g5,'gezicht r5 (16x)'),(gm,'gezicht model (zelfde schaal)')]):
    dr.text((pad+k*(W+pad),y),t,fill=(0,0,0)); vel.paste(im,(pad+k*(W+pad),y+14))
y+=14+g5.height+pad
dr.text((pad,y),'1x licht / donker / wit, en 2x',fill=(0,0,0))
for k,bg in enumerate([L,D,(255,255,255,255)]): vel.paste(rgba(o,bg),(pad+k*72,y+14))
vel.paste(rgba(o,L).resize((128,128),Image.NEAREST),(pad+3*72+20,y+14))
vel.save('vel.png'); print(vel.size)
