# r4: oogvarianten V1-V5 + monocle-ringen R1/R2. Alleen pixels uit echte sprites (1-op-1, omgekleurd naar grijs),
# geknipt/verschoven; niets getekend. Tonen: 0=16 1=32 2=64 3=96 4=112 5=144 6=208 7=248 (gezichtswit).
# Plaats: verre oog x29-31 (x28 blijft wit tot de rand x27), nabije oog in de monocle (binnenkant x37-41, y16-20).
import numpy as np; from PIL import Image
G='../../../../../graphics/pokemon/%s/%s.png'
def bron(p,f='anim_front_gba'): return np.asarray(Image.open(G%(p,f))).astype(int)
MIME,CHAN,MEW,MAGN,RIME=bron('mr_mime'),bron('hitmonchan'),bron('mewtwo'),bron('magnemite'),bron('mr_rime','front')
# omkleuring per bron (paletindex -> toon); niet genoemd = huid/achtergrond -> gezichtswit 7
K_MIME={14:0,3:3,15:7,1:6,2:5,4:2}            # e zwart, 3 (90) pupilgrijs, f wit, 1 (205) lichtgrijs
K_CHAN={15:0,1:7,14:2,5:3}                    # f zwart, 1 wit, e (106) bruine lijn -> 64
K_MEW={14:0,15:7,1:7,2:6,3:5,4:2,5:6,6:5,7:3,8:2}
K_RIME={0xa:7,6:6,7:5,0xb:0,8:5,3:0,1:0}
def knip(S,K,y0,y1,x0,x1):
    return [[K.get(S[y,x],7) for x in range(x0,x1+1)] for y in range(y0,y1+1)]
# oogpatches (rijen van tonen); verre oog = smallere uitsnede (perspectief)
P={
 'V1':(knip(MIME,K_MIME,19,21,24,25), knip(MIME,K_MIME,20,23,30,31)),     # Mr. Mime: ver = linkeroog, nabij = rechteroog
 'V3':(knip(CHAN,K_CHAN,18,22,26,28), knip(CHAN,K_CHAN,19,23,33,37)),     # Hitmonchan compleet (nabij: x32 lidpunt eraf)
 'V4':(knip(MEW,K_MEW,14,17,36,38),   knip(MEW,K_MEW,14,17,36,40)),       # Mewtwo-oog (ver: rechterkolommen eraf)
}
# plaats (bovenrij, linkerkolom) van ver / nabij oog
POS={'V1':((18,29),(17,38)), 'V3':((16,29),(16,37)), 'V4':((16,29),(16,37))}
# Hitmonchan-lid (recht stuk, 3 px zwart) voor V2/V5
LID_VER=[(17,29),(17,30),(17,31)]; LID_NAB=[(17,38),(17,39),(17,40)]
# ringen (x36-42, y15-21): R1 = Magnemite-oogomtrek (rij 29-35, x30-36), R2 = modelring factor 2.3, fase (39.7,18.6), 1 omhoog/1 links
def ring_magn():
    return [(y-29+15,x-30+36) for y in range(29,36) for x in range(30,37) if MAGN[y,x]==14]
def ring_model():
    a=np.asarray(Image.open('natief_stok.png').convert('L')).astype(int); cx,cy=104,63
    yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]]; d=np.hypot(xx-cx,yy-cy)
    up=np.repeat(np.repeat((a<140)&(d>=5)&(d<=8.6),10,0),10,1).astype(float); F=2.3; sx=39.7; sy=18.6; out=[]
    for y in range(13,25):
        for x in range(33,46):
            x0=cx+(x-sx-0.5)*F; y0=cy+(y-sy-0.5)*F
            if up[int(y0*10):int((y0+F)*10), int(x0*10):int((x0+F)*10)].mean()>=0.4: out.append((y-1,x-1))
    return out
RINGEN={'R1':ring_magn,'R2':ring_model}
def binnen(ring):
    rs=set(ring); out=set()
    for y in range(15,22):
        xs=[x for x in range(30,48) if (y,x) in rs]
        if len(xs)>=2:
            for x in range(min(xs)+1,max(xs)):
                if (y,x) not in rs: out.add((y,x))
    return out
def maak(C,var,rv='R1',log=None):
    C=C.copy(); log={} if log is None else log
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    for y in range(15,21):                                   # oogvlak leeg -> gezichtswit
        for x in range(28,44):
            if C[y,x]!=-1: zet(y,x,7,'oogvlak leeg -> gezichtswit')
    ring=RINGEN[rv](); BIN=binnen(ring)
    for (y,x) in ring:
        if 15<=y<=20: zet(y,x,2,'monocle %s (tint 64)'%rv)   # rij 21 = zwarte snorrand, blijft
    basis=var if var in P else {'V2':'V1'}.get(var)
    if basis:
        (pv,pn),((vy,vx),(ny,nx))=P[basis],POS[basis]
        for i,r in enumerate(pv):
            for j,t in enumerate(r): zet(vy+i,vx+j,t,'verre oog (%s)'%basis)
        for i,r in enumerate(pn):
            for j,t in enumerate(r):
                if (ny+i,nx+j) in BIN: zet(ny+i,nx+j,t,'nabije oog (%s)'%basis)
    if var=='V5':   # Rime-oog: Rime-linkeroog -> ver (x29-31), Rime-rechteroog -> nabij (binnen de ring)
        for y in range(17,21):                 # Rime-rijen 17-20 (rij 16 = hoedschaduw)
            for x in range(29,32):             # Rime x23-25 (middelste 3 van het verre oog x22-26)
                v=RIME[y,x-6]
                if v in K_RIME: zet(y,x,K_RIME[v],'Rime-oog ver')
            for x in range(37,42):             # Rime x30-34 (nabije oog)
                v=RIME[y,x-7]
                if (y,x) in BIN and v in K_RIME: zet(y,x,K_RIME[v],'Rime-oog nabij')
    if var in ('V2','V5'):
        for (y,x) in LID_VER: zet(y,x,0,'Hitmonchan-lid ver')
        for (y,x) in LID_NAB:
            if (y,x) in BIN: zet(y,x,0,'Hitmonchan-lid nabij')
    # neus terug (r3): wit bolletje + modelselout 112
    for (y,x) in ((20,33),(20,34)): zet(y,x,7,'neus wit')
    for (y,x) in ((19,33),(19,34),(20,32),(20,35)): zet(y,x,4,'neus selout 112')
    return C
if __name__=='__main__':
    for v in P: print(v, P[v])
    print('R1',sorted(ring_magn())); print('R2',sorted(ring_model()))
