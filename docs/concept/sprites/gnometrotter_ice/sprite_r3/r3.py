# r3.py: keurderreparaties A1-A5 (keuring/KEURING.md) op sprite_r2/gnometrotter_ice_gatdicht.png.
# Alleen tint/lijn binnen het bestaande silhouet; elke pixel volgt de keuring + modelmeting (keuring/lum.py, kaart.py).
import sys, numpy as np
sys.path.insert(0,'../sprite'); from gemeen import lees, opslaan
C,D,E=12,13,14
o=lees('../sprite_r2/gnometrotter_ice_gatdicht.png'); r2=o.copy(); LOG={}
def zet(x,y,k,why,van=None):
    if van is not None and o[y,x] not in van: return
    if o[y,x]!=k: LOG.setdefault(why,[]).append((x,y)); o[y,x]=k
# A1 baardtinten uit het model (schaduw rechts, spleten x24/x29, x20 licht)
for y in range(26,36):
    for x in (26,27,28,30): zet(x,y,C,'A1 schaduwkant D->C',(D,))
for y in range(26,29): zet(25,y,C,'A1 x25 E->C',(E,))
for y in range(25,31): zet(29,y,C,'A1 x29 E->C',(E,))
for y in range(31,35): zet(29,y,3,'A1 x29 E->3 (spleet)',(E,))
for y in range(29,36): zet(24,y,3,'A1 x24 C->3 (spleet)',(C,))
for y in range(25,29): zet(24,y,D,'A1 x24 C->D (model 205-231)',(C,))
for y in range(27,33): zet(20,y,D,'A1 x20 C->D (geen spleet)',(C,))
# A2 roze notch -> ijsspleet
for y in (34,35): zet(20,y,3,'A2 notch 7->3',(7,))
# A3 pegel over de riem op de linkerdij (model r3: lichte streep x19-21, y42-46, donkere lijn rechts ervan)
IJS={(21,42):C,(19,43):D,(20,43):D,(21,43):C,(19,44):D,(20,44):D,(21,44):C,(19,45):D,(20,45):D,(21,45):C,(20,46):D}
def pegel(IJS,tag):
    for (x,y),k in IJS.items(): zet(x,y,k,tag+' ijs')
    for (x,y) in IJS:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            u,v=x+dx,y+dy
            if (u,v) in IJS or o[v,u]==0: continue
            if o[v,u] in (9,10,11): zet(u,v,2,tag+' rand 2 (ijs tegen blauw)')
pegel(IJS,'A3')
zet(19,47,9,'A3 los B-pixel onder de punt -> 9 (dijrand)',(11,))
# A4 stok linkerrand overal 2
for p in [(5,37),(5,41),(6,42),(6,49),(7,50)]: zet(*p,2,'A4 stok 1->2',(1,))
# A5 hand R rechter- en onderrand zwart
for p in [(61,37),(60,38),(60,39),(56,40),(57,40),(58,40),(59,40),(57,41),(58,41)]: zet(*p,1,'A5 hand R ->1')
opslaan(o,'gnometrotter_ice.png')
from PIL import Image
Image.open('gnometrotter_ice.png').convert('RGBA').resize((512,512),Image.NEAREST).save('gnometrotter_ice_8x.png')
print('anders t.o.v. r2 gatdicht:',(o!=r2).sum(),' silhouet-diff:',((o>0)!=(r2>0)).sum())
for k,v in LOG.items(): print('  %-40s %2d %s'%(k,len(v),v))
