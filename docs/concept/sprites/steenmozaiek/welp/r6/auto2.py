# Lijf-onderlaag r6: vulpixels (bruin, niet de buitenrand) krijgen de toon van het model op helderheid (facetlum.npy):
# <84 S, <120 M, anders L; 3x3-modus binnen dezelfde vorm (2x), clusters < 4 px naar de buurtint.
import numpy as np
r5=np.load('welp_r5.npy'); F=np.load('form.npy'); lum=np.load('facetlum.npy'); H,W=r5.shape
S,M,L=3,4,5; BR=(S,M,L)
edge=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if r5[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or r5[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): edge[y,x]=True
vul=np.isin(r5,BR+(2,))&~edge   # ook lijnbruin binnenin opnieuw bepalen
a=r5.copy()
for y,x in zip(*np.where(vul)):
    l=lum[y,x]
    if l>0: a[y,x]=S if l<84 else (M if l<120 else L)
    elif a[y,x]==2: a[y,x]=S
def modus(a,it=2):
    for _ in range(it):
        o=a.copy()
        for y,x in zip(*np.where(vul)):
            cnt={}
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W and a[yy,xx] in BR and F[yy,xx]==F[y,x]: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
            if cnt:
                v=max(cnt,key=cnt.get)
                if cnt[v]>=5: o[y,x]=v
        a=o
    return a
def korrels(a,mn=4):
    seen=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            if seen[j,i] or not vul[j,i]: continue
            c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==c and vul[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<mn:
                cnt={}
                for y,x in cl:
                    for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                        if 0<=yy<H and 0<=xx<W and a[yy,xx] in BR and a[yy,xx]!=c: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
                if cnt:
                    v=max(cnt,key=cnt.get)
                    for y,x in cl: a[y,x]=v
    return a
a=modus(a); a=korrels(a); a=korrels(a)
np.save('auto2.npy',a)
ch='.KdSMLPQRgWCTGH'
print('    '+''.join(str(x%10) for x in range(W)))
for y in range(H): print('%2d  '%y+''.join(ch[v] for v in a[y]))
