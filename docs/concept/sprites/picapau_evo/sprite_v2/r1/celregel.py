# Celregel op het 1024-model voor een kleine zone (geen tekenen): per spritecel achtergrond als >=50% wit,
# zwart als >=35% zwart, anders de meerderheidsklasse (zonder wit/zwart). Codes zoals klassen.py.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int)
M=[(255,255,255),(14,10,8),(205,134,91),(191,110,63),(138,73,46),(243,233,201),(224,206,171),(200,179,141),(222,87,77),
   (180,168,164),(118,106,104),(70,60,56),(248,221,95),(213,186,91)]
P=np.array(M); S=15.36; OY,OX=5.12,4*5.12
def cel(x,y,bg=0.5,zw=0.35):
    b=a[int(OY+y*S):int(OY+(y+1)*S),int(OX+x*S):int(OX+(x+1)*S)].reshape(-1,3)
    k=((b[:,None]-P[None])**2).sum(2).argmin(1); c=np.bincount(k,minlength=14)/len(k)
    if c[0]>=bg: return 0
    if c[1]>=zw: return 1
    c=c.copy(); c[0]=0; c[1]=0; return int(c.argmax())
