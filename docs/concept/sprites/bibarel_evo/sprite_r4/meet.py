# meet.py: rechte runs op tuinbroekranden (>3 px) en vlakgrootte per crèmetint (>40 px), ook tintclusters <3 px
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from scipy import ndimage
o=laad(sys.argv[1] if len(sys.argv)>1 else 'sprite_r4/sprite.png')
fg=o>0; P=np.pad(fg,1); rand=fg&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
CR=np.isin(o,(6,7,15)); CR[:30]=False; CR[:,:14]=False      # tuinbroek (potlood x<14 en gezicht y<30 niet)
def runs(kind):
    out=[]
    # horizontale grens tussen (y,x) en (y+1,x); verticale tussen (y,x) en (y,x+1)
    if kind=='h':
        E=np.zeros((64,64),bool)
        for y in range(63):
            for x in range(64):
                a,b=(y,x),(y+1,x)
                if CR[a]!=CR[b] and fg[a] and fg[b] and not (rand[a] and not CR[a]) and not (rand[b] and not CR[b]): E[y,x]=True
        for y in range(64):
            x=0
            while x<64:
                if E[y,x]:
                    s=x
                    while x<64 and E[y,x]: x+=1
                    if x-s>3: out.append(('horizontaal onder rij %d'%y,s,x-1,x-s))
                else: x+=1
    else:
        E=np.zeros((64,64),bool)
        for y in range(64):
            for x in range(63):
                a,b=(y,x),(y,x+1)
                if CR[a]!=CR[b] and fg[a] and fg[b] and not (rand[a] and not CR[a]) and not (rand[b] and not CR[b]): E[y,x]=True
        for x in range(64):
            y=0
            while y<64:
                if E[y,x]:
                    s=y
                    while y<64 and E[y,x]: y+=1
                    if y-s>3: out.append(('verticaal rechts van kol %d'%x,s,y-1,y-s))
                else: y+=1
    return out
def tintruns():
    out=[]
    for y in range(63):
        x=0
        while x<64:
            if CR[y,x] and CR[y+1,x] and o[y,x]!=o[y+1,x] and not rand[y,x] and not rand[y+1,x]:
                s=x; pr=(o[y,x],o[y+1,x])
                while x<64 and CR[y,x] and CR[y+1,x] and (o[y,x],o[y+1,x])==pr and not rand[y,x] and not rand[y+1,x]: x+=1
                if x-s>3: out.append(('tintgrens horiz onder rij %d'%y,s,x-1,x-s))
            else: x+=1
    for x in range(63):
        y=0
        while y<64:
            if CR[y,x] and CR[y,x+1] and o[y,x]!=o[y,x+1] and not rand[y,x] and not rand[y,x+1]:
                s=y; pr=(o[y,x],o[y,x+1])
                while y<64 and CR[y,x] and CR[y,x+1] and (o[y,x],o[y,x+1])==pr and not rand[y,x] and not rand[y,x+1]: y+=1
                if y-s>3: out.append(('tintgrens vert rechts van kol %d'%x,s,y-1,y-s))
            else: y+=1
    return out
r=runs('h')+runs('v')
print('RANDEN tuinbroek (crème tegen vacht/hand/voet, buitenlijn niet meegeteld) met run >3:',len(r))
for q in r: print('  ',q)
t=tintruns(); print('TINTGRENZEN binnen crème met run >3:',len(t))
for q in t: print('  ',q)
print('VLAKKEN per crèmetint (>40 px = effen):')
for k,n in ((7,'creme'),(6,'creme-schaduw'),(15,'creme-donker')):
    lab,nn=ndimage.label((o==k)&CR&~rand,structure=np.ones((3,3)))
    sz=sorted([(lab==i).sum() for i in range(1,nn+1)],reverse=True)
    print('  %-14s clusters (8-buren) %s'%(n,[int(q) for q in sz]), '<3px:',[[(int(x),int(y)) for y,x in np.argwhere(lab==i)] for i in range(1,nn+1) if (lab==i).sum()<3])
print('crème aandeel:',{n:int(((o==k)&CR).sum()) for k,n in ((7,'C'),(6,'S'),(15,'D'))})
