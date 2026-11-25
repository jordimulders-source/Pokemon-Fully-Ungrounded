from PIL import Image
import numpy as np
from collections import deque
import os
VAR=os.environ.get('VAR','130')   # r7: model met vergrote oogbollen (120 of 130)
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..',('model_bol%s.png'%VAR) if VAR!='100' else os.path.join('..','..','model','model_gekozen.png'))
K=float(VAR)/100
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
    BGF=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','model_bol%s_bg.npy'%VAR)
    if os.path.exists(BGF): bg=np.load(BGF)   # r7: achtergrond = alles buiten het object (originele achtergrond, niet afgedekt door een bol)
    return a,bg
