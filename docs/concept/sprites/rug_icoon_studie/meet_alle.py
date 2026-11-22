import os,sys,json,numpy as np
from PIL import Image
G='graphics/pokemon'; S=sys.argv[1]
gen=dict(l.split() for l in open(S+'/gen.txt'))
def bbox(a):
    ys,xs=np.nonzero(a)
    return None if len(xs)==0 else (xs.min(),ys.min(),xs.max(),ys.max())
rows=[]
for sp in sorted(os.listdir(G)):
    d=os.path.join(G,sp)
    if sp not in gen or not os.path.exists(d+'/back.png'): continue
    fp=d+'/anim_front.png' if os.path.exists(d+'/anim_front.png') else d+'/front.png'
    if not os.path.exists(fp): continue
    f=np.array(Image.open(fp))[:64]; b=np.array(Image.open(d+'/back.png'))
    bf,bb=bbox(f),bbox(b)
    if not bf or not bb: continue
    r={'sp':sp,'gen':int(gen[sp]),'fw':bf[2]-bf[0]+1,'fh':bf[3]-bf[1]+1,'bw':bb[2]-bb[0]+1,'bh':bb[3]-bb[1]+1,'bbot':bb[3]}
    row=(b[bb[3]]>0).sum(); r['bflat']=row/ (b>0).sum(axis=1).max()
    if os.path.exists(d+'/icon.png'):
        i=np.array(Image.open(d+'/icon.png'))[:32]; bi=bbox(i)
        if bi: r['iw'],r['ih'],r['ibot']=bi[2]-bi[0]+1,bi[3]-bi[1]+1,bi[3]
    if os.path.exists(d+'/overworld.png'):
        o=np.array(Image.open(d+'/overworld.png')); fs=o.shape[0]; r['ows']=fs
        bo=bbox(o[:,:fs])
        if bo: r['oh'],r['ow'],r['obot']=bo[3]-bo[1]+1,bo[2]-bo[0]+1,bo[3]
        r['ocol']=len(np.unique(o))-1
    rows.append(r)
json.dump(rows,open(S+'/meet2.json','w'),default=int); print(len(rows))
