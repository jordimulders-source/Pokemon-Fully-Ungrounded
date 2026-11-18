import os,sys,re,json,numpy as np
from PIL import Image
sys.path.insert(0,'tools/concept/sprites'); import spritelib as L
G='graphics/pokemon'
def arr(p):
    im=Image.open(p); return np.array(im), im
def bbox(a):
    ys,xs=np.nonzero(a)
    if len(xs)==0: return None
    return xs.min(),ys.min(),xs.max(),ys.max()
def wh(b): return (b[2]-b[0]+1,b[3]-b[1]+1)
# iconPalIndex per soort
ipi={}
for f in os.listdir('src/data/pokemon/species_info'):
    t=open('src/data/pokemon/species_info/'+f).read()
    for m in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',t,re.S):
        mm=re.search(r'iconPalIndex = (\d)',m.group(2))
        if mm: ipi[m.group(1).lower()]=int(mm.group(1))
rows=[]
for sp in sorted(os.listdir(G)):
    d=os.path.join(G,sp)
    if not os.path.exists(d+'/back_gba.png'): continue
    r={'sp':sp}
    for set_,fn,bn,ic in [('g','anim_front_gba.png','back_gba.png','icon_gba.png'),('n','anim_front.png','back.png','icon.png')]:
        fp=d+'/'+fn
        if not os.path.exists(fp): fp=d+'/'+fn.replace('anim_','')
        if not os.path.exists(fp): continue
        f,_=arr(fp); f1=f[:64]; b,_=arr(d+'/'+bn)
        bf=bbox(f1); bb=bbox(b)
        if not bf or not bb: continue
        r[set_+'fw'],r[set_+'fh']=wh(bf); r[set_+'bw'],r[set_+'bh']=wh(bb)
        r[set_+'fbot']=bf[3]; r[set_+'bbot']=bb[3]
        r[set_+'bcut']=float((b[63]>0).sum()/max(1,(b[bb[1]:,:]>0).sum(axis=1).max()))
        r[set_+'fcx']=(bf[0]+bf[2])/2; r[set_+'bcx']=(bb[0]+bb[2])/2
        r[set_+'fcol']=len(np.unique(f1))-1; r[set_+'bcol']=len(np.unique(b))-1
        # zelfde indexen?
        r[set_+'bonly']=len(set(np.unique(b))-set(np.unique(f)))
        if os.path.exists(d+'/'+ic):
            i,_=arr(d+'/'+ic); i1=i[:32]; i2=i[32:64]; bi=bbox(i1)
            if bi:
                r[set_+'iw'],r[set_+'ih']=wh(bi); r[set_+'ibot']=bi[3]; r[set_+'icol']=len(np.unique(i))-1
                bi2=bbox(i2); r[set_+'idy']=bi2[3]-bi[3] if bi2 else None
                r[set_+'idytop']=bi2[1]-bi[1] if bi2 else None
                # beste verschuiving
                best=1e9
                for dy in range(-3,4):
                    for dx in range(-3,4):
                        s=np.roll(np.roll(i1,dy,0),dx,1); best=min(best,(s!=i2).sum())
                r[set_+'idiff']=best/max(1,(i1>0).sum())
    if os.path.exists(d+'/overworld.png'):
        o,_=arr(d+'/overworld.png'); fs=o.shape[0]
        r['ows']=fs
        for k,name in enumerate(['s1','s2','n1','n2','w1','w2']):
            fr=o[:,k*fs:(k+1)*fs]; bo=bbox(fr)
            if bo: r['o'+name+'w'],r['o'+name+'h']=wh(bo); r['o'+name+'bot']=bo[3]
        r['ocol']=len(np.unique(o))-1
    r['ipi']=ipi.get(sp)
    rows.append(r)
json.dump(rows,open(sys.argv[1],'w'),default=int)
print(len(rows))
