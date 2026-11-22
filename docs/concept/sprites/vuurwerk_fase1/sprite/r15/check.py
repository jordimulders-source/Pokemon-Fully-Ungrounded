# Controle per bestand: kleuren (incl. transparant), open buitenrand, losse pixels, tintvlakjes <3 px; diff t.o.v. basis per zone.
import numpy as np, sys
from collections import deque, Counter
from PIL import Image
sys.path.insert(0,'../r10'); from txt import CH
CH2='.#Ddsml'+'rMpYSckbw'
def check(fn):
    im=Image.open(fn); a=np.array(im); H,W=a.shape
    print('==',fn,im.mode,'transparency',im.info.get('transparency'))
    used=Counter(CH2[x] for x in a.flatten() if x)
    print(' kleuren incl. transparant:',len(used)+1, dict(used))
    openr=[];los=[]
    for y in range(H):
        for x in range(W):
            if not a[y,x]: continue
            nb4=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
            edge=any(not(0<=yy<H and 0<=xx<W) or a[yy,xx]==0 for yy,xx in nb4)
            if edge and CH2[a[y,x]] not in '#dbD': openr.append((y,x,CH2[a[y,x]]))
            n8=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
            if all(a[p]==0 for p in n8): los.append((y,x))
    seen=np.zeros_like(a,bool); klein=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or seen[y,x]: continue
            c=a[y,x]; q=deque([(y,x)]); seen[y,x]=1; comp=[]
            while q:
                cy,cx=q.popleft(); comp.append((cy,cx))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and a[ny,nx]==c: seen[ny,nx]=1; q.append((ny,nx))
            if len(comp)<3 and CH2[c] not in 'w#dbD': klein.append((CH2[c],comp))
    print(' open rand',openr,'\n los',los)
    print(' tintvlakjes <3 px:',len(klein),klein)
    return a
def diff(f1,f2,zone=None):
    a=np.array(Image.open(f1)); b=np.array(Image.open(f2)); d=list(zip(*np.nonzero(a!=b)))
    d=[(int(r),int(c)) for r,c in d]
    buiten=[p for p in d if zone and not zone(*p)]
    print(' diff %s -> %s: %d px; buiten zone: %d %s'%(f1,f2,len(d),len(buiten),buiten if buiten else ''))
    return d
if __name__=='__main__':
    check('sprite.png')
    hand=lambda r,c: 15<=r<=20 and (18<=c<=24 or 28<=c<=33)
    diff('../r11/sprite.png','stap1.png',hand)
    # stap 2: alleen lint (rij>=21, niet pijl), kieuwen/sprieten (rij 2-21, kol 30-50) mogen wijzigen
    gill=lambda r,c: (2<=r<=8 and 30<=c<=36) or (12<=r<=21 and 42<=c<=50)
    lintz=lambda r,c: r>=21 and not (r<=22 and c>=35) and c<=36
    d=diff('stap1.png','A.png',lambda r,c: gill(r,c) or lintz(r,c))
    print('  A in kieuwzone',sum(gill(*p) for p in d),'| in lintzone',sum(lintz(*p) and not gill(*p) for p in d))
    d=diff('A.png','B.png',lintz)
