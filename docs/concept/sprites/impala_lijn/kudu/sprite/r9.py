# Ronde 9: 3 vormen (onderrand borstkant N=3/6/9 px hoger) x 2 manieren (A pluizige kraag, B lang hangend kapsel).
import r9lib as R, r8lib as L, r8, itertools
VORMEN=(3,6,9)
BOVEN={  # stukken boven de snede (uit r8), per manier
 'A':[(r8.A_UP2,22,25,'kampunt 1'),(r8.A_UP2,26,26,'kampunt 2'),(r8.A_UP2,29,28,'kampunt 3'),
      (r8.A_LEFT,7,33,'franjepluk',2),(r8.A_LEFT,15,27,'nekrand-pluk 1'),(r8.A_LEFT,15,32,'nekrand-pluk 2'),
      (r8.A_DOWN,25,27,'kampunt onder (over de rug)'),
      (r8.A_RIGHT,21,31,'schouderpunten 1'),(r8.A_RIGHT,19,36,'schouderpunten 2'),(r8.A_BUMP,22,31,'schouderbult')],
 'B':[(r8.A_UP2,26,26,'kampunt'),(r8.A_DOWN,25,27,'kampunt onder (over de rug)'),
      (r8.A_RIGHT,19,36,'schouderpunt (onderste lok)'),(r8.A_BUMP,23,31,'schouderbult')],
}
ONDER={'A':(9,13,17),'B':(8,11,14,17)}
def onderrand(mask,x):
    ys=[y for (a,y) in mask if a==x]; return max(ys) if ys else None
def stukken(N,m):
    v=R.Vorm9(N); out=[]
    for st in BOVEN[m]:
        sn,dx,dy=st[0],st[1],st[2]; S=L.snip(*sn)
        if any((dx+i,dy+j) in v.vrij for j,r in enumerate(S) for i,c in enumerate(r) if c not in '.#'): continue
        out.append(st)
    links=min(x for x,y in v.mask0 if y>=33)
    for x in ONDER[m]:
        x=max(x,links-1); b=onderrand(v.mask0,x+2)
        if b is not None: out.append((r8.A_DOWN,x,b-3,'onderpunt x%d'%x,1))
    return out
def maak(N,m,st):
    v=R.Vorm9(N); v.veld(*r8.VELD,label='vlak: Arcanine-rugpluk (x33-60,y2-26) op (7,23)')
    for s in st:
        sn,dx,dy,lab=s[:4]; v.rand(*sn,dx,dy,(s[5] if len(s)>5 else False),label=lab,diepte=(s[4] if len(s)>4 else 1))
    return v,v.maak()
def kwaal(v,g):
    r=L.rechte(g,v.mask)
    # losse manenpixels / gaten: achtergrondpixels binnen het silhouet naast manen
    gat=sum(1 for x,y in L.ZONE if g[y][x]=='.' and sum(g[y+b][x+a]!='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))>=3)
    return len(r)*10+gat, r
def bouw(N,m):
    st=stukken(N,m); v,g=maak(N,m,st); k,r=kwaal(v,g)
    # rechte manenlijnen breken met de kleine Arcanine-bult (A_BUMP), gespiegeld aan de lichtkant; beste plek per run gezocht
    for _ in range(4):
        if not r: break
        best=None
        for t,a,b0,b1 in r[:1]:
            for fl in (False,True):
                for dx in range(-5,3):
                    for dy in range(-3,2):
                        if t=='v': x,y=a+dx,(b0+b1)//2+dy
                        else: x,y=(b0+b1)//2+dx,a+dy
                        s=(r8.A_BUMP,x,y,'bult tegen rechte lijn',1,fl)
                        vv,gg=maak(N,m,st+[s]); kk,rr=kwaal(vv,gg)
                        if best is None or kk<best[0]: best=(kk,s)
        if best and best[0]<k: st=st+[best[1]]; v,g=maak(N,m,st); k,r=kwaal(v,g)
        else: break
    v.stukken=st
    return v,g
if __name__=='__main__':
    import sys
    from PIL import Image
    V=Image.new('RGB',(3*300,2*280),'white')
    for j,m in enumerate('AB'):
        for i,N in enumerate(VORMEN):
            v,g=bouw(N,m); print(m,N,kwaal(v,g))
            V.paste(L.rgba8(g).crop((2,18,38,52)).resize((288,272),0),(i*300,j*280))
    V.save(sys.argv[1])
