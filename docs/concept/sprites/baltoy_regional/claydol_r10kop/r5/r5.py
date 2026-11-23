# Ronde 5 (basis r4, bevroren buiten de opdrachtzones):
# 1. afbuiging van de rode lijn naast het rechteroog k px hoger (k=2/3); horizontale loop zelfde vorm, k px hoger.
#    Waar rood verdwijnt: de r4-onderlaag (kopshading/oog zoals r4 die had zonder golf).
# 2+3. lijf + rechterhand met de hand ingekleurd (tekstraster LIJF hieronder); 7/8/9-plaatsen, trapjes, plooien blijven.
import os, sys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
for p in ('..','../r2','../r3','../r4'): sys.path.insert(0,os.path.join(H,p))
import r4 as R4
from r2 import LIJF, KIN, R1, ontspikkel, oog_asset
from r3 import PAL
from lagen import G as G3
yy,xx=np.mgrid[0:64,0:64]
B=np.array(Image.open(os.path.join(H,'../r4/claydol_r10kop_r4.png'))).astype(int)

def golf_mask(P):
    M=np.zeros((64,64),bool)
    for (x0,y0),(x1,y1) in zip(P[:-1],P[1:]):
        vx,vy=x1-x0,y1-y0; L2=vx*vx+vy*vy
        t=np.clip(((xx-x0)*vx+(yy-y0)*vy)/L2,0,1)
        M|=((xx-(x0+t*vx))**2+(yy-(y0+t*vy))**2)<=1.0001
    return M
LINKS=[(11,18),(12,18),(13,17),(14,16),(15,15),(16,14),(18,14),(19,15),(20,16),(21,17),(22,18),(23,19),(24,20),(25,20),
       (26,19),(27,18),(28,17),(29,16),(30,15),(31,14),(35,14),(36,15),(37,16),(38,17),(39,18),(40,19)]
STAART={0:[(41,20),(41.5,21),(41.5,22),(42,23),(43,24),(44,24.6),(46,25),(48,25.3),(53,25.8)],          # = r4
        2:[(41,20),(42,21),(43,22),(44,22.6),(46,23),(48,23.3),(53,23.8)],
        3:[(41,19.8),(42,20.3),(43,21),(44,21.6),(46,22),(48,22.3),(53,22.8)]}
def golf(k,d=1):
    P=[(x,y+d) for x,y in LINKS+STAART[k]]; return golf_mask(P)

def onderlaag():
    """r4 zonder golf: zelfde bouw als r4.bouw(1) maar de golf weggelaten"""
    S=R1.copy(); M={k:np.zeros((64,64),bool) for k in ('neus','oog','rood','barst')}
    R4.kop(S,1,M)
    N=-np.ones((13,6),int)
    for y,(a,b) in R4.NEUS_RIJEN.items():
        for x in range(a,b+1): N[y-22,x-22]=G3[y,x]
    R4.plak(S,N,22,23,M['neus']); R4.plak(S,oog_asset(),27,19,M['oog']); R4.plak(S,oog_asset(weg_k=(27,35)),12,18,M['oog'])
    vlak,sel=R4.lijf(S)
    steen=KIN&~(M['neus']|M['oog']|M['barst']); ontspikkel(S,steen|vlak)
    return S

LIJFTXT={
40:'.........6755555555555AAAA6AA7.........',
41:'........5575555555555AAAAA6A777........',
42:'......655655555555555AAAAAA6AAA7.......',
43:'.....636622222222333333355565555577....',
44:'...552236666222222336663555563333357...',
45:'..522233622622222363633555563335555A7..',
46:'..632235622666223366633555655555555AA7.',
47:'..633635622233333363333555655555556357.',
48:'..735565788833333333335559575555563357.',
49:'...75AA6733393333333888885AA7655A6357..',
50:'....7A777933933333395555595AA67A6AAA7..',
51:'.....7..659339333359559665AAA677AAA7...',
52:'........65593933355959555AAA6A7.777....',
53:'........755939555559595AAA66667........',
54:'.........66666AAAAA959AAA6A6667........',
55:'7........7333335553333335555AAA7......6',
56:'7.........733355663333355555AAA7......6',
57:'57.........77AAAA67755555AAAAA7......53',
58:'7............77777.7555AAAAA77.......53',
59:'....................75AAAAA7........535',
}

