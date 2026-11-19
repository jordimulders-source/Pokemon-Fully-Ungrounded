# Per spritecel het aandeel van elke modelklasse in de 1024-pixels (dichtstbijzijnde modelkleur), voor kleine zones.
# python3 frac.py x0 y0 x1 y1  -> per cel: top-2 klassen met % (z = zwart <60 lum)
import sys; import numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5])
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int)
M=[(255,255,255),(14,10,8),(205,134,91),(191,110,63),(138,73,46),(243,233,201),(224,206,171),(200,179,141),(222,87,77),
   (180,168,164),(118,106,104),(70,60,56),(248,221,95),(213,186,91)]
CH='.#lmdCckrgGhyY'; P=np.array(M); S=15.36; OY,OX=5.12,4*5.12
for y in range(y0,y1):
    out=[]
    for x in range(x0,x1):
        b=a[int(OY+y*S):int(OY+(y+1)*S),int(OX+x*S):int(OX+(x+1)*S)].reshape(-1,3)
        k=((b[:,None]-P[None])**2).sum(2).argmin(1); c=np.bincount(k,minlength=14)/len(k)
        t=np.argsort(-c)[:2]; out.append('%s%02d%s%02d'%(CH[t[0]],min(99,c[t[0]]*100),CH[t[1]],min(99,c[t[1]]*100)))
    print('%2d '%y+' '.join(out))
print('   '+' '.join('%-6d'%x for x in range(x0,x1)))
