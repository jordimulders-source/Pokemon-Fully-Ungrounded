# r9: vanaf r8-naden; per schots twee aaneengesloten vlakken (licht/schaduw), grens = Otsu op het gladgestreken model
import sys; sys.path.insert(0,'r7w')
from zones import *
import p6
PAL=np.array(p6.PAL,float); LUM={c:PAL[I[c]].mean() for c in 'WLMD'}
o=np.load('r7w/r8.npy').copy()
body=np.load('r7w/body2.npy'); outer=np.load('r7w/outer2.npy'); P50=np.load('r7w/P50.npy')
eye=isin(R,'erCg')
seam=np.load('r7w/seam8.npy').copy()
for p in [(31,9),(30,10)]: seam[p]=False          # kruinnaad 2 px eerder laten stoppen
inter=body&~outer&~eye
fill=inter&~seam
# glad model: gemiddelde P50 over 3x3 binnen dezelfde vulling
G=np.zeros((64,64))
for j,i in zip(*np.where(fill)):
    v=[P50[j+dy,i+dx] for dy in (-1,0,1) for dx in (-1,0,1) if fill[j+dy,i+dx] and P50[j+dy,i+dx]>0]
    G[j,i]=np.mean(v)
voet=np.zeros((64,64),bool); voet[53:,:]=True
def toon(j,i):
    g=G[j,i]
    if voet[j,i]: return 'D' if g<155 else ('M' if g<205 else 'L')
    if g>=225: return 'W'
    if g>=205: return 'L'
    if g>=175: return 'M'
    return 'D'
for j,i in zip(*np.where(fill)): o[j,i]=I[toon(j,i)]
# eilandjes (<=3 px) opheffen: naar de meest voorkomende buurtoon in de vulling
for _ in range(4):
    done=np.zeros((64,64),bool); ch=0
    for j,i in zip(*np.where(fill)):
        if done[j,i]: continue
        reg=flood(o,[(j,i)],fill&(o==o[j,i])); done|=reg
        if reg.sum()<=3:
            nb=[o[y+dy,x+dx] for y,x in zip(*np.where(reg)) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if fill[y+dy,x+dx] and not reg[y+dy,x+dx]]
            if nb: o[reg]=max(set(nb),key=nb.count); ch+=1
    if not ch: break
info=[]
o[seam]=I['S']
for j,i in zip(*np.where(inter&~seam&isin(o,'SK'))): pass
for x in info: print(x)
np.save('r7w/r9.npy',o); np.save('r7w/seam9.npy',seam); p6.to_txt(o,'r9.txt')
im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in p6.PAL for v in c]
im.putpalette(pal+[0]*(768-len(pal))); im.save('r9.png',transparency=0)
r=Image.open('r9.png').convert('RGBA').resize((512,512),0); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r); bg.convert('RGB').save('r9_8x.png')
