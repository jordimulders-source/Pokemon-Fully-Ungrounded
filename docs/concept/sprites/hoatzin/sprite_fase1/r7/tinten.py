# Ronde 7 (Jordi: "moet ipv die zwarte omlijning niet gewoon de schaduwtinten van de ledematen anders?"):
# binnen het silhouet geen lijn meer tussen vleugel, lijf en poot; scheiding met schaduwtinten. Vanaf r6.
import numpy as np
from PIL import Image
im=Image.open('../r6/kuiken_r6.png'); a=np.array(im); r6=a.copy(); W=np.load('../r6/vleugel.npy')
pal=im.getpalette()
EXTRA=13; pal[EXTRA*3:EXTRA*3+3]=[24,26,32]          # 1 extra tint: schaduw van het donkerste dons (2)
VL=(10,9,8,5)                                        # vleugeltinten licht -> donker
SCHADUW={4:3,3:2,2:EXTRA,6:2,7:6,          # dons/geel een stap donkerder
         10:9,9:8,8:5,5:12,12:12}         # poot/grijs een stap donkerder
N4=((-1,0),(1,0),(0,-1),(0,1))
def tr(y,x): return not (0<=y<64 and 0<=x<64) or a[y,x]==0
n={}
def zet(y,x,v,k):
    if out[y,x]!=v: out[y,x]=v; n[k]=n.get(k,0)+1
out=a.copy()
# (2) vleugelrand binnen het silhouet: geen lijn maar vleugeltint; lichtkant licht, schaduwkant donkerste vleugeltint
for y,x in zip(*np.nonzero(W)):
    buiten=[(dy,dx) for dy,dx in N4 if not W[y+dy,x+dx]]
    if not buiten or any(tr(y+dy,x+dx) for dy,dx in buiten): continue      # binnenpixel of silhouetrand: blijft
    schaduw=any(d in ((1,0),(0,1)) for d in buiten)
    zet(y,x,5 if schaduw else 10,'2 vleugelrand')
# veerlijnen binnen de vleugel in een vleugeltint
for y,x in zip(*np.nonzero(W)):
    if a[y,x]==12 and out[y,x]==12 and all(W[y+dy,x+dx] for dy,dx in N4): zet(y,x,5,'veerlijn -> vleugeltint')
# (1)+(3) slagschaduw: lijf/poot direct langs de vleugelrand een stap donkerder; zwarte binnenpixels daar -> schaduwtint van hun deel
for y in range(64):
    for x in range(64):
        if W[y,x] or a[y,x]==0 or (any(tr(y+dy,x+dx) for dy,dx in N4) and a[y,x] not in (5,8,9,10)): continue
        grijs=a[y,x] in (5,8,9,10)
        if not (W[y-1,x] or W[y,x-1] or (grijs and any(W[y+dy,x+dx] for dy,dx in N4))): continue
        # lijf: alleen aan de schaduwkant (vleugel boven/links, licht linksboven); poot (grijs) ligt achter de vleugel: aan elke kant
        v=a[y,x]
        if v==1:   # oude lijn: tint van het deel eronder bepalen uit de buren buiten de vleugel
            nb=[a[y+dy,x+dx] for dy,dx in N4 if not W[y+dy,x+dx] and a[y+dy,x+dx] not in (0,1)]
            base=max(set(nb),key=nb.count) if nb else 2
            zet(y,x,SCHADUW.get(int(base),base),'1 lijn -> schaduwtint')
        else: zet(y,x,SCHADUW.get(int(v),v),'1 slagschaduw')
# (3) poot onder de onderpunt: een stap donkerder dan de vleugelpunt (5) -> 12
for x,y in ((36,52),(38,52)): zet(y,x,12,'3 poot onder onderpunt')
assert ((out>0)!=(r6>0)).sum()==0
o=Image.fromarray(out,'P'); o.putpalette(pal); o.save('kuiken_r7.png',transparency=0)
print(n,'totaal',int((out!=r6).sum()),'zwart %',round((out==1).sum()/(out>0).sum()*100,1),'kleuren',sorted(set(out.flatten())-{0}))
