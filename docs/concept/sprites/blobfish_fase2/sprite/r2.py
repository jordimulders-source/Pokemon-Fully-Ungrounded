# r2 = r1 (bevroren) + vier zones opnieuw uit het model; buiten de zones diff 0 (bewezen onderaan).
import json; import numpy as np
from zone import *
r1=np.load('r1_bevroren.npy'); o=r1.copy()
op=r1>0; p=np.pad(op,1); RAND=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
zones={}
# 1. mond + neus: variant v2 uit mond_var.py (fase x 1/3, y 1/3, lipregel: lipkleur wint bij >=40% lip in het blok)
MV=np.load('mond_varianten.npy'); MJ=json.load(open('mond_varianten.json')); k=[n for n,r in enumerate(MJ) if abs(r[1]-1/3)<.01 and abs(r[2]-1/3)<.01 and r[3]][0]
Zm=np.zeros((64,64),bool); Zm[33:47,6:38]=True; Zm&=op&~RAND
o[Zm]=MV[k][Zm]; zones['mond+neus']=Zm
# 2. ogen: variant o5 uit ogen_var.py (fase x 1/3, y 1/3, oogzwart >=30%, rest vulkleur incl. grijze oogkas)
OV=np.load('ogen_varianten.npy'); Zo=np.zeros((64,64),bool); Zo[29:33,13:18]=True; Zo[29:33,28:33]=True; Zo&=op&~RAND
o[Zo]=OV[5][Zo]; zones['ogen']=Zo
# 3. grijze schaduw rechts: vlakpixels (geen lijn, geen rand, niet de vin) opnieuw getoond = mediaan van het modelblok (zonder lijncellen)
Zg=np.zeros((64,64),bool); Zg[22:49,33:57]=True; Zg[36:49,49:57]=False; Zg&=op&~RAND&~Zm&~Zo&~np.isin(r1,[1,9])
KAND=[c for c in GRP if c!=9]; ng=0
for j,i in zip(*np.where(Zg)):
    X=[RGB[y,x] for y,x,w in cellen(i,j,0,0) for _ in range(int(round(w*4))) if AL[y,x] and not ZW[y,x] and not D9[y,x]]
    if X: o[j,i]=dichtst(np.median(np.array(X),0),KAND)
# alleen in de grijze zone: tintvlakjes < 3 px (behalve glans) -> meest voorkomende buurtint van de zone
def klein(o,Z):
    n=0
    for c in [c for c in GRP if c not in (2,9)]:
        m=(o==c)&Z; seen=np.zeros_like(m)
        for y,x in zip(*np.where(m)):
            if seen[y,x]: continue
            st=[(y,x)]; cl=[]; seen[y,x]=1
            while st:
                a_,b_=st.pop(); cl.append((a_,b_))
                for aa,bb in ((a_-1,b_),(a_+1,b_),(a_,b_-1),(a_,b_+1)):
                    if m[aa,bb] and not seen[aa,bb]: seen[aa,bb]=1; st.append((aa,bb))
            if len(cl)<3:
                bu=[o[aa,bb] for a_,b_ in cl for aa,bb in ((a_-1,b_),(a_+1,b_),(a_,b_-1),(a_,b_+1)) if Z[aa,bb] and o[aa,bb] not in (c,1,9)]
                if bu:
                    v=max(set(bu),key=bu.count)
                    for a_,b_ in cl: o[a_,b_]=v; n+=1
    return n
for Z in (Zg,Zm): klein(o,Z)
zones['grijs rechts']=Zg
# 4. losse donkere binnenlijnpixels (index 9 in een 8-verbonden groepje lijnpixels (zwart of 9, rand meegeteld) van <= 2 px, niet op de rand): blijven alleen als het model daar een donkere lijn heeft (>=25% van het blok)
Zl=np.zeros((64,64),bool); m=np.isin(o,[1,9]); seen=np.zeros_like(m); weg=[]; blijf=[]
for y,x in zip(*np.where(m)):
    if seen[y,x]: continue
    st=[(y,x)]; cl=[]; seen[y,x]=1
    while st:
        a_,b_=st.pop(); cl.append((a_,b_))
        for aa,bb in ((a_+dy,b_+dx) for dy in (-1,0,1) for dx in (-1,0,1)):
            if m[aa,bb] and not seen[aa,bb]: seen[aa,bb]=1; st.append((aa,bb))
    if len(cl)>2 or any(RAND[a_,b_] for a_,b_ in cl): continue
    for a_,b_ in cl:
        if o[a_,b_]!=9: continue
        tw=sum(w for *_,w in cellen(b_,a_,0,0)); dl=sum(w for yy,xx,w in cellen(b_,a_,0,0) if D9[yy,xx] or ZW[yy,xx])
        if dl/tw>=0.25: blijf.append((b_,a_))
        else:
            X=[RGB[yy,xx] for yy,xx,w in cellen(b_,a_,0,0) if AL[yy,xx] and not ZW[yy,xx] and not D9[yy,xx]]
            o[a_,b_]=dichtst(np.median(np.array(X),0),KAND); Zl[a_,b_]=True; weg.append((b_,a_))
zones['losse donkere px']=Zl
for Z in (Zg,Zm,Zo,Zl): klein(o,Z|np.zeros_like(Z))
print('losse 9-pixels weg',len(weg),'blijven (model heeft daar een lijn)',len(blijf))
np.save('r2.npy',o); opslaan(o,'r2.png')
# bewijs: diff buiten de zones
alle=np.zeros((64,64),bool)
for n,Z in zones.items(): alle|=Z; print(f'{n}: zone {Z.sum()} px, gewijzigd {((o!=r1)&Z).sum()} px')
print('gewijzigd BUITEN de zones:',((o!=r1)&~alle).sum(),'| totaal gewijzigd t.o.v. r1:',(o!=r1).sum(),'| silhouet gelijk:',((o>0)==(r1>0)).all())
k0=np.load('kaal.npy'); print('afwijkend van de kale reductie (fase 0): r1',(r1!=k0).sum(),'r2',(o!=k0).sum())
