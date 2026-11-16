# Stap 2 (Jordi: "kan jij de onderdelen dan groter maken zelf?"): alleen in de middenzone kleine onderdelen
# (ketting, losse boutjes, plaatjes) samenvoegen met het grootste aangrenzende stuk. Niets getekend:
# elke pixel krijgt de modelkleur van het dichtstbijzijnde overblijvende modelstuk; lijnen blijven alleen
# waar ze twee overblijvende stukken (of stuk en achtergrond) scheiden.
import sys; from PIL import Image; import numpy as np; from collections import deque
import os; ANY=os.environ.get('ANY')=='1'
CORE=int(sys.argv[3]) if len(sys.argv)>3 else 30
T=int(sys.argv[1]) if len(sys.argv)>1 else 60
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
H,W=a.shape[:2]; fg=a.min(2)<225
L=a@[0.3,0.59,0.11]; line=fg&(L<40); sat=a[...,0]-a[...,2]
grp=np.where(sat>22,1,2); grp[~fg]=0; grp[line]=3          # 1 bruin, 2 staal, 3 lijn
# middenzone (natieve coordinaten), buiten: schoorsteen, wiel, rail blijven model
yy,xx=np.mgrid[0:H,0:W]
wiel=((xx-134.5)**2/24**2+(yy-115)**2/32**2)<=1
schoor=((xx-79)**2/22**2+(yy-62)**2/18**2)<=1          # mond
schoor|=(yy>=60)&(yy<=118)&(xx>=80+(yy-80)*0.37)&(xx<=98+(yy-80)*0.15)   # pijp (schuin)
rail=(xx<=66)&(yy>=112)
bout=((xx>=60)&(xx<=74)&(yy>=99)&(yy<=114))|((xx>=119)&(xx<=130)&(yy>=73)&(yy<=85))|((xx>=57)&(xx<=67)&(yy>=131)&(yy<=141))
mid=fg&~wiel&~schoor&~rail&~bout&(yy<=150)
np.save('zones.npy',np.stack([wiel,schoor,rail,mid]))
def lab4(m):
    lab=np.zeros(m.shape,int); n=0
    for y in range(H):
        for x in range(W):
            if m[y,x] and not lab[y,x]:
                n+=1; q=[(y,x)]; lab[y,x]=n
                while q:
                    cy,cx=q.pop()
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and not lab[ny,nx] and (ANY or grp[ny,nx]==grp[cy,cx]): lab[ny,nx]=n; q.append((ny,nx))
    return lab,n
lab,n=lab4(fg&~line)
MERGED=[]; KET=[]
size=np.bincount(lab.ravel(),minlength=n+1)
# overblijvend: groot genoeg, of (deels) buiten de middenzone
keep=np.zeros(n+1,bool)
for k in range(1,n+1):
    m=lab==k
    pm=np.pad(m,1); core=m.copy()
    for dy in (-1,0,1):
        for dx in (-1,0,1): core&=pm[1+dy:1+dy+H,1+dx:1+dx+W]
    if (size[k]>=T and core.sum()>=CORE) or (m&~mid).sum()>size[k]*0.5: keep[k]=True
surv=keep[lab]&(lab>0)
# kleine stukjes van dezelfde kleurgroep die vlak bij elkaar liggen (alleen een lijn ertussen) = samen één groter stuk
T2=int(sys.argv[2]) if len(sys.argv)>2 else 40
small=mid&(lab>0)&~keep[lab]
for g in (1,2):
    sm=small&(grp==g); dil=sm.copy()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        sh=np.roll(sm,(dy,dx),(0,1)); dil|=sh&line&mid
    m2=np.zeros((H,W),int); nn=0
    for y,x in zip(*np.where(dil)):
        if m2[y,x]: continue
        nn+=1; q=[(y,x)]; m2[y,x]=nn
        while q:
            cy,cx=q.pop()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=cy+dy,cx+dx
                if 0<=ny<H and 0<=nx<W and dil[ny,nx] and not m2[ny,nx]: m2[ny,nx]=nn; q.append((ny,nx))
    for k in range(1,nn+1):
        cm=(m2==k)&sm
        if cm.sum()>=T2:
            n+=1; lab[(m2==k)]=n; keep=np.append(keep,True); surv|=cm
            # lijnen binnen het samengevoegde stuk worden later gevuld (eigenaar = dit stuk)
            line_in=(m2==k)&line; MERGED.append(line_in); KET.append(m2==k)

# BFS: elke voorgrondpixel -> dichtstbijzijnde overblijvende pixel (bron)
src=-np.ones((H,W,2),int); dist=np.full((H,W),999); q=deque()
for y,x in zip(*np.where(surv)): src[y,x]=(y,x); dist[y,x]=0; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 0<=ny<H and 0<=nx<W and fg[ny,nx] and dist[ny,nx]>dist[y,x]+1:
            dist[ny,nx]=dist[y,x]+1; src[ny,nx]=src[y,x]; q.append((ny,nx))
INL=np.zeros((H,W),bool)
for mm in MERGED: INL|=mm
out=a.copy(); owner=np.where(surv,lab,0)
own=np.zeros((H,W),int)
for y,x in zip(*np.where(fg)):
    sy,sx=src[y,x]
    if sy>=0: own[y,x]=lab[sy,sx]
ch=0
for y,x in zip(*np.where(mid&(~surv|INL))):
    sy,sx=src[y,x]
    if sy<0: continue
    if line[y,x]:
        # lijn blijft als hij aan de rand ligt of twee verschillende stukken scheidt
        nb=[own[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W]
        edge=any(not fg[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W)
        if edge or (len(set(nb)-{own[y,x]})>0 and not INL[y,x]): continue
    out[y,x]=a[sy,sx]; ch+=1
print('stukken',n,'overblijvend',keep.sum(),'omgezette natieve px',ch)
Image.fromarray(out.astype(np.uint8)).save('natief_samen.png')
K=np.zeros((H,W),bool)
for kk in KET: K|=kk
np.save('ketting.npy',K); print('samengevoegde massa natief px',K.sum())
ys,xs=np.where(fg); c=(xs.min()-1,ys.min()-1,xs.max()+2,ys.max()+2)
A=Image.open('natief.png').crop(c); B=Image.fromarray(out.astype(np.uint8)).crop(c)
V=Image.new('RGB',(A.width*2+4,A.height),'white'); V.paste(A,(0,0)); V.paste(B,(A.width+4,0))
V.resize((V.width*5,V.height*5),Image.NEAREST).save('samen_5x.png')
