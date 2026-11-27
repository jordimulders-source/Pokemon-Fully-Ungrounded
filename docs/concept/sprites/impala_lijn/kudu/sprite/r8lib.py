# Ronde 8 gereedschap: Arcanine/Growlithe-vacht 1-op-1 stempelen in de manenzone van de kudu.
import json, numpy as np
from PIL import Image
GP='../../../../../../graphics/pokemon/'
def src(n):
    a=np.array(Image.open(GP+n+'/anim_front_gba.png'))[:64]
    return [''.join('.' if v==0 else '0123456789abcdef'[v] for v in r) for r in a]
ARC=src('arcanine'); GRO=src('growlithe')
# omkleuren naar de manentinten van de kudu (r7-palet): licht l, midden m, lijn d, zwart 0
MAP={'arcanine':{'7':'l','8':'l','9':'m','a':'d','f':'0'},
     'growlithe':{'1':'l','7':'l','8':'m','9':'m','a':'d','f':'0'}}
R6=[list(r) for r in json.load(open('r6/grid.json'))['grid']]
R7=[list(r) for r in json.load(open('r7/grid.json'))['grid']]
KAAL=json.load(open('r6/grid.json'))['kaal']
H,W=len(R6),len(R6[0])
HAAR={(x,y) for y in range(23,48) for x in range(0,33) if R6[y][x] in 'lmd'}
ZONE={(x+a,y+b) for x,y in HAAR for a in(-1,0,1) for b in(-1,0,1)}|{(22,43)}
class Bouw:
    def __init__(s):
        s.g=[r[:] for r in R6]; s.bron={}
        for x,y in HAAR: s.g[y][x]='?'
    def stempel(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label=None,alleen=None):
        S=ARC if naam=='arcanine' else GRO; M=MAP[naam]; n=0
        for sy in range(y0,y1+1):
            for sx in range(x0,x1+1):
                c=S[sy][sx]
                if c not in M: continue
                tx=(dx+(x1-sx) if flip else dx+(sx-x0)); ty=dy+(sy-y0)
                if (tx,ty) not in ZONE: continue
                if alleen and (tx,ty) not in alleen: continue
                cur=s.g[ty][tx]
                if (tx,ty) in HAAR or cur in '.0?' :
                    s.g[ty][tx]=M[c]; s.bron[(tx,ty)]=(label or naam,sx,sy); n+=1
        return n
    def rest(s,buiten='.',lijf='M'):
        # niet-gedekte haarpixels: aan de buitenkant achtergrond, anders lijf (hals/schouder)
        out=set()
        for x,y in HAAR:
            if s.g[y][x]=='?': out.add((x,y))
        return out
    def grid(s): return [''.join(r) for r in s.g]
