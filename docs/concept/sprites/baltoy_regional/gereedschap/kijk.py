# Proefvel: kale schrap-reducties 48/52/56 op 8x naast het model (box-verkleind tot dezelfde maat).
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'gereedschap'); import schrap as S
SCR='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/cc339c8a-c402-5a74-878a-f7e0da92c812/scratchpad/'
nat=Image.open('gereedschap/natief.png').convert('RGB').crop((15,13,83,83))
tiles=[]
for h in (48,52,56):
    kk,rr,*_=S.schrap(S.H-h,int(round(S.W-S.W*h/S.H)))
    im=Image.fromarray(rr.astype('uint8')); im=im.resize((im.width*8,im.height*8),Image.NEAREST)
    m=nat.resize((kk.shape[1],kk.shape[0]),Image.BOX).resize((kk.shape[1]*8,kk.shape[0]*8),Image.NEAREST)
    t=Image.new('RGB',(im.width*2+16,im.height),'white'); t.paste(im,(0,0)); t.paste(m,(im.width+16,0)); tiles.append(t)
W=max(t.width for t in tiles); Hh=sum(t.height+16 for t in tiles)
v=Image.new('RGB',(W,Hh),'white'); y=0
for t in tiles: v.paste(t,(0,y)); y+=t.height+16
v.save(SCR+'proef.png')
