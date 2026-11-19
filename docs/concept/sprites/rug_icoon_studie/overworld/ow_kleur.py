# Kleur van overworldsprites t.o.v. de front: omlijning, aantal kleuren, hoeveel OW-kleuren uit het frontpalet komen.
import os,json,colorsys,numpy as np
from PIL import Image
G='graphics/pokemon'
def pal(p):
    L=[l.split() for l in open(p).read().split('\n')[3:] if l.strip()]
    return np.array([[int(x) for x in l] for l in L],float)
def lum(c): return 0.299*c[...,0]+0.587*c[...,1]+0.114*c[...,2]
out=[]
for sp in sorted(os.listdir(G)):
    d=os.path.join(G,sp)
    try:
        o=np.array(Image.open(d+'/overworld.png')); op=pal(d+'/overworld_normal.pal'); fp=pal(d+'/normal.pal')
        f=np.array(Image.open(d+'/anim_front.png'))[:64]
    except Exception: continue
    if o.shape[0]!=32: continue
    fr=o[:,:32]  # voor
    m=fr>0
    # randpixels: figuurpixels met een transparante 4-buur
    pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    el=lum(op[fr[edge]]); 
    used=np.unique(o[o>0]); fused=np.unique(f[f>0])
    oc=op[used]; fc=fp[fused]
    dist=np.sqrt(((oc[:,None,:]-fc[None,:,:])**2).sum(-1)).min(1)
    # helderheid/verzadiging van het grootste vlak (meest gebruikte niet-randkleur)
    inner=fr[m&~edge]; 
    if len(inner)==0: continue
    vals,cnt=np.unique(inner,return_counts=True); big=op[vals[cnt.argmax()]]/255
    fv,fc2=np.unique(f[f>0],return_counts=True)
    # dichtstbijzijnde frontkleur bij dat vlak
    j=np.sqrt(((fp[fv]-big*255)**2).sum(-1)).argmin(); fb=fp[fv[j]]/255
    h1,l1,s1=colorsys.rgb_to_hls(*big); h2,l2,s2=colorsys.rgb_to_hls(*fb)
    out.append({'sp':sp,'edge_lum_med':float(np.median(el)),'edge_dark':float((el<60).mean()),
                'n_used':len(used),'n_front':len(fused),'same':float((dist<12).mean()),'near':float((dist<30).mean()),
                'dL':l1-l2,'dS':s1-s2})
json.dump(out,open('docs/concept/sprites/rug_icoon_studie/overworld/data_kleur.json','w'))
A=lambda k:np.array([r[k] for r in out])
for k in ['edge_lum_med','edge_dark','n_used','n_front','same','near','dL','dS']:
    v=A(k); print(k,'mediaan %.2f p25 %.2f p75 %.2f'%(np.median(v),np.percentile(v,25),np.percentile(v,75)))
print(len(out))
