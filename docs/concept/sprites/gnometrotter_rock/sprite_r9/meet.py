# meet.py: waar staat zwart? buitenrand per kant (richting naar transparant) en binnen
import sys,numpy as np; from PIL import Image
def zwart_idx(im):
    p=np.array(im.getpalette()[:48]).reshape(16,3); s=p.sum(1); return [i for i in range(1,16) if s[i]<120]
def meet(f):
    im=Image.open(f); a=np.array(im).astype(int); Z=zwart_idx(im); H,W=a.shape
    fig=a>0; bl=np.isin(a,Z)&fig
    kant={'boven':[0,0],'links':[0,0],'rechts':[0,0],'onder':[0,0]}
    rand=np.zeros_like(fig)
    for y in range(H):
        for x in range(W):
            if not fig[y,x]: continue
            d=[]
            for n,(dx,dy) in {'links':(-1,0),'rechts':(1,0),'boven':(0,-1),'onder':(0,1)}.items():
                i,j=x+dx,y+dy
                if not(0<=i<W and 0<=j<H) or not fig[j,i]: d.append(n)
            if d:
                rand[y,x]=1
                for n in d: kant[n][0 if bl[y,x] else 1]+=1
    binnen=bl&~rand
    # binnenzwart: grenst het aan een randzwart (aansluitend) of los?
    nb=0
    for y,x in np.argwhere(binnen):
        if any(bl[j,i] and rand[j,i] for j in range(y-1,y+2) for i in range(x-1,x+2) if 0<=i<W and 0<=j<H): nb+=1
    print('%-40s zwart=%d (rand %d, binnen %d waarvan %d direct aan randzwart)'%(f.split('/')[-1],bl.sum(),(bl&rand).sum(),binnen.sum(),nb))
    for n,(z,o) in kant.items(): print('   rand %-6s zwart %3d / ander %3d  = %d%%'%(n,z,o,100*z//max(1,z+o)))
    return a,bl,rand
if __name__=='__main__':
    for f in sys.argv[1:]: meet(f)
