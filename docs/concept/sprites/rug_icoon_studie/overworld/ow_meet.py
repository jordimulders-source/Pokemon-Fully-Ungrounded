# Meetstudie overworld: per aanzicht (voor/achter/opzij) maat t.o.v. front en icoon, loopframes.
# Gebruik (repo-root): python3 docs/concept/sprites/rug_icoon_studie/overworld/ow_meet.py
import os,json,numpy as np
from PIL import Image
G='graphics/pokemon'
def bbox(a):
    ys,xs=np.nonzero(a)
    return None if len(xs)==0 else (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
def shift_best(a,b,r=3):
    # beste verschuiving van b op a; geeft (dx,dy,aandeel verschillende pixels)
    best=(0,0,1e9)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            bb=np.roll(np.roll(b,dy,0),dx,1)
            d=((a>0)|(bb>0)).sum(); n=((a!=bb)&((a>0)|(bb>0))).sum()
            if n<best[2]: best=(dx,dy,n)
    tot=((a>0)|(b>0)).sum()
    return best[0],best[1],best[2]/max(tot,1)
rows=[]
for sp in sorted(os.listdir(G)):
    d=os.path.join(G,sp); op=d+'/overworld.png'
    fp=d+'/anim_front.png'
    if not (os.path.exists(op) and os.path.exists(fp)): continue
    o=np.array(Image.open(op)); fs=o.shape[0]
    if o.shape[1]!=6*fs: continue
    fr=[o[:,i*fs:(i+1)*fs] for i in range(6)]
    f=np.array(Image.open(fp))[:64]; bf=bbox(f)
    if not bf: continue
    r={'sp':sp,'fs':fs,'fh':bf[3]-bf[1]+1,'fw':bf[2]-bf[0]+1}
    ip=d+'/icon.png'
    if os.path.exists(ip):
        i=np.array(Image.open(ip))[:32]; bi=bbox(i)
        if bi: r['ih'],r['iw']=bi[3]-bi[1]+1,bi[2]-bi[0]+1
    for k,n in [(0,'v'),(2,'a'),(4,'z')]:
        b=bbox(fr[k]); b2=bbox(fr[k+1])
        if not b or not b2: break
        r[n+'h'],r[n+'w'],r[n+'bot'],r[n+'top'],r[n+'cx']=b[3]-b[1]+1,b[2]-b[0]+1,b[3],b[1],(b[0]+b[2])/2
        r[n+'h2'],r[n+'bot2'],r[n+'top2']=b2[3]-b2[1]+1,b2[3],b2[1]
        dx,dy,frac=shift_best(fr[k],fr[k+1])
        r[n+'dx'],r[n+'dy'],r[n+'diff']=dx,dy,round(float(frac),3)
        # waar zit het verschil (zonder verschuiving): bovenste of onderste helft van de figuur
        dm=(fr[k]!=fr[k+1]); ys=np.nonzero(dm)[0]
        r[n+'difftop']=round(float(((ys-b[1])/(b[3]-b[1]+1)).mean()),2) if len(ys) else None
        r[n+'ncol']=len(np.unique(fr[k]))-1
        # spiegelsymmetrie (alleen zinvol voor voor/achter)
        m=fr[k]>0; x0,x1=b[0],b[2]; mm=m[:,x0:x1+1]
        r[n+'sym']=round(float((mm==mm[:,::-1]).mean()),3)
    else:
        rows.append(r)
json.dump(rows,open('docs/concept/sprites/rug_icoon_studie/overworld/data_ow.json','w'))
print(len(rows))
