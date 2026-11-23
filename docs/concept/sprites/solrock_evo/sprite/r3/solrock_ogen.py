# Ronde 3 (Jordi: "kopieer gewoon solrocks ogen en pas die dan aan"):
# Solrocks oog pixel voor pixel uit graphics/pokemon/solrock/anim_front_gba.png (bovenste 64x64, oog x29-39, y28-44).
# Solrock heeft maar een oog; dat oog wordt voor beide ogen gebruikt.
# Aangepast = alleen rijen/kolommen geschrapt (uit het midden, zodat de buitenring heel blijft) + kleuren naar ons palet.
# Letterlijk = hele oog 1-op-1, Solrocks eigen kleuren, gecentreerd op de modelogen, niets geschrapt.
# Basis = r2 met de B-onderpuntjes terug naar r1.
import numpy as np; from PIL import Image
SR=Image.open('../../../../../../graphics/pokemon/solrock/anim_front_gba.png'); sa=np.array(SR)[:64]; spal=SR.getpalette()
ORANJE={5,6,7,8,9,10,11}            # Solrocks gezicht rond het oog (niet meegenomen)
r1={v:np.array(Image.open(f'../r1/{v}.png')) for v in 'AB'}
r2={};PAL=None
for v in 'AB':
    im=Image.open(f'../r2/{v}.png'); r2[v]=np.array(im); PAL=im.getpalette()
TERUG=[(28,42),(29,42),(30,42),(32,42),(33,42),(28,43),(29,43),(30,43),(32,43),(33,43)]
base={}
for v in 'AB':
    b=r2[v].copy()
    if v=='B':
        for x,y in TERUG: b[y,x]=r1['B'][y,x]
    base[v]=b
# --- oude ogen (r2) weghalen: oogzones terug naar ondergrond
BOX={'R':(24,34,31,42),'L':(14,23,30,40)}     # x0,x1,y0,y1 (excl.)
OPKERN={'A':'R','B':'L'}
def leeg(o,v,k):
    x0,x1,y0,y1=BOX[k]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if o[y,x] in (11,12,5) or (o[y,x]==1 and r2[v][y,x]==1 and (y,x) in OOGK[v][k]):
                o[y,x]=3 if k==OPKERN[v] else (7 if y<=34 else 8)
# zwarte oogkas-pixels uit r2 (het kader dat de coordinator zette)
OOGK={}
for v in 'AB':
    OOGK[v]={'R':{(y,x) for y in range(34,39) for x in range(26,33)},'L':{(y,x) for y in range(34,38) for x in range(17,22)}}
# --- palet: Solrock-index -> ons palet (+2 extra)
PAL=PAL[:16*3]+[0]*(48-len(PAL[:48]))
PAL[13*3:13*3+3]=[238,213,115]      # extra 1: Solrocks middelste lensgeel (2)
PAL[14*3:14*3+3]=[139,115,115]      # extra 2: Solrocks lichte ringgrijs (13), voor het oog op de kern
MAP_PLAAT={15:1,14:4,13:4,1:5,2:13,3:6,4:6,12:12}
MAP_KERN ={15:1,14:4,13:14,1:5,2:13,3:6,4:6,12:12}
KEEP={'R':([31,33,34,35,36,37,38,39,41],[29,30,31,33,34,35,37,38,39]),
      'L':([31,33,35,36,37,39,41],[29,30,33,34,35,38,39])}
CENTRUM={'R':(28.5,36.0),'L':(18.5,34.5)}   # midden van de modelogen (spritepx)
def plak(o,rows,cols,k,mapping,overschrijf=True):
    h,w=len(rows),len(cols); cx,cy=CENTRUM[k]
    x0=int(round(cx-w/2+0.01)); y0=int(round(cy-h/2+0.01))
    for dy,j in enumerate(rows):
        for dx,i in enumerate(cols):
            s=sa[j,i]
            if s in ORANJE or s==0: continue
            o[y0+dy,x0+dx]=mapping[s] if mapping else s
    return x0,y0
info=[]
for v in 'AB':
    o=base[v].copy(); leeg(o,v,'R'); leeg(o,v,'L')
    for k in 'RL':
        m=MAP_KERN if k==OPKERN[v] else MAP_PLAAT
        x0,y0=plak(o,*KEEP[k],k,m); info.append((v,k,x0,y0))
    im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(PAL+[0]*(768-48)); im.save(f'{v}.png',transparency=0)
    np.save(f'{v}.npy',o)
    # letterlijk: Solrocks eigen kleuren -> extra paletplaatsen (vergelijkingsmateriaal, >16 kleuren)
    L=base[v].copy(); leeg(L,v,'R'); leeg(L,v,'L')
    P2=PAL[:13*3]; extra={}
    for s in sorted({int(x) for x in sa[28:45,29:40].ravel()}-ORANJE-{0}):
        extra[s]=len(P2)//3; P2+=spal[3*s:3*s+3]
    rows=list(range(28,45)); cols=list(range(29,40))
    for k in 'LR': plak(L,rows,cols,k,extra)
    im=Image.fromarray(L.astype('uint8'),'P'); im.putpalette(P2+[0]*(768-len(P2))); im.save(f'{v}_letterlijk.png',transparency=0)
    np.save(f'{v}_letterlijk.npy',L)
print(info)
# --- bewijs: buiten oog- en plaatzone diff 0 met r2
for v in 'AB':
    o=np.load(f'{v}.npy'); zone=np.zeros((64,64),bool)
    for (x0,x1,y0,y1) in BOX.values(): zone[y0:y1,x0:x1]=True
    d=o!=r2[v]
    tp=np.zeros_like(d)
    for x,y in TERUG: tp[y,x]=True
    print(v,'diff met r2:',int(d.sum()),'| buiten oogzones:',int((d&~zone).sum()),'(waarvan B-onderpuntjes terug:',int((d&tp).sum()),') | kleuren',len(np.unique(o)))
