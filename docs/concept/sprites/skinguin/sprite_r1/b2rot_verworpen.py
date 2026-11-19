# Variant B2 (r1b): verre ski draaien om de enkel op MODELresolutie, zodat hij evenwijdig aan de nabije ski komt
# (rechte verschuiving omlaag kan niet: 1 px omlaag raakt al de opgebogen punt van de nabije ski).
# Stappen: verre ski uitknippen in het 1024-model -> draaien om de enkel (NEAREST, dus alleen modelpixels) ->
# opnieuw door dezelfde pijplijn (natief raster, dezelfde geschrapte rijen/kolommen, kwant, bouw.py stap 1-3) ->
# alleen de verre poot+ski uit dat resultaat in A plakken. Gebruik: python3 b2rot.py HOEK_GRADEN [DY_px_model]
import sys, os, subprocess, numpy as np; from PIL import Image
TH=float(sys.argv[1]) if len(sys.argv)>1 else 10; DYM=float(sys.argv[2]) if len(sys.argv)>2 else 0
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
P=10.24; C0=5.13
mod=np.asarray(Image.open('../model/model.png').convert('RGB')).copy()
A=np.loadtxt('A.txt',dtype=int); m=np.load('poot_masker.npy'); wk,wr=np.load('weg.npy')
keepc=np.array([c for c in range(75) if c not in wk]); keepr=np.array([r for r in range(75) if r not in wr])
# verre poot+ski in het 1024-model zelf uitknippen: floodfill over niet-witte, niet-rode pixels vanaf de verre ski, onder de heup
mf=mod.astype(int); nietwit=mf.min(2)<238; rood=(mf[...,0]>140)&(mf[...,1]<110)
hr,hc=keepr[41]+16,keepc[24]+12; HY=int(C0+hr*P-P/2)          # bovenkant beenrij 41
sr,sc=keepr[51]+16,keepc[10]+12; seed=(int(C0+sr*P),int(C0+sc*P))
from collections import deque
M=np.zeros((1024,1024),bool); q=deque([seed])
while q:
    y,x=q.popleft()
    if 0<=y<1024 and 0<=x<1024 and not M[y,x] and nietwit[y,x] and not rood[y,x] and y>=HY:
        M[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
# randje anti-aliasing erbij (1 px dilatie binnen niet-wit)
M2=M.copy(); M2[1:]|=M[:-1]; M2[:-1]|=M[1:]; M2[:,1:]|=M[:,:-1]; M2[:,:-1]|=M[:,1:]; M=M2&(mf.min(2)<252)&~rood
piv=(C0+hc*P, HY)   # draaipunt = heup (bovenkant been), aansluiting aan de dij blijft
laag=np.zeros((1024,1024,4),'uint8'); laag[M,:3]=mod[M]; laag[M,3]=255
mod[M]=255
L=Image.fromarray(laag).rotate(-TH,resample=Image.NEAREST,center=piv)
if DYM>0:   # been rekken: alles onder de snede midden in het been DYM px omlaag, de band ertussen = de beenrij erboven herhaald (modelpixels)
    la=np.asarray(L).copy(); YC=int(C0+(keepr[43]+16)*P); d=int(round(DYM))
    nl=np.zeros_like(la); nl[:YC]=la[:YC]; nl[YC+d:]=la[YC:1024-d]
    for k in range(d): nl[YC+k]=la[YC-1]
    L=Image.fromarray(nl)
comp=Image.fromarray(mod).convert('RGBA'); comp.alpha_composite(L); comp=comp.convert('RGB')
comp.save('b2/model_b2.png')
# zelfde pijplijn
a=np.asarray(comp).astype(int); cs=np.arange(C0,1024,P)
out=np.zeros((100,100,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
b=out[16:91,12:87]; b=np.delete(np.delete(b,wk,axis=1),wr,axis=0)
Image.fromarray(b).save('b2/geschrapt.png')
for f in ('kwant.py','bouw.py'):
    subprocess.run(['python3',os.path.join(D,f)],cwd=os.path.join(D,'b2'),check=False,capture_output=True)
N=np.loadtxt('b2/A.txt',dtype=int)
rest=(A>0)&~m
B2=A.copy(); B2[m]=0
neem=(N>0)&~rest; neem[:41]=False
# alleen het verbonden stuk vanaf de verre poot (geen restjes elders)
from collections import deque
seen=np.zeros_like(neem); q=deque([(41,24)])
while q:
    y,x=q.popleft()
    if 0<=y<61 and 0<=x<61 and neem[y,x] and not seen[y,x]:
        seen[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1),(y+1,x+1),(y-1,x-1),(y+1,x-1),(y-1,x+1)])
B2[seen]=N[seen]
# been rekken als de ski omlaag ging: beenrijen 44-45 KS px omlaag, rij 43 herhaald (pixels uit A)
KS=0
if KS>0:
    leg=m.copy(); leg[:41]=False; leg[46:]=False
    for y in (45,44):
        for x in np.where(leg[y])[0]:
            if B2[y+KS,x]==0: B2[y+KS,x]=A[y,x]
            seen[y+KS,x]=True
    for k in range(KS):
        for x in np.where(leg[43])[0]:
            B2[44+k,x]=A[43,x]; seen[44+k,x]=True
far=seen
# raken? (Chebyshev-afstand tot de rest onder rij 44)
near=rest.copy(); near[:44]=False
fy,fx=np.where(far&(np.arange(61)[:,None]>=44)); ny,nx=np.where(near)
DD=np.maximum(np.abs(fy[:,None]-ny[None]),np.abs(fx[:,None]-nx[None]))
def gaten(F):
    g=[]
    for x in range(61):
        a=np.where(F[:,x])[0]; b=np.where(near[:,x])[0]
        if len(a) and len(b):
            bb=b[b>a.max()]
            if len(bb): g.append(int(bb.min()-a.max()-1))
    return g
mA=m.copy(); mA[:44]=False; gA=gaten(mA); fB=far.copy(); fB[:44]=False; gB=gaten(fB)
print('hoek',TH,'vrij',DD.min()-1,'A gaten',gA,'gem %.1f max %d'%(np.mean(gA),max(gA)),'| B2 gaten',gB,'gem %.1f max %d'%(np.mean(gB),max(gB)))
d=np.argwhere(B2!=A); buiten=[(y,x) for y,x in d if not (m[y,x] or far[y,x])]
print('diff A-B2',len(d),'buiten verre poot (oud+nieuw):',len(buiten),' rood in ski:',int(((B2>=2)&(B2<=5)&far).sum()))
np.savetxt('B2.txt',B2,fmt='%d')
