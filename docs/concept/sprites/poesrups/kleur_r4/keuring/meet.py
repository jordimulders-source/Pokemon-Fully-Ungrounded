# Metingen eindkeuring poesrups r4: palet, luma-stappen, clusters, buitenrand, lichtverdeling, vergelijking Gen 3
from PIL import Image
from collections import Counter, deque
import os
R='/home/user/Pokemon-Fully-Ungrounded/'
S=R+'docs/concept/sprites/'
def luma(c): return .299*c[0]+.587*c[1]+.114*c[2]
im=Image.open(S+'poesrups/kleur_r4/poesrups.png'); px=im.load(); pal=im.getpalette()
P={i:tuple(pal[i*3:i*3+3]) for i in range(16)}
G={(x,y):px[x,y] for x in range(64) for y in range(64) if px[x,y]}
cnt=Counter(G.values())
print('kleuren gebruikt:',len(cnt),'+ transparant')
for i in sorted(cnt,key=lambda i:-luma(P[i])): print('  %X %s luma %.1f  %d px'%(i,P[i],luma(P[i]),cnt[i]))
LINE={1,2,3,4}
# buitenrand
N4=[(1,0),(-1,0),(0,1),(0,-1)]
edge={p:v for p,v in G.items() if any((p[0]+dx,p[1]+dy) not in G for dx,dy in N4)}
print('buitenrand px',len(edge),Counter(edge.values()))
print('lichte kleur op buitenrand (5,6,7,A):',sorted(p for p,v in edge.items() if v not in LINE))
# buitenlijn-dikte: lijnpixel (2/3) op rand met lijnpixel (1-3) direct erachter naar binnen, loodrecht
# per rij: index van meest linkse en meest rechtse pixel; per kolom bovenste/onderste
print('links per rij :',''.join('%X'%G[min((p for p in G if p[1]==y))] for y in range(29,63)))
print('rechts per rij:',''.join('%X'%G[max((p for p in G if p[1]==y))] for y in range(29,63)))
xs=sorted({p[0] for p in G})
print('boven per kolom:',''.join('%X'%G[min((p for p in G if p[0]==x),key=lambda p:p[1])] for x in xs))
print('onder per kolom:',''.join('%X'%G[max((p for p in G if p[0]==x),key=lambda p:p[1])] for x in xs))
# clusters (4-verbonden) per vlaktint
def clusters(idx):
    seen=set();out=[]
    for p,v in G.items():
        if v!=idx or p in seen: continue
        q=deque([p]);seen.add(p);c=[p]
        while q:
            a=q.popleft()
            for dx,dy in N4:
                b=(a[0]+dx,a[1]+dy)
                if G.get(b)==idx and b not in seen: seen.add(b);q.append(b);c.append(b)
        out.append(c)
    return out
lw=set()
for f in('../lijnwerk.txt','../pootjes.txt'):
    for l in open(f):
        l=l.strip()
        if ',' in l:
            a,b=l.split(',')[:2]
            try: lw.add((int(a),int(b)))
            except: pass
for idx in (10,7,6,5,4,3):
    cl=clusters(idx)
    small=[c for c in cl if len(c)<3]
    print('tint %X: %d clusters, <3 px: %d'%(idx,len(cl),len(small)),[(sorted(c),'lijnwerk' if all(p in lw for p in c) else 'VLAK') for c in small])
# lichtverdeling: gem. luma vlakpixels per kwadrant van de bounding box
x0=min(p[0] for p in G);x1=max(p[0] for p in G);y0=min(p[1] for p in G);y1=max(p[1] for p in G)
cx=(x0+x1)/2;cy=(y0+y1)/2
for name,f in (('linksboven',lambda p:p[0]<cx and p[1]<cy),('rechtsboven',lambda p:p[0]>=cx and p[1]<cy),('linksonder',lambda p:p[0]<cx and p[1]>=cy),('rechtsonder',lambda p:p[0]>=cx and p[1]>=cy)):
    v=[luma(P[G[p]]) for p in G if f(p) and G[p] not in LINE]
    print('  %-11s gem. luma vlak %.0f (%d px)'%(name,sum(v)/len(v),len(v)))
# gem. luma per kolomband (romp x 6..46, rijen 40..57)
print('luma per kolomband (5 px), vlakpixels rij 38-57:')
for a in range(5,60,5):
    v=[luma(P[G[p]]) for p in G if a<=p[0]<a+5 and 38<=p[1]<=57 and G[p] not in LINE]
    if v: print('   x%2d-%2d: %.0f'%(a,a+4,sum(v)/len(v)))
print('luma per rijband, vlakpixels:')
for a in range(29,62,4):
    v=[luma(P[G[p]]) for p in G if a<=p[1]<a+4 and G[p] not in LINE]
    if v: print('   y%2d-%2d: %.0f'%(a,a+3,sum(v)/len(v)))
# pillow: aandeel vlakpixels grenzend aan buitenlijn dat donkerder is dan basis, per zijde
# vergelijking Gen 3
def stats(path,label):
    im=Image.open(path)
    if im.mode!='P': print(label,'niet geindexeerd');return
    im=im.crop((0,0,64,64));p=im.load();pl=im.getpalette()
    c=Counter(p[x,y] for x in range(64) for y in range(64) if p[x,y]!=0)
    tot=sum(c.values())
    cols=sorted(((luma(pl[i*3:i*3+3]),tuple(pl[i*3:i*3+3]),n) for i,n in c.items()),reverse=True)
    mean=sum(l*n for l,_,n in cols)/tot
    print('%-12s %2d kl. gem.luma %.0f  donkerste %.0f  | '%(label,len(c),mean,cols[-1][0])+' '.join('%.0f(%d)'%(l,n) for l,_,n in cols))
stats(S+'poesrups/kleur_r4/poesrups.png','POESRUPS')
stats(S+'poedellarve/af/poedellarve.png','poedellarve')
stats(S+'poedelmot/af/poedelmot.png','poedelmot')
for n in['silcoon','cascoon','wurmple','swablu','altaria','mareep','seel','dewgong','swinub','castform']:
    for f in('anim_front.png','front.png'):
        pth=R+'graphics/pokemon/%s/%s'%(n,f)
        if os.path.exists(pth): stats(pth,n);break
