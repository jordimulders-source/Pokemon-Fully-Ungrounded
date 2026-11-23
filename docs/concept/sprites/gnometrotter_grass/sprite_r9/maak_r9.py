# maak_r9.py: Gnometrotter Grass r9 = r8 + keuring_r8 R0, R2, R3 (R1 bewust niet: niet in Jordi's opdracht). Rest 0 px.
import os, numpy as np
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
bim=Image.open('../sprite_r8/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
WIJZ=[]
def zet(x,y,v,z):
    if O[y,x]!=v: WIJZ.append((z,x,y,O[y,x],v)); O[y,x]=v
# R0 neusboog sluiten (= Rock af)
zet(26,20,6,'R0 neus')
# R2 naad 2 als boog: x35 y22-23, x34 y24-26, x33 y27-30, x34 y31-32, x35 y33-35; 7|6-paar schuift mee (rij 27-32), vrij -> 8
NAAD={22:35,23:35,24:34,25:34,26:34,27:33,28:33,29:33,30:33,31:34,32:34,33:35,34:35,35:35}
for y,xn in NAAD.items():
    oud=[x for x in range(32,38) if B[y,x]==6][0]          # huidige naadkolom in de zone
    if oud==xn: continue
    had7 = B[y,oud-1]==7
    zet(xn,y,6,'R2 naad')
    if had7: zet(xn-1,y,7,'R2 naad')
    for x in range(xn+1,oud+1): zet(x,y,8,'R2 naad')
# R3 linkerdij licht op de bolling
for x,y in ((20,45),(21,45),(22,45),(20,46),(21,46)): zet(x,y,11,'R3 dij')
assert all(z.startswith(('R0','R2','R3')) for z,*_ in WIJZ)
with open('log_r9.txt','w') as f:
    for z,x,y,a,b in WIJZ: f.write('%s x=%d y=%d %d->%d\n'%(z,x,y,a,b))
tel={}
for z,*_ in WIJZ: tel[z]=tel.get(z,0)+1
print(tel,'totaal',len(WIJZ),'rest 0')
out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
r8=bim.convert('RGB').resize((512,512),Image.NEAREST); r9=out.convert('RGB').resize((512,512),Image.NEAREST)
W=Image.new('RGB',(1034,512),'white'); W.paste(r8,(0,0)); W.paste(r9,(522,0)); W.save('vel.png')
