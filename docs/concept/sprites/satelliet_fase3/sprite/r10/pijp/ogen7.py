# r7: oogreparaties per bolvariant, afgeleid uit het (vergrote) model i.p.v. met de hand geplaatst.
# Zelfde regel als r4 (ring + iris + pupil, geen wit binnen de ring, modelkleuren):
#  - oogzone in het model = cirkel rond het irismiddelpunt met straal 1,6 x irisstraal (gemeten ringbuitenrand r13b: 11/6,8)
#  - per spritepixel binnen die zone (middelpunt <= R/s): klasse = grootste modeldekking van ring (paars 6/7/8) / iris (teal) / pupil
#    (donker binnen 0,75 x irisstraal); wit/bolkleur telt niet mee -> geen wit in de ring
#  - tint = grootste dekking binnen de klasse (ring 6/7/8, iris 9/A, pupil navy 2)
import numpy as np, kaal
from common import load, VAR
a,bg=load(); s=3.515625; H,W=bg.shape
pal=np.array(kaal.PAL[1:],float)
lab=((a[:,:,None,:].astype(float)-pal[None,None])**2).sum(3).argmin(2)+1; lab[bg]=0
Y,X=np.mgrid[0:H,0:W]
teal=(a[:,:,1]>a[:,:,0]+25)&(a[:,:,2]>a[:,:,0]+20)&~bg
dark=(a.sum(2)<180)&~bg
BOX={'voor':(X<110)&(Y>100),'links':(X<110)&(Y<=100),'rechts':(X>=150)}
OH=kaal.reduce()[0].shape[0]
Wx=kaal.overlap(64,3,s,W); Wy=kaal.overlap(OH,3,s,H)
def cov(m): return Wy@m.astype(float)@Wx.T/(s*s)
INFO={}; ZONE={}; PUPC={}; NONBG=None
def bereken():
    out={}
    for nm,bx in BOX.items():
        t=teal&bx; cy,cx=Y[t].mean()+.5,X[t].mean()+.5; r=np.sqrt(t.sum()/np.pi)
        d=np.hypot(X+.5-cx,Y+.5-cy); R=1.6*r
        pup=dark&(d<=0.75*r)
        ring=np.isin(lab,(6,7,8))&(d<=R+1)
        iris=teal&~pup
        C={'ring':cov(ring),'iris':cov(iris),'pup':cov(pup)}
        T={c:cov((lab==c)&ring) for c in (6,7,8)}; T.update({c:cov((lab==c)&iris) for c in (9,10)})
        scx,scy=(cx-3)/s,(cy-3)/s; sR=R/s
        px=[]
        for y in range(OH):
            for x in range(64):
                if np.hypot(x+.5-scx,y+.5-scy)>sR: continue
                k=max(C,key=lambda q:C[q][y,x])
                if C[k][y,x]<0.08: continue
                if k=='pup': c=2
                elif k=='ring': c=max((6,7,8),key=lambda q:T[q][y,x])
                else: c=max((9,10),key=lambda q:T[q][y,x])
                px.append((x,y,c))
        ZONE[nm]=(scx,scy,sR); PUPC[nm]=C['pup']
        out[nm]=px; INFO[nm]=dict(model_c=(round(cx,1),round(cy,1)),iris_r=round(r,2),ring_R=round(R,2),sprite_c=(round(scx,2),round(scy+13,2)),sprite_R=round(sR,2))
    return out
OGEN={VAR:bereken()} if VAR!='100' else {}
NONBG=cov(~bg)
STAAF={'120':[],'130':[]}
# handreparaties na de algemene oogregels (x, y in de uitsnede = spritey-13, kleur), zelfde soort als r4 OGEN 'rechts':
# 130 rechteroog: iris lag 4 breed tegen de bolrand (las als teal blok) -> ring links (8 licht boven, 7 midden) en
#   ring boven gesloten (51,24: iris 9 -> ring 8); iris 3 breed met pupil op de modelplek.
# 120/130 linkeroog: (19,30) viel op ring (modeldekking ring > iris) -> iris kleiner dan r6 (2+1 px); terug naar iris A zoals r6 (2x2 binnen de ring)
EXTRA={'120':[('links',19,17,10)],'130':[('rechts',49,25,8),('rechts',49,26,7),('rechts',51,24,8),('links',19,17,10)]}
if __name__=='__main__':
    for k,v in INFO.items(): print(k,v,len(OGEN[VAR][k]))
