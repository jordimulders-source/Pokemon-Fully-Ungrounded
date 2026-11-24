import re,os,sys,json,glob,subprocess
from PIL import Image
import numpy as np
R="/home/user/Pokemon-Fully-Ungrounded/"
src=open(R+"docs/concept/sprites/showcase/maak_vel.py").read()
items=re.findall(r'\(\s*["\']([^"\']+\.png)["\']\s*,\s*([\'"].*?[\'"])\s*,',src)
def load(p):
    im=Image.open(p)
    a=im.convert("RGBA").crop((0,0,64,64))
    arr=np.array(a).astype(int)
    if im.mode=="P":
        idx=np.array(im)[:64,:64]; op=idx!=0
    else: op=arr[:,:,3]>0
    return arr[:,:,:3],op
def lum(c): return 0.299*c[...,0]+0.587*c[...,1]+0.114*c[...,2]
def metr(p):
    rgb,op=load(p)
    H,W=op.shape
    key=(rgb[:,:,0]<<16)|(rgb[:,:,1]<<8)|rgb[:,:,2]; key=np.where(op,key,-1)
    cols=np.unique(key[op]); n=len(cols)
    area=op.sum(); ys,xs=np.where(op); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
    pad=np.pad(op,1); 
    nb=[np.roll(pad,s,a)[1:-1,1:-1] for s,a in((1,0),(-1,0),(1,1),(-1,1))]
    edge=op&~(nb[0]&nb[1]&nb[2]&nb[3])
    L=lum(rgb)
    edgeL=L[edge].mean(); edge_dark=(L[edge]<60).mean()
    # same-colour neighbour ratio
    same=tot=0
    for dy,dx in((0,1),(1,0)):
        a=key[:H-dy,:W-dx]; b=key[dy:,dx:]; m=(a>=0)&(b>=0)
        same+=(a[m]==b[m]).sum(); tot+=m.sum()
    flat=same/tot
    # small clusters
    from scipy import ndimage
    small=0; ncl=0
    for c in cols:
        lab,k=ndimage.label(key==c); 
        if k==0: continue
        sz=np.bincount(lab.ravel())[1:]; ncl+=k
        small+=sz[sz<=2].sum()
    noise=small/area; meancl=area/ncl
    # checker/dither 2x2: a b / b a with a!=b
    a=key[:-1,:-1];b=key[:-1,1:];c=key[1:,:-1];d=key[1:,1:]
    chk=((a==d)&(b==c)&(a!=b)&(a>=0)&(b>=0)).sum()/area
    # interior dark lines
    inner=op&~edge
    darkthr=np.percentile(L[op],10)
    inner_dark=((L<=max(darkthr,50))&inner).sum()/area
    # light direction: top-left vs bottom-right (within sprite, excluding edge)
    cy,cx=ys.mean(),xs.mean()
    tl=inner&((np.arange(H)[:,None]-cy)+(np.arange(W)[None,:]-cx)<0)
    br=inner&((np.arange(H)[:,None]-cy)+(np.arange(W)[None,:]-cx)>0)
    light=L[tl].mean()-L[br].mean()
    # contrast range
    lr=np.percentile(L[op],95)-np.percentile(L[op],5)
    # 3x3 variety
    var=[]
    for y,x in zip(ys,xs):
        if 0<y<H-1 and 0<x<W-1 and op[y-1:y+2,x-1:x+2].all():
            var.append(len(np.unique(key[y-1:y+2,x-1:x+2])))
    var=np.mean(var) if var else 0
    # saturation mean
    mx=rgb.max(2);mn=rgb.min(2); sat=((mx-mn)/np.maximum(mx,1))[op].mean()
    return dict(n=int(n),area=int(area),h=int(h),w=int(w),edgeL=round(float(edgeL),1),edge_dark=round(float(edge_dark),2),
        flat=round(float(flat),3),noise=round(float(noise),3),meancl=round(float(meancl),1),chk=round(float(chk),3),
        inner_dark=round(float(inner_dark),3),light=round(float(light),1),lr=round(float(lr),1),var=round(float(var),2),sat=round(float(sat),2))
out={"ours":[],"gen3":[]}
for p,nm in items:
    full=R+"docs/concept/sprites/"+p
    d=metr(full); d["name"]=nm.strip("'\""); d["path"]=p
    try:
        dt=subprocess.run(["git","-C",R,"log","--diff-filter=A","--follow","--format=%as","--",full],capture_output=True,text=True).stdout.split()
        d["date"]=dt[-1] if dt else ""
    except: d["date"]=""
    out["ours"].append(d)
for f in sorted(glob.glob(R+"graphics/pokemon/*/anim_front_gba.png")):
    d=metr(f); d["name"]=f.split("/")[-2]; out["gen3"].append(d)
json.dump(out,open("metrics.json","w"),indent=0)
print(len(out["ours"]),len(out["gen3"]))
