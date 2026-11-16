# Keuring r7: meet vulvlakjes, dambord, losse lijnpixels, buitenlijnkanten, om-en-om, tinten.
import sys,numpy as np;from PIL import Image;from scipy import ndimage as nd
FACE=lambda x,y: 18<=x<=36 and 22<=y<=34
def meet(f,lijn={1,15,2,8},vul=(3,4,5,6,7,9,10,11,12,13),sel={2,8},verbose=True):
    im=Image.open(f); o=np.asarray(im).astype(int)[:64,:64]; m=o>0
    P=np.array(im.getpalette()[:768]).reshape(-1,3); L=P@[.299,.587,.114]
    blk=min(set(np.unique(o[m])),key=lambda i:L[i])
    pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    kl=[]
    for v in vul:
        lab,n=nd.label(o==v)
        for i in range(1,n+1):
            ys,xs=np.nonzero(lab==i)
            if len(ys)<3: kl.append((v,list(zip(xs.tolist(),ys.tolist()))))
    db=[]
    for y in range(63):
        for x in range(63):
            q=o[y:y+2,x:x+2]
            if (q>0).all() and q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]: db.append((x,y,int(q[0,0]),int(q[0,1])))
    # losse zwarte pixel binnen de figuur: zwart, geen randpixel, geen 8-buur zwart
    zw=o==blk; los=[]
    for y,x in zip(*np.nonzero(zw&~rand)):
        if zw[max(0,y-1):y+2,max(0,x-1):x+2].sum()==1: los.append((int(x),int(y)))
    # buitenlijn
    E={}
    for y,x in zip(*np.nonzero(rand)):
        d=[(dy,dx) for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if not(0<=y+dy<64 and 0<=x+dx<64) or not m[y+dy,x+dx]]
        E[(int(x),int(y))]=d
    lit=[];sh=[]
    for (x,y),d in E.items():
        s=-sum(a for a,b in d)-sum(b for a,b in d)
        (lit if s>0 else sh if s<0 else []).append((x,y))
    licht_op_rand=[(x,y,int(o[y,x])) for (x,y) in E if o[y,x] not in sel|{blk}]
    alt=[]
    for (x,y) in E:
        nb=[(x+dx,y+dy) for dy in(-1,0,1) for dx in(-1,0,1) if (dx or dy) and (x+dx,y+dy) in E]
        k=o[y,x]==blk
        if o[y,x] in sel|{blk} and len(nb)==2 and all(o[b[1],b[0]] in sel|{blk} and (o[b[1],b[0]]==blk)!=k for b in nb): alt.append((x,y))
    r=dict(px=int(m.sum()),zwart=100*zw.sum()/m.sum(),zwart_binnen=100*(zw&~rand).sum()/m.sum(),vulvlakjes=len(kl),
           vul_buiten_gezicht=[k for k in kl if not all(FACE(x,y) for x,y in k[1])],dambord=db,los_zwart=los,
           lit_zwart=sum(o[y,x]==blk for x,y in lit),lit_sel=sum(o[y,x] in sel for x,y in lit),n_lit=len(lit),
           sh_zwart=sum(o[y,x]==blk for x,y in sh),sh_sel=sum(o[y,x] in sel for x,y in sh),n_sh=len(sh),
           licht_op_rand=licht_op_rand,om_en_om=alt,zw_lichtkant=sorted([p for p in lit if o[p[1],p[0]]==blk],key=lambda p:(p[1],p[0])))
    return r
if __name__=='__main__':
    for f in sys.argv[1:]:
        r=meet(f); print('==',f)
        for k,v in r.items():
            if isinstance(v,list): print(' ',k,len(v),v if len(v)<40 else v[:40])
            else: print(' ',k,round(v,1) if isinstance(v,float) else v)
