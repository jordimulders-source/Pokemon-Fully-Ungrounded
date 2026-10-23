# Gedeelde hulp voor ronde "toegepast2": laden, opslaan, pixeldiff, open randen.
import numpy as np, os, shutil
from PIL import Image
S='/home/user/projectgrounded/docs/concept/sprites/'
def load(p):
    im=Image.open(S+p+'/anim_front.png'); return np.array(im).astype(np.uint8), im.getpalette()
def save(a,pal,src,out):
    os.makedirs(S+out,exist_ok=True)
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal)
    im.save(S+out+'/anim_front.png',transparency=0)
    shutil.copy(S+src+'/normal.pal',S+out+'/normal.pal')
def g(rows):
    "tekstraster -> lijst van rijen; '.'=0, hex=index, '?'=laat staan"
    return [r for r in rows]
def put(a,f,x0,y0,rows):
    n=0
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch in '? ': continue
            v=0 if ch=='.' else int(ch,16)
            Y=y0+j+64*f; X=x0+i
            if a[Y,X]!=v: n+=1
            a[Y,X]=v
    return n
def edges(a,outl):
    "opake pixels naast transparant (4-buren, rand telt als transparant) die geen omlijningskleur hebben"
    pad=np.pad(a,1); bad=set()
    H,W=a.shape
    for y in range(H):
        for x in range(W):
            if a[y,x]==0 or a[y,x] in outl: continue
            fy=y%64
            nb=[pad[y,x+1],pad[y+2,x+1],pad[y+1,x],pad[y+1,x+2]]
            if fy==0: nb[0]=0
            if fy==63: nb[1]=0
            if 0 in nb: bad.add((y//64,x,fy))
    return bad
def report(old,new,zones,outl):
    "zones: lijst (f,x0,y0,x1,y1) inclusief. Bewijs: diff buiten zones = 0."
    d=np.argwhere(old!=new); out=[]; outside=0
    for f in (0,1):
        dd=[(int(x),int(y-64*f)) for y,x in d if y//64==f]
        ins=[p for p in dd if any(z[0]==f and z[1]<=p[0]<=z[3] and z[2]<=p[1]<=z[4] for z in zones)]
        outside+=len(dd)-len(ins)
        out.append('frame %d: %d px gewijzigd, buiten de zones: %d'%(f+1,len(dd),len(dd)-len(ins)))
    eo=edges(old,outl); en=edges(new,outl)
    out.append('open randen: nieuw %d (origineel %d, weg %d)'%(len(en-eo),len(eo),len(eo-en)))
    if en-eo: out.append('  NIEUW OPEN: %s'%sorted(en-eo))
    out.append('oppervlak f1 %d -> %d, f2 %d -> %d'%((old[:64]>0).sum(),(new[:64]>0).sum(),(old[64:]>0).sum(),(new[64:]>0).sum()))
    out.append('kleuren: %d -> %d, max index %d'%(len(np.unique(old)),len(np.unique(new)),new.max()))
    return out,outside
