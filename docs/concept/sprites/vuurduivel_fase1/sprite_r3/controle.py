# controle.py SPRITE.png: formaat, kleuren, hoogte, tintvlekjes <3 px, losse zwarte pixels, lichte kleur op de buitenrand
import sys, numpy as np; from PIL import Image
CH='.#dmlRrOYbBkpWMa'
im=Image.open(sys.argv[1]); o=np.asarray(im).astype(int)
used=sorted(set(o.ravel()))
print('formaat',im.size,im.mode,'transp',im.info.get('transparency'),'indexen gebruikt',len(used),''.join(CH[k] for k in used))
fg=o>0; yy,xx=np.where(fg); print('bbox x%d-%d y%d-%d -> %dx%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1,fg.sum()))
def comp(m):
    seen=np.zeros_like(m); out=[]
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=1; c=[]
        while st:
            a,b=st.pop(); c.append((b,a))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                p,q=a+dy,b+dx
                if 0<=p<64 and 0<=q<64 and m[p,q] and not seen[p,q]: seen[p,q]=1; st.append((p,q))
        out.append(c)
    return out
for k in used:
    if k in (0,1): continue
    kl=[c for c in comp(o==k) if len(c)<3]
    if kl: print('  %s: %d vlekjes <3 px: %s'%(CH[k],len(kl),[c[0] for c in kl]))
los=[(x,y) for y,x in zip(*np.where(o==1)) if all(o[y+dy,x+dx] not in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
licht={4,8,13,11,12}
rand=[(x,y,CH[o[y,x]]) for y,x in zip(yy,xx) if o[y,x] in licht and (not fg[y,x-1] or not fg[y,x+1] or not fg[y-1,x] or not fg[y+1,x])]
print('lichte kleur op de buitenrand:',rand)
