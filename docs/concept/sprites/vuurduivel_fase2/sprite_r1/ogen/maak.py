# maak.py: oogvarianten voor vuurduivel2_r1. Elk oog = pixels 1-op-1 uit een echte Gen 3-sprite (anim_front.png, frame 1),
# alleen omgekleurd naar zwart / donkerrood / rood, geen wit. Bron-indexen per klasse:
#  L = lijn (zwart), S = wit/licht (oogwit, glans, lichte iris), I = iris/pupil (rood), D = donkere iris.
# Twee kleurversies: X = S->rood, I/D->zwart ; Y = S->zwart, I->rood, D->donkerrood.
# A = de versie met het meeste rood ("rood met zwart erin"), B = de andere ("zwart met rood erin").
# Basis: r1 met de oude oogpixels (27-29, 19-20) op de donkere maskertint (22,22,22); daarna het bronoog erop. Zone x25-31, y17-21; daarbuiten diff 0.
import numpy as np, os; from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
CH='.#dgHhBcCRrOAYE'
PAL=[(0,0,0),(3,1,1),(22,22,22),(40,40,40),(50,40,34),(80,64,52),(124,97,77),(218,184,134),(240,229,186),
     (105,20,22),(138,30,34),(205,75,50),(240,135,62),(250,205,110),(200,36,40)]
# bron: (soort, {bronindex: klasse}, bron-bbox x0,y0,x1,y1 (incl), doelverschuiving dx,dy, extra uitgesloten bronpixels)
BRON=[
 ('absol',   {'1':'L','2':'L','5':'L','b':'D','c':'I','d':'S','7':'S'}, (22,24,27,26), (3,-6)),
 ('sharpedo',{'5':'L','8':'S','9':'D','a':'I'}, (24,39,28,43), (2,-22)),
 ('sneasel', {'7':'L','b':'S','c':'S','2':'I'}, (30,21,35,24), (-4,-4)),
 ('umbreon', {'3':'L','9':'S','8':'D','a':'I'}, (19,26,23,28), (7,-8)),
 ('banette', {'2':'L','5':'L','9':'S','8':'I','7':'D'}, (17,25,20,28), (10,-7)),
]
def laad(f):
    im=Image.open(f); return np.asarray(im).astype(int)
r1=laad('../vuurduivel2_r1.png').copy()
basis=r1.copy()
for x in (27,28,29):
    for y in (19,20): basis[y,x]=2
def bouw(o,fn):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[c for t in PAL for c in t]; p+=[0]*(768-len(p)); im.putpalette(p); im.save(fn,transparency=0,bits=4)
def rgba(fn,bg=(255,255,255)):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(Image.open(fn).convert('RGBA')); return b.convert('RGB')
opties=[]; log=[]
for soort,kl,(x0,y0,x1,y1),(dx,dy) in BRON:
    s=laad(G+soort+'/anim_front.png')[:64]
    pix=[(x,y,kl['%x'%s[y,x]]) for y in range(y0,y1+1) for x in range(x0,x1+1) if '%x'%s[y,x] in kl]
    for naam,mp in (('X',{'L':1,'S':14,'I':1,'D':1}),('Y',{'L':1,'S':1,'I':14,'D':9})):
        o=basis.copy()
        for x,y,c in pix: o[y+dy,x+dx]=mp[c]
        rood=sum(1 for x,y,c in pix if mp[c]!=1)
        opties.append([soort,naam,o,rood,pix,(dx,dy)])
# A/B toekennen per bron
uit=[]
for i in range(0,len(opties),2):
    a,b=opties[i],opties[i+1]
    if b[3]>a[3]: a,b=b,a
    a[1],b[1]='A','B'; uit+= [a,b]
# diff-bewijs + bestanden
zone=np.zeros((64,64),bool); zone[17:22,25:32]=True
for soort,ab,o,rood,pix,(dx,dy) in uit:
    d=(o!=r1)&~zone; assert d.sum()==0, (soort,ab,d.sum())
    fn='oog_%s_%s.png'%(soort,ab); bouw(o,fn)
    n=int((o!=r1).sum())
    log.append('%s %s: %d bronpixels, verschuiving (%d,%d), %d px anders dan r1 (alle in zone x25-31 y17-21), %d rood'%(soort,ab,len(pix),dx,dy,n,rood))
open('diff.txt','w').write('\n'.join(log)+'\n'); print('\n'.join(log))
# opties.png: per optie kop 8x (x16-37, y10-29) + label, plus 1x op wit en donker; bovenaan r1 en het model
W=22*8; H=20*8
kols=4; rijen=(len(uit)+2+kols-1)//kols
v=Image.new('RGB',(kols*(W+12)+12,rijen*(H+110)+12),(235,235,235)); d=ImageDraw.Draw(v)
from PIL import Image as I
nat=I.open('../natief.png'); X0,Y0,NX,NY=4,5,62,6
model=nat.crop((NX+(16-X0)*2,NY+(10-Y0)*2,NX+(38-X0)*2,NY+(30-Y0)*2)).resize((W,H),I.NEAREST)
items=[('model (natief)',None,model),('r1 (huidig)','../vuurduivel2_r1.png',None)]+[('%s %s'%(s,ab),'oog_%s_%s.png'%(s,ab),None) for s,ab,*_ in uit]
for k,(lab,fn,img) in enumerate(items):
    cx=12+(k%kols)*(W+12); cy=12+(k//kols)*(H+110)
    if img is None: img=rgba(fn).crop((16,10,38,30)).resize((W,H),I.NEAREST)
    v.paste(img,(cx,cy)); d.text((cx,cy+H+4),lab,fill=(0,0,0))
    if fn:
        v.paste(rgba(fn),(cx,cy+H+18)); v.paste(rgba(fn,(40,40,56)),(cx+70,cy+H+18))
v.save('opties.png')
