# Ronde 3: oogvarianten op r2. Oogvorm E1 = de reductie van de modelogen (rood/zwart-fracties per spritepixel uit model.png):
#  rechts: zwaar bovenlid rij 34 (x26-31), zwarte V-inkeping (28,35) (model 55% zwart), lichtere onderhelft, smalle onderlob (28-29,37), punt (28-29,38)
#  links : lid rij 33 (x17-20), rood 2x2 (18-19,34-35) met lichtrood rechtsonder, taps (18-19,36)
# E2 = principe van Solrocks eigen oog (lichte lens, zwarte rand, rode spleet) op de modelmaat en -plek.
# E3/E4 = E1/E2 + lichte oogkas (G3, kerngrijs) rond alleen het oog op de zwarte kern.
# B: kleine onderpuntjes uit r2 terug naar r1 (grote onderpunt x23-25 blijft).
import numpy as np; from PIL import Image
C={'K':1,'R':12,'r':11,'W':5,'C':5,'Y':6}
E={
 'E1':{'R':(26,34,["KKKKKK","KRKWRK","KRrrRK",".KrrK.","..KK.."]),
       'L':(17,33,["KKKK","KWRK","KRrK",".KK."])},
 'E2':{'R':(26,34,[".KKKK.","KCCCCK","KKRRKK","KYYYYK",".KKKK."]),
       'L':(17,33,[".KK.","KCCK","KRRK","KYYK",".KK."])},
}
E['E3']=E['E1']; E['E4']=E['E2']
BOX={'R':(26,33,32,39),'L':(16,22,32,38)}   # x0,x1(excl),y0,y1(excl): oogzone
def laad(f):
    im=Image.open(f); return np.array(im),im.getpalette()
r1={v:laad(f'../r1/{v}.png')[0] for v in 'AB'}
for v in 'AB':
    r2,pal=laad(f'../r2/{v}.png')
    base=r2.copy()
    if v=='B':
        for x,y in [(28,42),(29,42),(30,42),(32,42),(33,42),(28,43),(29,43),(30,43),(32,43),(33,43)]:
            base[y,x]=r1['B'][y,x]
    opkern={'A':'R','B':'L'}[v]          # welk oog op de kern ligt
    for e,spec in E.items():
        o=base.copy()
        for k,(x0,y0,rows) in spec.items():
            bx0,bx1,by0,by1=BOX[k]
            # oogzone eerst leeg: kern -> G2, plaat -> plaattint uit r1 (of P1 boven / P2 onder het oog)
            for y in range(by0,by1):
                for x in range(bx0,bx1):
                    if k==opkern: o[y,x]=3
                    else:
                        t=r1[v][y,x]
                        o[y,x]=t if t in (7,8,9,10) else (7 if y<=y0 else 8)
            for dy,row in enumerate(rows):
                for dx,ch in enumerate(row):
                    if ch!='.': o[y0+dy,x0+dx]=C[ch]
            if e in ('E3','E4') and k==opkern:
                eye=np.zeros_like(o,bool)
                for dy,row in enumerate(rows):
                    for dx,ch in enumerate(row):
                        if ch!='.': eye[y0+dy,x0+dx]=True
                for y in range(by0-1,by1+1):
                    for x in range(bx0-1,bx1+1):
                        if not eye[y,x] and o[y,x] in (2,3) and any(eye[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1))):
                            o[y,x]=4
        im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save(f'{v}_{e}.png',transparency=0)
        # bewijs: buiten oog- en plaatzone diff 0 met r2
        zone=np.zeros_like(o,bool)
        for (bx0,bx1,by0,by1) in BOX.values(): zone[by0-1:by1+1,bx0-1:bx1+1]=True
        plaat=np.isin(r2,[7,8,9,10])|np.isin(r1[v],[7,8,9,10])
        d=(o!=r2); print(v,e,'diff met r2 totaal',int(d.sum()),'| buiten oog-+plaatzone',int((d&~zone&~plaat).sum()),'| kleuren',len(np.unique(o)))
