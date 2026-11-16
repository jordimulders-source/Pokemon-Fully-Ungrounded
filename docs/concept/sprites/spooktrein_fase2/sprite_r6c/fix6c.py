# r6c: banden in de flank 9 -> 13; plankentint 8 (114,86,65) -> (124,94,71) (helderheid 92 -> 100). Onderkant/omlijning blijven 9/1.
import numpy as np; from PIL import Image
src=Image.open('r6b.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r=o.copy()
FACE=np.zeros((64,64),bool); FACE[9:27,25:42]=True
FL=np.zeros((64,64),bool); FL[23:43,24:56]=True
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
def edge(y,x): return any(not fg(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
log=[]
for y,x in zip(*np.where(FL&~FACE&(r==9))):
    if not edge(y,x): o[y,x]=13; log.append((int(x),int(y)))
pal[8*3:8*3+3]=[124,94,71]
Image.fromarray(o.astype('uint8'),'P').putpalette(pal) if False else None
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
d=o!=r; print('banden 9->13:',len(log),'gezicht diff',int(d[FACE].sum()))
open('telling.txt','w').write('banden 9->13 (%d px): %s\npalet 8: (114,86,65)=92 -> (124,94,71)=100 (geen indexwijziging)\n'%(len(log),log))
L=np.array([0 if i==0 else 0.3*pal[3*i]+0.59*pal[3*i+1]+0.11*pal[3*i+2] for i in range(14)]); print('lum',L.round())
# waar staat 8 naast 10 / buiten de flank
print('8 buiten flank:',int(((o==8)&~FL).sum()),' waarvan y>=43:',int(((o==8)&~FL&(np.arange(64)[:,None]>=43)).sum()),' in gezichtsbox:',int(((o==8)&FACE).sum()))
adj=set()
for y,x in zip(*np.where(o==8)):
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        if fg(y+dy,x+dx) and o[y+dy,x+dx] in (10,13,9): adj.add(int(o[y+dy,x+dx]))
print('8 grenst aan',adj, ' 8 naast 10:',[(int(x),int(y)) for y,x in zip(*np.where(o==8)) if any(fg(y+a,x+b) and o[y+a,x+b]==10 for a,b in ((-1,0),(1,0),(0,-1),(0,1)))])
MG=np.load('../sprite_r6/modelstats.npy')[0]
z=np.zeros((64,64),bool); z[30:45,36:51]=True; z&=o>0; w=z&np.isin(o,(7,8,9,13))
print('rechterflank sprite %.0f model %.0f; hout/ijzer %.0f model %.0f'%(L[o][z].mean(),MG[z].mean(),L[o][w].mean(),MG[w].mean()))
