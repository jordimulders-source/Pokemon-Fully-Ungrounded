# bewijs: alpha-diff 0, 0 px in bevroren vakken, alleen vachttinten 1-5, open randen
from PIL import Image
B=Image.open('../ronde6/nachtaap_fase3.png'); b=B.load()
bev={'kop/gezicht/maan x0-19 r14-43':(0,14,20,44),'vuistarm x0-25 r14-31':(0,14,26,32),
     'healerhand+gloed x1-23 r44-63':(1,44,24,64),'staartspiraal x>=48':(48,0,64,64),
     'opgeheven voet r0-13':(0,0,64,14),'onderste voet x50-63 r48-63':(50,48,64,64)}
def open_randen(a):
    op=[]
    for y in range(64):
        for x in range(64):
            if a[x,y] in (0,1,2): continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X,Y=x+dx,y+dy
                if not(0<=X<64 and 0<=Y<64) or a[X,Y]==0: op.append((x,y)); break
    return op
ob=open_randen(b)
for n in ['matig','sterk']:
    im=Image.open('optie_%s.png'%n); a=im.load()
    assert im.getpalette()[:48]==B.getpalette()[:48], 'palet'
    d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
    alpha=sum(1 for x,y in d if (a[x,y]==0)!=(b[x,y]==0))
    tint=set((b[x,y],a[x,y]) for x,y in d); buiten=[t for t in tint if not(1<=t[0]<=5 and 1<=t[1]<=5)]
    print('optie',n,': gewijzigd',len(d),'px, alpha-diff',alpha,', zone x%d-%d r%d-%d'%(min(p[0] for p in d),max(p[0] for p in d),min(p[1] for p in d),max(p[1] for p in d)),', niet-vachttinten:',buiten)
    for k,(x0,y0,x1,y1) in bev.items():
        print('    %-34s %d px'%(k,sum(1 for x,y in d if x0<=x<x1 and y0<=y<y1)))
    op=open_randen(a)
    print('    open randen (index>=3 naast transparant): %d, nieuw t.o.v. ronde 6: %d'%(len(op),len(set(op)-set(ob))))
