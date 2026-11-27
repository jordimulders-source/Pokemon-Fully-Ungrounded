# Stap 1: natief raster (fase1_maat/natief.png = model r4 op zijn Gemini-raster, 70x77) met alleen Jordi's wijzigingen (27 nov):
#  A. rugharen weg; B. haren rond beide vleugels weg (nieuwe haren komen pas in de sprite, zie bouw.py);
#  C. omcirkelde wig in de nabije vleugel = lijf ("onder de vleugel is het lichaam");
#  D. omcirkeld strookje tussen rechterpoot en vleugel = poot ("gewoon de poot doortrekken").
import numpy as np
from PIL import Image
from scipy import ndimage as nd
nat=np.array(Image.open('../../fase1_maat/natief.png')).astype(int)
m=nat[...,3]>0
L=nat[...,:3].mean(2)
# --- rode omcirkeling van Jordi naar het natieve raster
s=np.array(Image.open('../jordi_omcirkeld.png').convert('RGB')).astype(int)
red=(s[...,0]>180)&(s[...,1]<80)&(s[...,2]<80)
fig=(s.sum(2)<600)&~red; ys,xs=np.nonzero(fig)
mo=np.array(Image.open('../../model/fase1_model.png').convert('RGB')).astype(int)
f2=mo.sum(2)<600; ys2,xs2=np.nonzero(f2)
ry,rx=np.nonzero(red)
nx=((rx-xs.min())/(xs.max()-xs.min()+1)*70).astype(int); ny=((ry-ys.min())/(ys.max()-ys.min()+1)*77).astype(int)
R=np.zeros(m.shape,bool); R[ny,nx]=1
lab,n=nd.label(nd.binary_dilation(R)); 
polys=[]
for i in range(1,n+1):
    p=nd.binary_fill_holes(nd.binary_dilation(lab==i))
    polys.append(p)
polys.sort(key=lambda p: np.nonzero(p)[0].mean())
wig,strook=polys[0],polys[1]
out=nat.copy()
body=np.median(nat[m&(L>28)&(L<50)][:, :3],0).astype(int)
print('lijftint',body)
# C: wig -> lijf (per pixel vastgelegd, natief (x,y)); omlijning onder de bovenarm en links van de onderarm blijft.
B=[(33,32),(34,32)]  # omlijning onder de bovenarm loopt door
LIJF=[(35,32),(36,32),(37,32),(34,33),(35,33),(34,34),(35,34),(36,34),(37,34),(40,34),
      (35,35),(36,35),(37,35),(38,35),(39,35),(40,35),(37,36),(38,36),(39,36),(40,36)]
for x,y in B: out[y,x,:3]=[2,2,2]
for x,y in LIJF: out[y,x,:3]=body
nC=(np.abs(out-nat).sum(2)>0).sum()
# D: strookje -> poot doorgetrokken: binnen de rode lus (zonder verdikking) poottint, buitenrand zwart;
#    zwarte binnenlijnen tussen strookje en poot verdwijnen (een poot).
strook=nd.binary_fill_holes(R & (np.arange(77)[:,None]>=44))
legc=np.median(nat[60:63,45:47,:3].reshape(-1,3),0).astype(int)   # poot eronder, licht
legd=np.array([102,102,102])                                     # poot eronder, schaduwkant (x43 r58-59)
print('poottint',legc,legd)
reg=strook&m
for y,x in zip(*np.nonzero(reg)):
    if (~m[max(y-1,0):y+2,max(x-1,0):x+2]).any(): out[y,x,:3]=[2,2,2]; continue
    out[y,x,:3]=legd if (~m[y,max(x-2,0):x]).any() else legc
# zwarte pixels direct rechts van het strookje die het van de poot scheiden
for y in range(46,60):
    xs=[x for x in range(36,50) if reg[y,x]]
    if not xs: continue
    x=max(xs)+1
    while x<49 and L[y,x]<45 and m[y,x] and m[y,x+1] and L[y,x+1]>45: 
        out[y,x,:3]=legc; x+=1
nD=(np.abs(out-nat).sum(2)>0).sum()-nC
# A+B: haren (dunne strepen) weg via opening, alleen in de haarzones
op=nd.binary_opening(m,np.ones((3,3),bool))
Z=np.zeros_like(m)
Z[8:27,27:62]=1; Z[27:47,50:68]=1; Z[38:49,9:23]=1
keep=np.where(Z,op,m)
lab,n=nd.label(keep); sz=nd.sum(keep,lab,range(1,n+1)); keep=lab==(np.argmax(sz)+1)
weg=m&~keep
out[~keep]=0
print('gewijzigd natief: wig',nC,'strook',nD,'haren weg',weg.sum())
Image.fromarray(out.astype(np.uint8)).save('natief_bewerkt.png')
v=out.copy(); v[weg]=[255,0,0,255]; v[(np.abs(out-nat).sum(2)>0)&keep]=[0,160,255,255]
big=lambda a:Image.fromarray(a.astype(np.uint8)).resize((700,770),Image.NEAREST)
c=Image.new('RGBA',(1420,770),'white'); c.paste(big(nat),(0,0),big(nat)); c.paste(big(v),(720,0),big(v)); c.save('natief_check.png')
np.save('weg.npy',weg)
