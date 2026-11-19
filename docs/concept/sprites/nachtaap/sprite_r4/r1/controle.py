# Controle: kleuren, randpixels, kleine tintclusters, losse omlijningspixels
import sys; sys.path.insert(0,'r1'); from pal import *
def label(m):
    lab=np.zeros(m.shape,int); n=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]
        while st:
            b,a=st.pop()
            if 0<=b<m.shape[0] and 0<=a<m.shape[1] and m[b,a] and not lab[b,a]:
                lab[b,a]=n; st+=[(b+1,a),(b-1,a),(b,a+1),(b,a-1)]
    return lab,n
f=sys.argv[1] if len(sys.argv)>1 else 'r1/anim_front.png'
im=Image.open(f); g=np.array(im)[:64].astype(int)
print('modus',im.mode,im.size,'transp',im.info.get('transparency'),'gebruikte indexen',sorted(set(g.flatten())-{0}),'aantal',len(set(g.flatten())-{0}))
H,W=g.shape; rand_ok={1,2,3,9,13,14}   # omlijning, selout, donkerpaars, oogrand, bruin, pupil
print('-- lichte kleur op de buitenrand:')
for y in range(H):
    for x in range(W):
        if g[y,x] and g[y,x] not in rand_ok:
            nb=[g[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else 0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
            if 0 in nb: print('  ',(x,y),S[g[y,x]])
print('-- tintclusters < 3 px (4-buren, zelfde index):')
for v in range(2,16):
    lab,n=label(g==v)
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(ys)<3: print('  ',S[v],list(zip(xs.tolist(),ys.tolist())))
print('-- losse pixels (geen enkele 8-buur met dezelfde index):')
for y in range(H):
    for x in range(W):
        v=g[y,x]
        if v:
            n=sum(1 for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W and g[y+dy,x+dx]==v)
            if n==0: print('  ',(x,y),S[v])
print('-- omlijning 1 zonder contact met rand of andere lijn:')
for y in range(H):
    for x in range(W):
        if g[y,x]==1:
            nb=[g[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
            if 0 not in nb and not any(v in (1,2,9) for v in nb): print('  ',(x,y))