def lijf(S):
    T=np.full((64,64),-1)
    for y,s in LIJFTXT.items():
        for i,c in enumerate(s):
            if c!='.': T[y,13+i]=int(c,16)
    m=LIJF&(yy>=40)&(T>=0)
    S[m]=T[m]; return m

VAST=(np.isin(B,(7,8,9)))&LIJF          # tekening die moet blijven (rood mag 8/9 wisselen)
G3R5=np.array(Image.open(os.path.join(H,'../../claydol_gemini_r3/r5/claydol_g3r5_paletB.png'))).astype(int)
def neus(S):
    """neus pixel voor pixel = g3r5 (1 px lager): de 5 randpixels waar de oogringen overheen vielen terug naar g3r5;
       ring van het linkeroog wijkt 1 px naar links (x21, y23-25); rechterring lag al dubbel (x28) en blijft"""
    M=np.zeros((64,64),bool)
    for x,y in ((22,23),(22,24),(22,25),(27,25),(27,26)): S[y,x]=G3R5[y-1,x]; M[y,x]=True
    for y in (23,24,25): S[y,21]=6; M[y,21]=True
    return M
def bouw(k):
    S=B.copy()
    oud=golf(0); nieuw=golf(k); O=onderlaag()
    weg=oud&~nieuw&KIN; S[weg]=O[weg]
    C=np.where(nieuw,9,0)
    for x in range(64):
        ys=np.where(nieuw[:,x])[0]
        if len(ys) and x<=36: C[ys[0],x]=8
    erbij=nieuw&KIN; S[erbij]=C[erbij]
    nz=neus(S)
    lm=lijf(S)
    return S,weg|erbij|nz,lm

def check(S,zone,lm):
    assert ((S>0)==(B>0)).all(),'silhouet'
    assert not ((S!=B)&~zone&~lm).any(),'buiten zones'
    assert ((np.isin(S,(8,9)))==(np.isin(B,(8,9))))[LIJF].all(),'rode haken'
    assert ((S==7)==(B==7))[LIJF].all(),'omlijning lijf'
    tr=[(22,44),(23,44),(24,44),(24,45),(24,46),(25,46),(26,46),(33,44),(34,44),(35,44),(31,45),(33,45),(31,46),(32,46),(33,46),(31,47),(21,43),(21,44),(21,45),(21,46),(21,47),(18,47),(19,48),(20,49),(47,47),(46,48),(46,49),(45,50)]
    assert all(S[y,x]==6 for x,y in tr),'trapjes/plooien'
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    for k in (2,3):
        S,z,lm=bouw(k); check(S,z,lm); save(S,os.path.join(H,'claydol_r10kop_r5_bocht%d'%k))
        d=(S!=B); print('k',k,'lijn px',int((d&z).sum()),'lijf px',int((d&lm).sum()),'rood weg',int((golf(0)&~golf(k)&KIN).sum()),'rood erbij',int((golf(k)&~golf(0)&KIN).sum()))

def lever(k=2):
    S,z,lm=bouw(k); check(S,z,lm); save(S,os.path.join(H,'claydol_r10kop_r5'))
    d=S!=B
    nz=np.zeros((64,64),bool); nz[23:27,21:28]=True
    print('r5 = bocht %d; afwijkend van r4: totaal %d | lijn %d | neus+ring %d | lijf %d | elders %d'%(k,d.sum(),(d&z&~nz).sum(),(d&nz).sum(),(d&lm).sum(),(d&~z&~lm).sum()))
    print('silhouet gelijk:',((S>0)==(B>0)).all(),' staven/krans/punt (buiten KIN en LIJF) diff:',int((d&~KIN&~LIJF).sum()))