def toon(g,y0=21,y1=49,x1=36):
    print('   '+''.join(str(x%10) for x in range(x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(g[y][:x1]))
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),
     'W':hx('#FFFFFF'),'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
def png(g,pad,schaal=1):
    H,W=len(g),len(g[0]); OX=(64-W)//2; OY=64-H
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
    return im
def rgba8(g,bg=(255,255,255)):
    H,W=len(g),len(g[0]); OX=(64-W)//2; OY=64-H
    im=Image.new('RGB',(64,64),bg)
    for y in range(H):
        for x in range(W):
            if g[y][x]!='.': im.putpixel((OX+x,OY+y),PAL[g[y][x]])
    return im
MANE='lmd0'
HALS={(x,y) for x,y in ZONE if R6[y][x]=='M' and x<=18 and 23<=y<=41}
def diep(x,y):
    k=0
    while all((x+a,y+b) in HAAR for a in range(-k,k+1) for b in range(-k,k+1)): k+=1
    return k
def snip(naam,x0,y0,x1,y1,flip=False):
    S=ARC if naam=='arcanine' else GRO; M=MAP[naam]; out=[]
    for sy in range(y0,y1+1):
        row=S[sy][x0:x1+1]
        if flip: row=row[::-1]
        out.append(''.join(M.get(c,'.' if c=='.' else '#') for c in row))
    return out
class Bouw2(Bouw):
    def veld(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label='veld'):
        """alleen vultinten l/m (geen lijnen) in HAAR: het schaduwvlak"""
        S=ARC if naam=='arcanine' else GRO; M=MAP[naam]
        for sy in range(y0,y1+1):
            for sx in range(x0,x1+1):
                c=M.get(S[sy][sx])
                if c not in ('l','m'): continue
                tx=dx+((x1-sx) if flip else (sx-x0)); ty=dy+sy-y0
                if (tx,ty) in HAAR and s.g[ty][tx]=='?':
                    s.g[ty][tx]=c; s.bron[(tx,ty)]=(label,naam,sx,sy)
    def vul_rest(s):
        # gaten in het veld: dichtstbijzijnde veldpixel (zelfde bronpixel herhaald)
        import math
        todo=[(x,y) for x,y in HAAR if s.g[y][x]=='?']
        vol=[(x,y) for x,y in HAAR if s.g[y][x] in 'lm']
        for x,y in todo:
            bx,by=min(vol,key=lambda p:(p[0]-x)**2+(p[1]-y)**2)
            s.g[y][x]=s.g[by][bx]; s.bron[(x,y)]=('veld-herhaald',)+tuple(s.bron[(bx,by)][1:])
    def rand(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label='rand',leeg=True,diepte=2):
        """randstuk 1-op-1: vacht + lijnen; '.' in het stuk snijdt de manen weg (leeg=True)"""
        sn=snip(naam,x0,y0,x1,y1,flip)
        h,w=len(sn),len(sn[0]); ext=set(); st=[(i,j) for j in range(h) for i in (0,w-1)]+[(i,j) for i in range(w) for j in (0,h-1)]
        while st:
            i,j=st.pop()
            if not(0<=i<w and 0<=j<h) or (i,j) in ext or sn[j][i]!='.': continue
            ext.add((i,j)); st+=[(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        for j,row in enumerate(sn):
            for i,c in enumerate(row):
                tx,ty=dx+i,dy+j
                if (tx,ty) not in ZONE or c=='#': continue
                cur=s.g[ty][tx]
                if c=='.':
                    if leeg and (tx,ty) in HAAR and (i,j) in ext and diep(tx,ty)<=diepte: s.g[ty][tx]='~'; s.bron.pop((tx,ty),None)
                    continue
                if (tx,ty) in HAAR or cur in '.0~':
                    s.g[ty][tx]=c; s.bron[(tx,ty)]=(label,naam,x0+((x1-x0-i) if flip else i),y0+j)
    def sluit(s):
        # weggesneden '~' -> achtergrond (verbonden met buiten) of lijf; dan open randen sluiten
        H,W=len(s.g),len(s.g[0]); seen=set(); st=[(0,y) for y in range(H)]+[(x,0) for x in range(W)]
        while st:
            x,y=st.pop()
            if not(0<=x<W and 0<=y<H) or (x,y) in seen or s.g[y][x] not in '.~': continue
            seen.add((x,y)); st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for y in range(H):
            for x in range(W):
                if s.g[y][x]=='~':
                    if (x,y) in seen: s.g[y][x]='.'
                    else:
                        nb=[s.g[y+b][x+a] for a,b in((1,0),(-1,0),(0,1),(0,-1)) if s.g[y+b][x+a] in 'MDL']
                        s.g[y][x]=max(set(nb),key=nb.count) if nb else 'M'
                    s.bron[(x,y)]=('lijf/achtergrond na snijden',)
        # open randen: vulpixel naast niet-manen -> lijn (links/boven = d selout, rechts/onder = 0)
        ch=[]
        for x,y in ZONE:
            if s.g[y][x] not in 'lm': continue
            for a,b,lijn in((-1,0,'d'),(0,-1,'d'),(1,0,'0'),(0,1,'0')):
                q=s.g[y+b][x+a]
                if q not in MANE: ch.append((x,y,lijn)); break
        for x,y,c in ch: s.g[y][x]=c; s.bron[(x,y)]=('omtrek-regel',)
def rechte(g,zone):
    """lijnstukken (d/0) in de manenzone: horizontale/verticale runs > 3"""
    out=[]
    for y in range(len(g)):
        run=[]
        for x in range(len(g[0])+1):
            if x<len(g[0]) and (x,y) in zone and g[y][x] in 'd0': run.append(x)
            else:
                if len(run)>3: out.append(('h',y,run[0],run[-1]))
                run=[]
    for x in range(len(g[0])):
        run=[]
        for y in range(len(g)+1):
            if y<len(g) and (x,y) in zone and g[y][x] in 'd0': run.append(y)
            else:
                if len(run)>3: out.append(('v',x,run[0],run[-1]))
                run=[]
    return out

class Vorm:
    """r8-methode: manen = één vorm (masker uit model A3 = r6-haar), rand gerafeld met randstukken uit Arcanine/Growlithe,
    vlak = vultinten uit een Arcanine/Growlithe-vlak, omtrek per regel (licht/boven d, schaduw/onder 0)."""
    def __init__(s):
        s.mask=set(HAAR); s.kleur={}; s.bron={}; s.weg=set()
        for x,y in ZONE-HAAR:   # losse r6-lijnpixels midden in het haar horen bij de manen
            if R6[y][x] in '0d' and sum((x+a,y+b) in HAAR for a,b in((1,0),(-1,0),(0,1),(0,-1)))>=3: s.mask.add((x,y))
    def veld(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label='veld'):
        S=ARC if naam=='arcanine' else GRO; M=MAP[naam]
        for sy in range(y0,y1+1):
            for sx in range(x0,x1+1):
                c=M.get(S[sy][sx])
                if c not in ('l','m'): continue
                tx=dx+((x1-sx) if flip else (sx-x0)); ty=dy+sy-y0
                if (tx,ty) in ZONE and (tx,ty) not in s.kleur:
                    s.kleur[(tx,ty)]=c; s.bron[(tx,ty)]=(label,naam,sx,sy)
    def rand(s,naam,x0,y0,x1,y1,dx,dy,flip=False,label='rand',diepte=1):
        sn=snip(naam,x0,y0,x1,y1,flip); h,w=len(sn),len(sn[0]); ext=set()
        st=[(i,j) for j in range(h) for i in (0,w-1)]+[(i,j) for i in range(w) for j in (0,h-1)]
        while st:
            i,j=st.pop()
            if not(0<=i<w and 0<=j<h) or (i,j) in ext or sn[j][i]!='.': continue
            ext.add((i,j)); st+=[(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        for j,row in enumerate(sn):
            for i,c in enumerate(row):
                t=(dx+i,dy+j); sx=x0+((w-1-i) if flip else i); sy=y0+j
                if t not in ZONE or c=='#': continue
                if c=='.':
                    if (i,j) in ext and t in HAAR and diep(*t)<=diepte: s.mask.discard(t); s.weg.add(t)
                    continue
                if t not in HAAR and not (R6[t[1]][t[0]] in '.0' or (t in ZONE and R6[t[1]][t[0]]=='M' and t not in HALS)): continue
                s.mask.add(t); s.weg.discard(t)
                if c in 'lm': s.kleur[t]=c
                s.bron[t]=(label,naam,sx,sy,c)
    def maak(s,base=None,slagschaduw=False):
        g=[r[:] for r in (base or R6)]
        # weggesneden pixel zonder open kant terug (geen gaten)
        changed=True
        while changed:
            changed=False
            for p in list(s.weg):
                x,y=p
                if all((x+a,y+b) in s.mask for a,b in((1,0),(-1,0),(0,1),(0,-1))): s.mask.add(p); s.weg.discard(p); changed=True
        # pixels die geen manen meer zijn
        H,W=len(g),len(g[0])
        for x,y in HAAR:
            if (x,y) not in s.mask: g[y][x]='~'
        seen=set(); st=[(0,y) for y in range(H)]+[(x,0) for x in range(W)]
        while st:
            x,y=st.pop()
            if not(0<=x<W and 0<=y<H) or (x,y) in seen or g[y][x] not in '.~': continue
            seen.add((x,y)); st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for _ in range(3):
            for y in range(H):
                for x in range(W):
                    if g[y][x]=='~':
                        if (x,y) in seen: g[y][x]='.'; s.bron[(x,y)]=('achtergrond (rand gerafeld)',)
                        else:
                            nb=[g[y+b][x+a] for a,b in((1,0),(-1,0),(0,1),(0,-1)) if g[y+b][x+a] in 'MDL']
                            if nb: g[y][x]=max(set(nb),key=nb.count); s.bron[(x,y)]=('lijf zichtbaar (rand gerafeld)',)
        for y in range(H):
            for x in range(W):
                if g[y][x]=='~': s.mask.add((x,y))   # ingesloten: blijft manen
        # vlak
        vol=[p for p in s.mask if p in s.kleur]
        for p in s.mask:
            x,y=p
            if p in s.kleur: c=s.kleur[p]
            else:
                q=min(vol,key=lambda v:(v[0]-x)**2+(v[1]-y)**2); c=s.kleur[q]; s.bron.setdefault(p,('veld-herhaald',)+tuple(s.bron[q][1:]))
            g[y][x]=c
        # omtrek per regel
        for x,y in s.mask:
            buren=[(a,b) for a,b in((-1,0),(0,-1),(1,0),(0,1)) if (x+a,y+b) not in s.mask and g[y+b][x+a] not in '0DKd']
            if not buren: continue
            if any(a>0 or b>0 for a,b in buren): g[y][x]='0'
            else: g[y][x]='d'
            s.bron.setdefault((x,y),('omtrek',))
        if slagschaduw:
            for x,y in ZONE:
                if g[y][x]=='M' and (x,y) not in HALS and (x-1,y) in s.mask and g[y][x-1]=='0': g[y][x]='D'; s.bron[(x,y)]=('slagschaduw op lijf (Arcanine e/d naast kraag)',)
        return [''.join(r) for r in g]
