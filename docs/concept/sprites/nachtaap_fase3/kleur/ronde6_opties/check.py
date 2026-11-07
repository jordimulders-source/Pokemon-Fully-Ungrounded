from PIL import Image
B=Image.open('../ronde6/nachtaap_fase3.png'); b=B.load()
bev={'kop/gezicht/maan':(0,14,20,44),'vuistarm':(0,14,26,32),'healerhand+gloed':(1,44,24,64),
     'staart':(44,0,64,42),'onderbeen+dij (r34+ rechts)':(30,34,64,64)}
for n in 'ABC':
    im=Image.open('optie_%s.png'%n); a=im.load()
    assert im.getpalette()[:48]==B.getpalette()[:48]
    d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
    alpha=sum(1 for x,y in d if (a[x,y]==0)!=(b[x,y]==0))
    print(n,'gewijzigd',len(d),'px, waarvan omtrek',alpha,'| zone x%d-%d r%d-%d'%(min(p[0] for p in d),max(p[0] for p in d),min(p[1] for p in d),max(p[1] for p in d)))
    for k,(x0,y0,x1,y1) in bev.items():
        print('   ',k,sum(1 for x,y in d if x0<=x<x1 and y0<=y<y1))
    op=[]
    for y in range(64):
        for x in range(64):
            if a[x,y] in (0,1,2): continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X,Y=x+dx,y+dy
                if not(0<=X<64 and 0<=Y<64) or a[X,Y]==0: op.append((x,y)); break
    print('    open randen (vachtkleur naast transparant) in hele sprite:',len(op), [p for p in op if 26<=p[0]<44 and p[1]<34])
