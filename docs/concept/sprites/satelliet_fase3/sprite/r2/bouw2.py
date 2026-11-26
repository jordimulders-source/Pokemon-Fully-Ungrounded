# r2 ruimtestation: elk onderdeel opnieuw opgebouwd uit op het model GEMETEN geometrie
# (bolmiddelpunten/stralen, buisassen/stralen, band- en kraagposities langs de as, paneelhoeken),
# zodat contouren recht en bollen rond zijn. Getallen in modelpixels (model_gekozen.png).
import os, json
import numpy as np
from PIL import Image
from common import load
import kaal
a,bg=load(); H,W=bg.shape
ys,xs=np.where(~bg); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
OUTW=64; s=(X1-X0)/OUTW; OH=int(np.ceil((Y1-Y0)/s))
SY,SX=np.mgrid[0:OH,0:OUTW]; MX=X0+(SX+0.5)*s; MY=Y0+(SY+0.5)*s
LIJN=int(os.environ.get('LIJN','11')); CEL=int(os.environ.get('CEL','3')); PRAND=int(os.environ.get('PRAND','2'))
# ---- metingen (fit.py / fit2.py: cirkelfit op de modelrand; meet.py: buisprofielen; banden.py: bandvormen)
BOL={'voor':((62.1,128.0),20.6),'ver':((182.0,36.1),14.8),'oogL':((74.9,64.7),11.2),'oogR':((189.0,91.0),11.2)}
def asvec(o,q):
    d=np.array(q)-np.array(o); L=np.hypot(*d); u=d/L; n=np.array([-u[1],u[0]]); n=n if n[1]>0 else -n; return np.array(o),u,n
LANG=asvec((62.1,128.0),(182.0,36.1)); ZIJ=asvec((74.9,64.7),(189.0,91.0))
# hub = snijpunt van de assen
_A=np.array([LANG[1],-ZIJ[1]]).T; _ts=np.linalg.solve(_A,ZIJ[0]-LANG[0]); HUBC=LANG[0]+LANG[1]*_ts[0]
BOL['hub']=((HUBC[0],HUBC[1]),20.5)
# buisstraal en -verschuiving langs de as (gemeten met meet.py)
def lang_rw(t): f=np.clip((t-38)/78,0,1.3); return 15-1.5*f, 2.0*f
def zij_rw(t): f=np.clip((t-24)/66,0,1.3); return 8+1.5*f, 0.5*f
BAND=json.load(open('banden.json'))
# bijgesteld waar de fit slecht was (maxres > 2): zelfde boogsoort als de buren
BAND['hubkraag_achter']=['lang',[93.5,0.0,10.0],4.0,'P',16]
BAND['hubkraag_voor']=['lang',[72.0,0.0,-2.0],4.5,'P',17]   # fit trok de onderste ring mee; gemeten (113,77),(120,88): t~70-71
BAND['hubkraag_links']=['zij',[48.0,0.0,-12.0],3.5,'P',11]
BAND['rechtskraag']=['zij',[110.0,0.0,-9.9],5.0,'P',11]
KRAAG=1.5
# paarse kragen minstens 5 modelpx breed (~1,4 spritepx), anders vallen ze op 64 px weg
for _k,_b in BAND.items():
    if _b[3]=='P': _b[2]=max(_b[2],5.0)
# donkere ring tussen bol en paarse kraag (model: profiel t=20 en s~104 navy/lavendel)
_v=BAND['voorkraag']; BAND['voorkraag_n']=['lang',[_v[1][0]-4.5,_v[1][1],_v[1][2]],5.5,'N',17]
BAND['rechtskraag_n']=['zij',[114.4,0.0,-9.9],4.0,'N',11]
GEO={'PA':((86,24),(137,40),(71,36),4),'PC':((176,58),(227,72),(163,70),4),'PD':((20,86),(61,101),(3,96),4),
     'PF':((123,100),(123,136),(133,104),3),'PE':((102,117),(149,134),(88,132),4),'PB':((123,3),(123,50),(132,8),3)}
# ---- tekenen: id-kaart + kleur, achter -> voor
ID=np.zeros((OH,OUTW),int); COL=np.zeros((OH,OUTW),int); names=['achtergrond']
def paint(name,mask,col):
    names.append(name); i=len(names)-1; ID[mask]=i; COL[mask]=col[mask] if isinstance(col,np.ndarray) else col
