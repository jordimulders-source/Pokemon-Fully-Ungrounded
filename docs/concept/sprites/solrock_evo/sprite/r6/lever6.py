import numpy as np, sys; from PIL import Image, ImageDraw
sys.path.insert(0,'..'); from npy2png import save
from toon_gezicht import PAL, rgba, gezicht, modelgezicht
o=np.load('basis6.npy'); r5=np.load('../r5/sprite.npy')
save(o,'sprite.png',PAL+[(0,0,0)]*(16-len(PAL))); np.save('sprite.npy',o)
Z=np.zeros((64,64),bool); Z[21:47,14:37]=True
d=o!=r5; print('r6 vs r5: totaal',int(d.sum()),'| buiten gezichtszone:',int((d&~Z).sum()),'| kleuren',len(np.unique(o)))
print('lijnpixels in de plaat (P3/P4):',int(np.isin(o,[9,10])[Z].sum()),' r5:',int(np.isin(r5,[9,10])[Z].sum()))
L=(232,236,224,255); D=(40,44,64,255); S=11.87; X0=138-0.5*S; Y0=107-1.2*S
m=Image.open('../../referenties/model.png').convert('RGBA')
mod=m.crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((64,64),Image.LANCZOS)
W=512;pad=12; g5,g6,gm=gezicht(r5),gezicht(o),modelgezicht()
H=pad+14+g6.height+pad+14+W+pad+14+140
vel=Image.new('RGBA',(3*g6.width+4*pad+0,H),(255,255,255,255)); dr=ImageDraw.Draw(vel)
for k,(im,t) in enumerate([(g5,'gezicht r5 (16x)'),(g6,'gezicht r6 (16x)'),(gm,'gezicht model (zelfde schaal)')]):
    dr.text((pad+k*(g6.width+pad),pad),t,fill=(0,0,0)); vel.paste(im,(pad+k*(g6.width+pad),pad+14))
y=pad+14+g6.height+pad
for k,(im,t) in enumerate([(rgba(o,L).resize((W,W),Image.NEAREST),'r6 (8x)'),(mod.resize((W,W),Image.NEAREST),'model verkleind (8x)')]):
    dr.text((pad+k*(W+pad),y),t,fill=(0,0,0)); vel.paste(im,(pad+k*(W+pad),y+14))
y+=14+W+pad
dr.text((pad,y),'1x licht / donker / wit, en 2x',fill=(0,0,0))
for k,bg in enumerate([L,D,(255,255,255,255)]): vel.paste(rgba(o,bg),(pad+k*72,y+14))
vel.paste(rgba(o,L).resize((128,128),Image.NEAREST),(pad+3*72+20,y+14))
vel.save('vel.png'); print(vel.size)
