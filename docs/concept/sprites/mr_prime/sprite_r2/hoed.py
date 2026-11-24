# Hoed + haarvleugels uit Mr. Rime's eigen front.png (graphics/pokemon/mr_rime/front.png), omgekleurd naar grijs,
# alleen verschoven/gespiegeld (niets getekend). Rime-index -> toon: 3,1 -> 0 (zwart), 4 -> 1 (48), 2 -> 3 (80).
import numpy as np; from PIL import Image
R=np.asarray(Image.open('../../../../../graphics/pokemon/mr_rime/front.png')).astype(int)
MAP={3:0,1:0,4:1,2:3}
DY=-2  # r2: hoed + vleugels als geheel 2 rijen hoger (voorhoofd uit het model eronder)
ZIJHAAR=False  # Rime-haar langs de achterkant van de kop: maakte de rechterkant van het gezicht zwart, uit
DX=7  # Rime-kop -> Prime-kop: Rime-rand x19-44 valt dan precies op de r9-rand x26-51; rijen 1-op-1 (zelfde verschuiving als de ogen)
def laag(cond):
    L={}
    for y in range(64):
        for x in range(64):
            if R[y,x] in MAP and cond(y,x): L[(y,x)]=MAP[R[y,x]]
    return L
kroon = laag(lambda y,x: 6<=y<=15 and 19<=x<=44)   # bol + rand (Rime-schaduwrij 16 op het gezicht niet: daar zitten de ogen)
lvleugel = laag(lambda y,x: 9<=y<=21 and 6<=x<=18 or (12<=y<=21 and 19<=x<=23 and y>=16))
rvleugel = laag(lambda y,x: 3<=y<=14 and 45<=x<=57)
zijhaar  = laag(lambda y,x: 17<=y<=23 and 38<=x<=44)
def plak(C,L,dx,dy=0,spiegel=None,achter=False,log=None,naam=''):
    for (y,x),v in L.items():
        xx=(spiegel-x if spiegel is not None else x)+dx; yy=y+dy
        if 0<=xx<64 and 0<=yy<64 and (not achter or C[yy,xx]==-1):
            if log is not None and C[yy,xx]!=v: log[naam]=log.get(naam,0)+1
            C[yy,xx]=v
def variant(C,v,log):
    C=C.copy()
    if v=='A':   # beide vleugels zoals Mr. Rime; linker (verre) vleugel 4 px verder naar achteren, achter kop/hoed
        plak(C,lvleugel,DX+4,dy=DY,achter=True,log=log,naam='Rime linkervleugel (+4 naar achter)')
        plak(C,rvleugel,DX,dy=DY,achter=True,log=log,naam='Rime rechtervleugel')
    elif v=='B': # vleugels plat naar achteren: rechtervleugel zoals Rime, linkervleugel gespiegeld eronder
        plak(C,rvleugel,DX,dy=DY,achter=True,log=log,naam='Rime rechtervleugel')
        plak(C,lvleugel,DX,dy=3+DY,spiegel=63,achter=True,log=log,naam='Rime linkervleugel gespiegeld naar achter')
    if ZIJHAAR: plak(C,zijhaar,DX,dy=DY,log=log,naam='Rime zijhaar (achterkant kop)')
    plak(C,kroon,DX,dy=DY,log=log,naam='Rime hoed (bol+rand)')
    return C
if __name__=='__main__':
    import sys; from toon import rgb
    C=np.load('basis.npy'); out=[]
    for v in 'AB':
        log={}; out.append(variant(C,v,log)); print(v,log)
    W=Image.new('RGB',(512*2+10,512),(255,255,255))
    for i,c in enumerate(out): W.paste(Image.fromarray(rgb(c)).resize((512,512),0),(i*522,0))
    W.save(sys.argv[1])
