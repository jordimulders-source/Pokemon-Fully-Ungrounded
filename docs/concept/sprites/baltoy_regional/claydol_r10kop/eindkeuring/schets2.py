# Eindkeuring, SCHETS 2: één radiaal lichtveld over hals+romp+onderlijf (gebogen grenzen die over de naden doorlopen),
# slagschaduw van de kop schuin, armen/voeten eigen kap in hetzelfde licht. Alleen hulp voor het tekstraster in eind.py.
import os,sys,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
for p in ('../r6','..','../r2','../r3','../r5'): sys.path.insert(0,os.path.join(H,p))
from schets import delen, VAST6
yy,xx=np.mgrid[0:64,0:64]; X=xx+0.5; Y=yy+0.5
R6=np.array(Image.open(os.path.join(H,'../r6/claydol_r10kop_r6.png'))).astype(int)
PAL=Image.open(os.path.join(H,'../r6/claydol_r10kop_r6.png')).getpalette()
def afst(cx,cy,sx,sy): return np.sqrt(((X-cx)/sx)**2+((Y-cy)/sy)**2)
def schets(P):
    D=delen(); S=R6.copy()
    r=afst(*P['c'])
    for k,(c,gr) in P['loc'].items():
        m=D==k; rr=afst(*c); r=np.where(m, np.minimum(r+P['lokplus'], rr) if k in P.get('eigen',()) else r, r)
    T=np.select([r<gr_ for gr_,_ in P['gr']],[t for _,t in P['gr']],P['rest'])
    # slagschaduw kop
    ys=P['sa']+P['sb']*np.clip((X-P['sx0'])/P['sw'],0,1)**P['sp']
    d=ys-Y
    sch=(d>0)
    T=np.where(sch&(T==2),5,T); T=np.where(sch&(T==3),5,T)
    T=np.where(sch&(d>P['diep'])&(T==5),10,T)
    for k in ('hals','romp','armL','armR','voetL','voetR'):
        m=D==k; S[m]=T[m]
    return S,D
P=dict(c=(25.5,45.5,1.0,0.9), gr=[(4.2,2),(9.5,3),(13.5,5),(17.5,10)], rest=6,
       loc={}, sa=41.2, sb=6.0, sx0=23, sw=17, sp=1.2, diep=1.6, lokplus=0)
def toon(S,D):
    for y in range(38,62):
        print('%2d '%y+''.join(('%X'%S[y,x] if S[y,x] else '.') for x in range(12,53)))
def save(S,pad,z=8):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad,transparency=0)
if __name__=='__main__':
    S,D=schets(P); toon(S,D); save(S,'/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/81de79ab-6056-55f3-b3d2-5fcd03808eb6/scratchpad/s2.png')

def schets3():
    S,D=schets(dict(P,gr=[(4.2,2),(9.5,3),(13.5,5),(18.5,10)]))
    # eigen kappen: (middelpunt, schaal, drempels) in hetzelfde licht linksboven
    caps={'armL':((16.0,44.8,1,1),[(2.2,2),(4.6,3),(6.5,5)],10),
          'armR':((43.0,44.6,1.1,1),[(1.6,3),(4.2,5),(7.2,10)],6),
          'voetL':((24.5,55.2,1.2,1),[(2.5,3),(5.5,5)],10),
          'voetR':((32.5,55.4,1.3,1),[(2.4,3),(5.5,5),(8.5,10)],6)}
    for k,(c,gr,rest) in caps.items():
        r=afst(*c); T=np.select([r<g for g,_ in gr],[t for _,t in gr],rest)
        m=D==k; S[m]=T[m]
    # hand (rechts, achter de plooi x 47-49): eigen kleine kap
    r=afst(47.2,47.6,1,1); T=np.select([r<1.6,r<3.2],[5,10],6)
    m=(D=='armR')&(xx>=46)&(yy>=47); S[m]=T[m]
    # slagschaduw kop op de bovenkant van de armen
    for k in ('armL','armR'):
        m=(D==k)&(yy<=42); S[m]=np.where(S[m]<=3,5,np.where(S[m]==5,10,S[m]))
    return S,D

def rand(S):
    """lijfpixels op de buitenrand (grenzen aan transparant) die geen lijn zijn: lichte tint -> selout 5"""
    a=S>0; out=[]
    for y in range(40,62):
        for x in range(12,53):
            if not a[y,x] or S[y,x] in (7,6,8,9): continue
            nb=[a[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
            if not all(nb) and S[y,x] in (1,2,3): out.append((x,y))
    return out
def schets4():
    S,D=schets(dict(P,gr=[(4.2,2),(9.5,3),(13.5,5),(18.5,10)]))
    S3,_=schets3()
    for k in ('armL','armR'):
        m=D==k; S[m]=S3[m]
    m=(D=='hals')&(yy==42)&(S==2); S[m]=3
    for x,y in rand(S):
        if D[y,x]: S[y,x]=5
    return S,D

def clusters(S,mask):
    from collections import deque
    seen=np.zeros_like(mask); res=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        t=S[y,x]; q=deque([(y,x)]); seen[y,x]=True; comp=[]
        while q:
            cy,cx=q.popleft(); comp.append((cx,cy))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if mask[ny,nx] and not seen[ny,nx] and S[ny,nx]==t: seen[ny,nx]=True; q.append((ny,nx))
        if len(comp)<3: res.append((t,comp))
    return res

def schets5(agr=19.5):
    S,D=schets(dict(P,gr=[(4.2,2),(9.5,3),(13.5,5),(agr,10)]))
    S3,_=schets3()
    for k in ('armL','armR'):
        m=D==k; S[m]=S3[m]
    m=(D=='hals')&(yy==42)&(S==2); S[m]=3
    for x,y in rand(S):
        if D[y,x]: S[y,x]=5
    for x,y in ((21,51),(21,52),(22,54)): S[y,x]=10
    S[43,41]=3
    for x in range(26,30): S[57,x]=10
    return S,D
