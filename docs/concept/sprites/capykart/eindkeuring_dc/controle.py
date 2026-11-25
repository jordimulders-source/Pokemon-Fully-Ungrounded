# controles: silhouet, kleuren, om-en-om op de buitenrand, tintvlekjes < 3 px, zwart per richting
import sys; sys.argv=['x']
exec(open('eindkeuring_dc/bouw.py').read().replace("if __name__=='__main__'","if False"))
from scipy import ndimage as nd
nn=np.array(Image.open('eindkeuring_dc/capykart.png'))
print('silhouet-diff t.o.v. eindkeuring_r17:',int(((nn==0)!=(o==0)).sum()))
print('kleuren incl. transparant:',len(set(nn.ravel())),'palet',len(PAL))
# om-en-om: ring-pixels K waarvan beide ringburen (4-buren in de ring) selout zijn, en omgekeerd
lijn=set(SEL.values())
oe=0
for y,x in zip(*np.where(ring)):
    k=nn[y,x]; bs=[nn[yy,xx] for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if 0<=yy<64 and 0<=xx<64 and ring[yy,xx]]
    if len(bs)>=2 and ((k==K and all(b in lijn and b!=K for b in bs)) or (k!=K and all(b==K for b in bs))): oe+=1
print('om-en-om op buitenrand (pixel tegengesteld aan beide ringburen):',oe)
lichtrand=[(x,y) for y,x in zip(*np.where(ring)) if nn[y,x] in (B3,B4,GE,RO,BL,GL,CR,HL)]
print('lichte kleur op buitenrand:',lichtrand)
# zwart op buitenrand per richting
tel={}
for y,x in zip(*np.where(ring)):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            yy,xx=y+dy,x+dx
            if (dy or dx) and (not(0<=yy<64 and 0<=xx<64) or nn[yy,xx]==0): v+=(dx,dy)
    if not v.any(): continue
    a=np.degrees(np.arctan2(v[1],v[0]))%360
    r=['rechts','rechtsonder','onder','linksonder','links','linksboven','boven','rechtsboven'][int(((a+22.5)%360)//45)]
    t=tel.setdefault(r,[0,0]); t[1]+=1; t[0]+=nn[y,x]==K
print('zwart/totaal op buitenrand:',{k:'%d/%d'%tuple(v) for k,v in tel.items()})
# tintvlekjes < 3 px (8-samenhang) binnen de vulling
klein=[]
for k in range(2,16):
    lab,c=nd.label(nn==k,structure=np.ones((3,3)))
    for i in range(1,c+1):
        m=lab==i
        if m.sum()<3: klein.append((k,[(int(x),int(y)) for y,x in zip(*np.where(m))]))
print('tintvlekjes < 3 px:',len(klein))
for k,p in klein: print('  ',k,p)
for k in range(1,16): print(k,PAL[k],int((nn==k).sum()))
