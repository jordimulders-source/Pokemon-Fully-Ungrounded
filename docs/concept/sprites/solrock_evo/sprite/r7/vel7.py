import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../r6'); from toon_gezicht import PAL, rgba, gezicht, modelgezicht, S, X0, Y0
o=np.load('sprite.npy'); r6=np.load('../r6/sprite.npy')
L=(232,236,224,255); D=(40,44,64,255)
m=Image.open('../../referenties/model.png').convert('RGBA')
mod=m.crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((64,64),Image.LANCZOS)
W=512;pad=12; g6,g7,gm=gezicht(r6),gezicht(o),modelgezicht()
H=pad+14+g7.height+pad+14+W+pad+14+140
vel=Image.new('RGBA',(3*g7.width+4*pad,H),(255,255,255,255)); dr=ImageDraw.Draw(vel)
for k,(im,t) in enumerate([(g6,'gezicht r6 (16x)'),(g7,'gezicht r7 (16x)'),(gm,'gezicht model (zelfde schaal)')]):
    dr.text((pad+k*(g7.width+pad),pad),t,fill=(0,0,0)); vel.paste(im,(pad+k*(g7.width+pad),pad+14))
y=pad+14+g7.height+pad
for k,(im,t) in enumerate([(rgba(o,L).resize((W,W),Image.NEAREST),'r7 (8x)'),(mod.resize((W,W),Image.NEAREST),'model verkleind (8x)')]):
    dr.text((pad+k*(W+pad),y),t,fill=(0,0,0)); vel.paste(im,(pad+k*(W+pad),y+14))
y+=14+W+pad
dr.text((pad,y),'1x licht / donker / wit, en 2x',fill=(0,0,0))
for k,bg in enumerate([L,D,(255,255,255,255)]): vel.paste(rgba(o,bg),(pad+k*72,y+14))
vel.paste(rgba(o,L).resize((128,128),Image.NEAREST),(pad+3*72+20,y+14))
vel.save('vel.png'); print(vel.size)
