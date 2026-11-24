# hybride_r2.py: B opnieuw uit de gerepareerde A (../sprite_r3) + keurderpunten B1-B6 (keuring/KEURING.md).
import sys, numpy as np; from scipy import ndimage as nd
sys.path.insert(0,'../sprite'); from gemeen import lees, opslaan
C,D,E=12,13,14
A2=lees('../sprite_r2/gnometrotter_ice_gatdicht.png'); A3=lees('../sprite_r3/gnometrotter_ice.png')
B0=lees('../sprite_hybride/gnometrotter_ice_hybride_gatdicht.png'); o=B0.copy()
DE=np.load('../sprite_r2/deel_r2.npy'); LIJF=np.isin(DE,[2,3,4,5,6,7,8,10,11,12,13,20])
LOG={}
def zet(x,y,k,why,van=None):
    if van is not None and o[y,x] not in van: return
    if o[y,x]!=k: LOG.setdefault(why,[]).append((x,y)); o[y,x]=k
# 0. alles buiten het lijf = A r3; B1 de 9 overschreven baardpixels = A r3
for y,x in zip(*np.where(~LIJF)): zet(x,y,A3[y,x],'buiten lijf = A r3')
for p in [(31,29),(31,30),(31,31),(31,32),(29,32),(30,33),(27,35),(27,36),(26,36)]: zet(*p,A3[p[1],p[0]],'B1 baardrand terug')
# B2: A1/A2/A4/A5 die binnen LIJF vallen ook overnemen (baard, stok, hand R; niet de dij)
for y,x in zip(*np.where((A3!=A2)&LIJF)):
    if y>=42 and 17<=x<=23: continue      # A3-pegel: hybride versie hieronder
    zet(x,y,A3[y,x],'B2 = A-reparatie in lijfmasker')
# B2/A3 hybride: pegel smaller (model_hybride: wit x20-21, y44-45, lichte streep vanaf (21,42))
IJS={(21,42):C,(21,43):D,(20,44):D,(21,44):C,(20,45):D,(21,45):C}
for (x,y),k in IJS.items(): zet(x,y,k,'B2 pegel ijs')
for (x,y) in IJS:
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        u,v=x+dx,y+dy
        if (u,v) in IJS or o[v,u]==0: continue
        if o[v,u] in (9,10,11): zet(u,v,2,'B2 pegel rand 2 (ijs tegen blauw)')
# B3 arm L zonder dambord: per rij een tint zoals A (bovenrij 6, midden 8, onderrij 7)
for y in range(31,34):
    for x in range(13,18): zet(x,y,A3[y,x],'B3 arm L = A')
# B4 rechterdij onderaan naar de modeltint
for x in range(41,45): zet(x,48,11,'B4 9->B',(9,))
for x in (47,48): zet(x,48,10,'B4 9->A',(9,))
for x in range(45,49): zet(x,49,10,'B4 9->A',(9,))
# B5 linkerdij
for x in range(21,25): zet(x,47,10,'B5 9->A',(9,))
def meerderheid(x,y,why,uit=(0,1,2,6)):
    t=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dx or dy) and o[y+dy,x+dx] not in uit and o[y+dy,x+dx]!=o[y,x]]
    if t: zet(x,y,np.bincount(t).argmax(),why)
for p in [(25,44),(26,45),(25,46),(20,47)]: meerderheid(*p,'B5 losse pixel dij')
# B6 vlekjes in het lijf
for p in [(48,25),(49,26),(48,27),(40,26),(41,27),(40,25),(33,21)]: meerderheid(*p,'B6 vlekje lijf',uit=(0,1,2,6,9))
# (54,30) 8 staat los tussen 6; het model heeft op (53,30) geen naad (helderheid 183 = 8) -> (53,30) 8, dan hoort (54,30) bij het 8-facet
zet(53,30,8,'B6 (54,30) in facet: (53,30) 6->8 (model 183)',(6,))
# B5/B6 algemeen: vlakvlekjes < 3 px (tinten 7,8,F / 9,A,B) binnen lijf en dijen opnemen; lijnen 1/2/6 en randpixels blijven
fg=o>0; OUT=fg&~nd.binary_erosion(fg)
VLAK=np.isin(DE,[2,3,4,5,6,10,11,12,13])   # lijf + dijen; arm L (7), hand R (8) en voeten (20) blijven als in A/oud
for it in range(3):
    for grp in ((7,8,15),(10,11)):
        for k in grp:
            lb,n=nd.label((o==k)&VLAK&~OUT)
            for j in range(1,n+1):
                mm=lb==j
                if mm.sum()>=3: continue
                rr=nd.binary_dilation(mm)&~mm&VLAK; t=o[rr]; t=t[np.isin(t,grp)&(t!=k)]
                if len(t):
                    for y,x in zip(*np.where(mm)): zet(x,y,np.bincount(t).argmax(),'vlekje <3 px')
opslaan(o,'gnometrotter_ice_hybride.png')
from PIL import Image
Image.open('gnometrotter_ice_hybride.png').convert('RGBA').resize((512,512),Image.NEAREST).save('gnometrotter_ice_hybride_8x.png')
print('anders t.o.v. B oud:',(o!=B0).sum(),' silhouet-diff:',((o>0)!=(B0>0)).sum(),' buiten lijf anders dan A r3:',((o!=A3)&~LIJF).sum())
print('baard-bbox (16-31,22-41) anders dan A r3:',(o[22:42,16:32]!=A3[22:42,16:32]).sum())
for k,v in LOG.items(): print('  %-38s %3d %s'%(k,len(v),v if len(v)<14 else ''))
