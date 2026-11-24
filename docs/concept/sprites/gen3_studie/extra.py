import json,numpy as np,glob
exec(open("metrics.py").read().split("def metr")[0])
from scipy import ndimage
def ex(p):
    rgb,op=load(p); H,W=op.shape
    key=np.where(op,(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2],-1)
    pad=np.pad(op,1); nb=[np.roll(pad,s,a)[1:-1,1:-1] for s,a in((1,0),(-1,0),(1,1),(-1,1))]
    edge=op&~(nb[0]&nb[1]&nb[2]&nb[3]); inner=op&~edge
    L=lum(rgb); ys,xs=np.where(op); cy,cx=ys.mean(),xs.mean()
    Y,X=np.mgrid[:H,:W]; tl=(Y-cy)+(X-cx)<0
    lite_dark=(L[edge&tl]<60).mean()   # zwart aan lichtkant
    shad_dark=(L[edge&~tl]<60).mean()
    small=0
    for c in np.unique(key[inner]):
        lab,k=ndimage.label((key==c)&inner); sz=np.bincount(lab.ravel())[1:]; small+=sz[sz<=2].sum()
    # binnenlijnen: donkere pixels (L<70) binnenin
    il=((L<70)&inner).sum()/inner.sum()
    return lite_dark,shad_dark,small/inner.sum(),il
R="/home/user/Pokemon-Fully-Ungrounded/"
D=json.load(open("scored.json"))
g=np.array([ex(f) for f in glob.glob(R+"graphics/pokemon/*/anim_front_gba.png")])
o=np.array([ex(R+"docs/concept/sprites/"+d["path"]) for d in D["ours"]])
for i,n in enumerate(["zwart lichtkant","zwart schaduwkant","binnen-ruis(<=2px)","donker binnenin"]):
    print(f"{n:20} gen3 p10/med/p90 {np.percentile(g[:,i],10):.2f}/{np.median(g[:,i]):.2f}/{np.percentile(g[:,i],90):.2f}   ons {np.percentile(o[:,i],10):.2f}/{np.median(o[:,i]):.2f}/{np.percentile(o[:,i],90):.2f}")
for d,v in zip(D["ours"],o): d["lite_dark"],d["shad_dark"],d["inoise"],d["il"]=map(float,v)
json.dump(D,open("scored.json","w"))
for d in sorted(D["ours"],key=lambda d:-d["lite_dark"])[:15]: print(f'{d["lite_dark"]:.2f} {d["name"]}')
