from PIL import Image
import numpy as np
from collections import deque
import os
VAR=os.environ.get('VAR','s16p13')
# r8: variant -> (voorste bol, zijbollen, paneelbreedte), factoren t.o.v. het originele model (r13b)
CFG={'100':(1.0,1.0,1.0),'120':(1.2,1.2,1.0),'130':(1.3,1.3,1.0),
     's16p13':(1.3,1.6,1.3),'s16p15':(1.3,1.6,1.5),'s18p13':(1.3,1.8,1.3),'s18p15':(1.3,1.8,1.5)}
# r9: variant 'r9' = s18p15 met eigen factoren voor de mastpanelen (t.o.v. r13b): PB x2,0 en PF x2,5, beide vanaf hun
#   linkerrand (anker v=0) verbreed; zo komt de verbreding naast de romp/buis uit (zichtbaar) en niet erachter.
CFG['r9']=(1.3,1.8,1.5)
KF,KS,KP=CFG[VAR]
KPK={'PA':KP,'PC':KP,'PD':KP,'PE':KP,'PB':2.0 if VAR=='r9' else KP,'PF':2.5 if VAR=='r9' else KP}
ANKER={'PA':0.5,'PE':0.5,'PF':0.0 if VAR=='r9' else 0.5,'PD':1.0,'PC':0.0,'PB':0.0}
_D=os.path.dirname(os.path.abspath(__file__))
M=os.path.join(_D,'..',('model_%s.png'%VAR)) if VAR not in ('100','120','130') else (os.path.join(_D,'..','..','..','model','model_gekozen.png') if VAR=='100' else os.path.join(_D,'..','..','r7','model_bol%s.png'%VAR))
def load():
    a=np.array(Image.open(M).convert('RGB')).astype(int)
    H,W,_=a.shape
    w=(a.min(2)>=245)
    bg=np.zeros((H,W),bool); q=deque()
    for y in range(H):
        for x in (0,W-1):
            if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
    for x in range(W):
        for y in (0,H-1):
            if w[y,x] and not bg[y,x]: bg[y,x]=1; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and w[yy,xx] and not bg[yy,xx]:
                bg[yy,xx]=1; q.append((yy,xx))
    BGF=os.path.join(_D,'..','model_%s_bg.npy'%VAR) if VAR not in ('100','120','130') else os.path.join(_D,'..','..','r7','model_bol%s_bg.npy'%VAR)
    if os.path.exists(BGF): bg=np.load(BGF)   # r7: achtergrond = alles buiten het object (originele achtergrond, niet afgedekt door een bol)
    return a,bg