def uv(k):
    T,R,L,n=GEO[k]; T,R,L=map(np.array,(T,R,L)); M=np.array([R-T,L-T]).T.astype(float); inv=np.linalg.inv(M)
    d=np.stack([MX-T[0],MY-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
def paneel(k):
    T,R,L,n=GEO[k]; u,v=uv(k)
    vmax=1.06 if k not in ('PB','PF') else 1.28   # PB: licht zijvlak (model x131-134)
    m=(u>=0)&(u<=1)&(v>=0)&(v<=vmax)
    col=np.full((OH,OUTW),CEL)
    du_dx=(uv_at(k,MX+s,MY)[0]-u); du_dy=(uv_at(k,MX,MY+s)[0]-u); gn=np.hypot(du_dx,du_dy)
    lim=0.5*np.maximum(np.abs(du_dx),np.abs(du_dy))/gn
    for j in range(1,n): col[np.abs(u-j/n)/gn<=lim]=LIJN
    if k in ('PB','PF'): col[v>1.0]=5
    paint(k,m,col)
def uv_at(k,px,py):
    T,R,L,n=GEO[k]; T,R,L=map(np.array,(T,R,L)); M=np.array([R-T,L-T]).T.astype(float); inv=np.linalg.inv(M)
    d=np.stack([px-T[0],py-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
LICHT=np.array([-0.55,-0.65,0.52]); LICHT/=np.linalg.norm(LICHT)
def bol(k):
    (cx,cy),r=BOL[k]; dx=(MX-cx)/r; dy=(MY-cy)/r; q=dx*dx+dy*dy; m=q<=1.0
    nz=np.sqrt(np.clip(1-q,0,1)); d=dx*LICHT[0]+dy*LICHT[1]+nz*LICHT[2]
    col=np.where(d>0.88,15,np.where(d>0.62,14,np.where(d>0.30,13,12)))
    paint('bol_'+k,m,col)
def coords(A):
    o,u,n=A; t=(MX-o[0])*u[0]+(MY-o[1])*u[1]; w=(MX-o[0])*n[0]+(MY-o[1])*n[1]; return t,w
def bandmask(nm,extra=0.0):
    asn,(a0,b0,c0),br,so,r=BAND[nm]; A=LANG if asn=='lang' else ZIJ; t,w=coords(A)
    rw=lang_rw if asn=='lang' else zij_rw; rr,off=rw(t); rr=rr+(KRAAG if so=='P' else 0)
    ww=w-off; q=np.clip(np.abs(ww)/rr,0,1); tc=a0+b0*ww+c0*np.sqrt(1-q*q)
    return (np.abs(ww)<=rr)&(np.abs(t-tc)<=br/2+extra), tc, ww/rr
def tc_of(nm):
    m,tc,wn=bandmask(nm); return tc
def buis(naam,A,rw,van,tot,banden,tonen):
    t,w=coords(A); rr,off=rw(t); ww=w-off; wn=ww/rr
    tv=tc_of(van)-BAND[van][2]/2; tt=tc_of(tot)+BAND[tot][2]/2
    m=(np.abs(ww)<=rr)&(t>=tv)&(t<=tt)
    col=tonen(wn)
    for b in banden:
        bm,tc,bwn=bandmask(b)
        if BAND[b][3]=='P': bc=np.where(bwn<0.2,8,np.where(bwn<0.5,7,6))
        else: bc=np.full((OH,OUTW),2)
        m=m|bm; col=np.where(bm,bc,col)
    paint('buis_'+naam,m,col)
def kragen(naam,banden):
    m=np.zeros((OH,OUTW),bool); col=np.zeros((OH,OUTW),int)
    for b in banden:
        bm,tc,bwn=bandmask(b); bc=np.where(bwn<0.2,8,np.where(bwn<0.5,7,6)); m|=bm; col=np.where(bm,bc,col)
    paint('kraag_'+naam,m,col)
TON_LANG=lambda wn: np.where(wn<0.03,15,np.where(wn<0.6,14,12))
TON_ZIJ=lambda wn: np.where(wn<-0.6,14,np.where(wn<-0.1,15,np.where(wn<0.3,14,12)))
def ring(name,c,rx,ry,gat=None,col=7):
    dx=(MX-c[0])/rx; dy=(MY-c[1])/ry; m=dx*dx+dy*dy<=1
    cc=np.where(dy<-0.2,8,np.where(dy<0.4,7,6))
    if gat: gx=(MX-c[0])/gat[0]; gy=(MY-c[1]-0.6)/gat[1]; cc=np.where(gx*gx+gy*gy<=1,2,cc)
    paint(name,m,cc)
def staaf(name,p0,p1,breed,col):
    p0=np.array(p0,float); p1=np.array(p1,float); d=p1-p0; L=np.hypot(*d); d/=L
    t=(MX-p0[0])*d[0]+(MY-p0[1])*d[1]; w=np.abs((MX-p0[0])*d[1]-(MY-p0[1])*d[0])
    paint(name,(t>=0)&(t<=L)&(w<=breed/2),col)
for k in ('PC','PA','PB','PD','PF','PE'): paneel(k)
staaf('stang_PD',(50,107),(68,103),2.4,5)
staaf('mastvoet_staaf',(128.5,50),(128.5,58),2.4,5)
bol('ver'); buis('achter',LANG,lang_rw,'hubkraag_achter','verkraag',['achterband','verkraag'],TON_LANG)
bol('oogL'); buis('links',ZIJ,zij_rw,'linkskraag','hubkraag_links',['linkskraag'],TON_ZIJ)
buis('rechts',ZIJ,zij_rw,'hubkraag_rechts','rechtskraag_n',['rechtskraag','rechtskraag_n'],TON_ZIJ); bol('oogR')
bol('hub')
kragen('hub',['hubkraag_achter','hubkraag_links','hubkraag_rechts'])
ring('ring_boven',(128.5,58.5),8.5,3.6,gat=(3.2,1.3))
staaf('mastvoet_staaf2',(128.5,50),(128.5,56),2.4,5)
ring('ring_onder',(128.0,97.5),7.5,3.0)
bol('voor'); buis('voor',LANG,lang_rw,'voorkraag_n','hubkraag_voor',['voorkraag_n','voorkraag','voorband','hubkraag_voor'],TON_LANG)
# ---- buitenlijnen: rand van elk onderdeel tegen achtergrond of tegen wat erachter ligt
DONKER={2,1}
out=COL.copy()
for y in range(OH):
    for x in range(OUTW):
        i=ID[y,x]
        if i==0: continue
        nbs=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
        rand=[]
        for yy,xx in nbs:
            j=ID[yy,xx] if (0<=yy<OH and 0<=xx<OUTW) else 0
            if j<i and not (names[i].startswith('buis') and names[j].startswith('bol') and False): rand.append((yy,xx,j))
        if not rand: continue
        nm=names[i]
        if nm.startswith('stang') or nm.startswith('mastvoet'): continue
        if nm.startswith('P'):
            schaduw=any(yy>y or xx>x for yy,xx,j in rand)
            out[y,x]=1 if (schaduw or PRAND==1) else 2
            if COL[y,x]==5 and nm in ('PB','PF') and not any(j==0 and xx>x for yy,xx,j in rand): out[y,x]=5
            continue
        if nm.startswith('ring'): out[y,x]=6 if any(yy>y for yy,xx,j in rand) else COL[y,x]; continue
        tegen_bg=any(j==0 for yy,xx,j in rand)
        schaduw=any((yy>y or xx>x) for yy,xx,j in rand)
        if COL[y,x] in (6,7,8): out[y,x]=6 if schaduw else 7 if not tegen_bg else 6
        else: out[y,x]=1 if (schaduw and tegen_bg) else 2
spr=out.copy()
# ---- ogen (r1, goedgekeurd door coordinator)
EYE=["..887..",".8999a6","89aaaa6","7a22aa6","7a22aa6",".6aaa6.","..666.."]
for j,r in enumerate(EYE):
    for i,ch in enumerate(r):
        if ch!='.': spr[33+j,12+i]=int(ch,16)
def klein(x0,y0):
    p={(x0+1,y0):8,(x0+2,y0):7,(x0,y0+1):8,(x0+3,y0+1):6,(x0,y0+2):7,(x0+3,y0+2):6,(x0+1,y0+3):6,(x0+2,y0+3):6,
       (x0+1,y0+1):9,(x0+2,y0+1):10,(x0+1,y0+2):2,(x0+2,y0+2):10}
    for (x,y),c in p.items(): spr[y,x]=c
klein(17,16); klein(50,24)
np.save('id.npy',ID); json.dump(names,open('names.json','w'))
def dump(path,A):
    with open(path,'w') as f:
        for y in range(OH): f.write(''.join('.' if A[y,x]==0 else '0123456789abcdef'[A[y,x]] for x in range(OUTW))+'\n')
if __name__=='__main__':
    dump('sprite.txt',spr); kaal.save(spr.astype(np.uint8),'sprite.png')
    # silhouet t.o.v. model (alpha >= 0.5)
    Wx=kaal.overlap(OUTW,X0,s,W); Wy=kaal.overlap(OH,Y0,s,H); al=(Wy@(~bg).astype(float)@Wx.T/(s*s))>=0.5
    sp=spr>0; print('silhouet: alleen sprite',int((sp&~al).sum()),'alleen model',int((al&~sp).sum()),'sprite px',int(sp.sum()),'model px',int(al.sum()))
    np.save('alpha_model.npy',al)
