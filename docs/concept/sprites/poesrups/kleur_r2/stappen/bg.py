# bg.py: achtergrondmasker van het model (wit, min(R,G,B)>=244, vulling vanaf de rand; zoals silhouet/sil.py)
import numpy as np, os
from PIL import Image
from collections import deque
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/'
_f=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bg.npy')
def masker():
    if os.path.exists(_f): return np.load(_f)
    c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(int)
    H,W=c.shape[:2]; wit=c.min(2)>=244; b=np.zeros((H,W),bool); q=deque()
    for x in range(W):
        for y in (0,H-1):
            if wit[y,x] and not b[y,x]: b[y,x]=1; q.append((y,x))
    for y in range(H):
        for x in (0,W-1):
            if wit[y,x] and not b[y,x]: b[y,x]=1; q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wit[yy,xx] and not b[yy,xx]: b[yy,xx]=1; q.append((yy,xx))
    np.save(_f,b); return b
