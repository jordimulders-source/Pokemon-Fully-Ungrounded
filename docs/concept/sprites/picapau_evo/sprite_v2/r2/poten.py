# Poten uit het model: per cel achtergrond (wit>=50%), zwart (>=45%), anders toon op gemiddelde lum van de grijze modelpixels:
# >=110 licht, 85-110 midden, <85 donker. Verre poot (links, x<=23) een tint donkerder: licht->G, midden->G, donker->h;
# nabije poot: licht->g, midden->G, donker->h. -> poten(x,y) geeft code of None (buiten de poten)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int); Lm=a.mean(2); S=15.36; OY,OX=5.12,4*5.12
def poot(x,y,zw=0.45):
    b=Lm[int(OY+y*S):int(OY+(y+1)*S),int(OX+x*S):int(OX+(x+1)*S)].ravel()
    z=(b<60).mean(); w=(b>235).mean(); m=b[(b>=60)&(b<=235)]
    if w>=0.5: return 0
    if z>=zw or not len(m): return 1
    t=m.mean(); ver=x<=23
    if t>=110: return 10 if ver else 9
    if t>=85: return 10
    return 11
if __name__=='__main__':
    CH={0:'.',1:'#',9:'g',10:'G',11:'h'}
    for y in range(44,54): print('%2d '%y+''.join(CH[poot(x,y)] for x in range(17,32)))
