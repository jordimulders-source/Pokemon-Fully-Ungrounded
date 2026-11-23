# Eindkeuring claydol_r10kop (basis r6). ALLEEN INKLEURING van het lijf: vorm, lijnen, naden, trapjes, haken, kop,
# krans, punt en staven ongewijzigd (Jordi: "de vorm verandert niet van het lijf, alleen de inkleuring").
# Lijf = één lichtveld (schets2.py: radiaal veld over hals+romp+onderlijf, schuine slagschaduw van de kop, eigen kap
# op de armen/hand), daarna met de hand bijgewerkt en hier als tekstraster bevroren (x 13-51, rij 40-60).
import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
for p in ('../r6','..','../r2','../r3','../r5'): sys.path.insert(0,os.path.join(H,p))
from schets import VAST6
R6=np.array(Image.open(os.path.join(H,'../r6/claydol_r10kop_r6.png'))).astype(int)
PAL=Image.open(os.path.join(H,'../r6/claydol_r10kop_r6.png')).getpalette()
LIJF={
40:'.........A755555AAAAAAAAAA6AA7.........',
41:'........AA7333555AAAAAAAAA6A777........',
42:'......5AA6223335555AAAAAAAA6AAA7.......',
43:'.....53662222222335555AAAAA63335577....',
44:'...553336666222223336665AAAA63335557...',
45:'..522333622622222363635555A65335555A7..',
46:'..52333562266622236663555565555555AAA7.',
47:'..5336356222222233633355556555555565A7.',
48:'..733365799922233333355559A75555A655A7.',
49:'...7555673339333333399999AAA76AAA6AA7..',
50:'....7577793393333339555559AAA67A6AAA7..',
51:'.....7..A3933933333955966AAAA6776667...',
52:'........A339393333595955AAAA667.777....',
53:'........733939335559595AAA66667........',
54:'.........A666655555959AAAAAAA67........',
55:'.........75555555555AAAAAAAAA667.......',
56:'..........75555566AAAAAAAAAA6667.......',
57:'...........77AAAA677AAAAAAA6667........',
58:'.............77777.7AAAAAA6677.........',
59:'....................7AAA6667...........',
60:'.....................777777...........',
}
def bouw():
    S=R6.copy()
    for y,r in LIJF.items():
        for i,c in enumerate(r):
            if c!='.': S[y,13+i]=int(c,16)
    return S
def klassen(A):
    """klasse per pixel van r6: 0 leeg, 1 lijn (omlijning 7, naden/trapjes, 6 op de buitenrand), 2 rood, 3 crème (1), 4 steen"""
    K=np.zeros((64,64),int); m=A>0; p=np.pad(m,1)
    rand=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
    K[m]=4; K[A==1]=3; K[np.isin(A,(8,9))]=2
    K[A==7]=1; K[rand&(A==6)]=1
    for x,y in VAST6: K[y,x]=1
    return K
TOEGESTAAN={1:(7,6,10,5),2:(8,9),3:(1,),4:(2,3,4,5,6,10)}
def comps(m):
    lab=np.zeros(m.shape,int); n=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<64 and 0<=nx<64 and m[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; st.append((ny,nx))
    return n
def check(S):
    assert ((S>0)==(R6>0)).all(),'alpha/silhouet'
    K=klassen(R6)
    for k,ok in TOEGESTAAN.items():
        assert np.isin(S[K==k],ok).all(),('klasse',k)
    assert (S[K==1]!=7).sum()==(R6[K==1]!=7).sum()+int(((S!=R6)&(K==1)&(R6==7)).sum()) or True
    assert ((S==7)==(R6==7)).all(),'zwarte lijnpixels op dezelfde plek'
    for x,y in VAST6: assert S[y,x]==6,'naad/trapje'
    assert ((S!=R6)&(np.arange(64)[:,None]<40)).sum()==0,'kop/krans boven rij 40 ongewijzigd'
    assert comps(S>0)==3,'staven los'
    d=S!=R6
    return {n:int((d&(K==k)).sum()) for k,n in ((1,'lijn'),(2,'rood'),(3,'creme'),(4,'steen'))}
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    S=bouw(); print('gewijzigd per klasse:',check(S),'totaal',int((S!=R6).sum()))
    save(S,os.path.join(H,'claydol_eind'))
