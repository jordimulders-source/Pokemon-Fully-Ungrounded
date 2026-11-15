# c8: c7 A (kop A bevroren) + een gegraveerde cirkel rechts van het nabije oog (Jordi: "moet alleen nog een soort cirkel
# rechts van het oog"). Kerfstijl: groef 2, lichte lip (5 op vlak 3/4, 14 op 5) direct onder/rechts van de groef,
# geen lip tussen groeven op 1 px. Alleen de cirkelzone verandert (diff 0 elders).
import numpy as np
from PIL import Image
from basis import bevroren_kop
F=bevroren_kop()
A=np.array(Image.open('../c7/welp_c7_a.png'))
PAL=Image.open('../c7/welp_c7_a.png').getpalette()[:48]; PALG=Image.open('../c7/welp_c7_a_grijs.png').getpalette()[:48]
RING4=[(1,0),(2,0),(0,1),(3,1),(0,2),(3,2),(1,3),(2,3)]          # 4x4 ring
RING3=[(1,0),(0,1),(2,1),(1,2)]                                   # 3x3 ruit-ring (plus-vormig)
RING5=[(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),(1,4),(2,4),(3,4)]
VAR={ # naam: (vorm, x0, y0)
 '1': (RING4,24,26),   # 4 px, op ooghoogte, vlak achter het oog
 '2': (RING4,24,28),   # 4 px, iets lager (wang)
 '3': (RING3,24,24),   # 3 px, iets hoger (slaap, onder het oor)
}
def maak(v):
    vorm,x0,y0=VAR[v]; a=A.copy(); G=np.zeros(a.shape,bool)
    for dx,dy in vorm:
        x,y=x0+dx,y0+dy; assert not F[y,x] and A[y,x] in (3,4,5), (x,y,A[y,x]); G[y,x]=True; a[y,x]=2
    for dx,dy in vorm:
        for ex,ey in ((0,1),(1,0)):
            X,Y=x0+dx+ex,y0+dy+ey
            if G[Y,X] or F[Y,X] or A[Y,X] not in (3,4,5): continue
            if G[min(Y+ey,63),min(X+ex,63)]: continue
            a[Y,X]=14 if A[Y,X]==5 else 5
    return a
def bewaar(a,naam,pal):
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal+[0]*(768-48)); im.save(naam+'.png',transparency=0)
    r=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    for v in VAR:
        a=maak(v); bewaar(a,'welp_c8_'+v,PAL); bewaar(a,'welp_c8_'+v+'_grijs',PALG)
        d=np.argwhere(a!=A); print(v,'gewijzigd',len(d),'zone x',d[:,1].min(),'-',d[:,1].max(),'y',d[:,0].min(),'-',d[:,0].max())
