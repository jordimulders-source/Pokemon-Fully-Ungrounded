from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/coathief/sprite/r3/'
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/7db28f68-7241-59bb-99a2-c407d0c24d8c/scratchpad/'
L=[list(r) for r in open(D+'r3.txt').read().split()]
pal={}
for l in open(D+'palet.txt'):
    if l.startswith('#'): continue
    i,r,g,b=l.split()[:4]; pal[int(i)]=(int(r),int(g),int(b))
orig=[r[:] for r in L]; opal=dict(pal)
def T(x): return [(x[i],x[i+1]) for i in range(0,len(x),2)]
def setp(pts,frm,to):
    for x,y in pts:
        assert L[y][x]==frm,(x,y,L[y][x],frm); L[y][x]=to
# palette
pal[2]=(32,33,36); pal[3]=(56,58,62); pal[4]=(88,92,98)
pal[8]=(176,150,112); pal[13]=(120,96,68)
# crème outline: 8 on outer edge -> D
edge8=[]
for y in range(64):
    for x in range(64):
        if L[y][x]=='8' and any(not(0<=x+dx<64 and 0<=y+dy<64) or L[y+dy][x+dx]=='0' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            edge8.append((x,y))
print('8 op buitenrand -> D:',edge8)
setp(edge8,'8','D')
# head sickle
sick=[(25,36),(25,37),(25,38),(24,39),(24,40),(23,43),(22,43),(21,44),(20,44),(19,45),(18,45),(17,45),(16,46),(15,46),(14,47),(13,47)]
setp(sick,'3','2')
# head top-left selout
sel=[]
for y in range(28,49):
    for x in range(0,24):
        if L[y][x]!='1': continue
        tl=[(dx,dy) for dx,dy in((-1,0),(0,-1)) if L[y+dy][x+dx]=='0']
        inn=[L[y+dy][x+dx] for dx,dy in((1,0),(0,1))]
        if tl and '4' in inn: sel.append((x,y))
print('kop selout 1->2:',sel)
sel+=[(12,36),(12,37),(12,38),(12,39),(12,40)]
setp(sel,'1','2')
setp([(41,35),(42,35),(34,37),(35,37)],'6','7')
setp([(29,33)],'7','5')
pal[5]=(92,44,28); pal[7]=(188,124,62)
leg=[(29,54),(29,55),(28,56),(28,57),(27,58),(26,59),(26,60)]
setp(leg,'3','4')
open(S+'sim.txt','w').write('\n'.join(''.join(r) for r in L))
def img(G,P):
    im=Image.new('RGBA',(64,64),(255,255,255,255)); p=im.load()
    for y in range(64):
        for x in range(64):
            c=int(G[y][x],16)
            if c: p[x,y]=P[c]+(255,)
    return im
for bg,nm in [((255,255,255),'w'),((40,40,60),'d')]:
    W=Image.new('RGB',(1044,512),bg)
    for k,(G,P) in enumerate([(orig,opal),(L,pal)]):
        a=img(G,P); b=Image.new('RGBA',(64,64),bg+(255,)); 
        px=a.load(); bp=b.load()
        for y in range(64):
            for x in range(64):
                if G[y][x]!='0': bp[x,y]=px[x,y]
        W.paste(b.resize((512,512),Image.NEAREST),(k*532,0))
    W.save(S+f'sim2_{nm}.png')
