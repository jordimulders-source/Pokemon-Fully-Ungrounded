# Reparatie 1-2 (r2): het midden als een paar losse stukken. Elk stuk groeit in het MODEL (natief) vanaf een punt
# op dat stuk, over pixels van hetzelfde materiaal zonder een modellijn over te steken. Wat overblijft in het midden
# (ketting, staafjes, vlekjes, lijnen) hoort bij het dichtstbijzijnde stuk. Lijnen blijven alleen op grenzen tussen
# stukken (of de buitenrand). Uitvoer: stuk-id per natieve pixel (stuk_nat.npy) + overzicht stukken_5x.png.
import numpy as np; from PIL import Image; from collections import deque
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); H,W=a.shape[:2]
fg=a.min(2)<225; L=a@[0.299,0.587,0.114]; line=fg&(L<40); mat=np.where(a[...,0]-a[...,2]>22,1,2)
wiel,schoor,rail,mid=np.load('zones.npy')
# (naam, materiaal 1=roest 2=staal, zaadpunt x,y) -- plekken gemeten op natief.png
ST=[('plank_boven',1,(104,74)),('beugel',2,(103,84)),('staven',1,(108,96)),('bijlplaat',2,(85,106)),
    ('bout_links',2,(65,104)),('plank_links',1,(73,112)),('klinkplaat',1,(80,124)),('klem',2,(96,124)),
    ('stang_onder',2,(75,133)),('onderplaat',2,(88,144)),('ketting',1,(110,135)),('rest_onder',1,(72,141)),('stokken',1,(76,95)),('staven_boven',1,(113,84))]
lab=np.zeros((H,W),int)
for k,(nm,mt,(sx,sy)) in enumerate(ST,1):
    if not mid[sy,sx] or line[sy,sx] or mat[sy,sx]!=mt:
        # zaad op de dichtstbijzijnde geschikte pixel
        best=None
        for r in range(1,9):
            for dy in range(-r,r+1):
                for dx in range(-r,r+1):
                    y,x=sy+dy,sx+dx
                    if mid[y,x] and not line[y,x] and mat[y,x]==mt and not lab[y,x]: best=(x,y); break
                if best: break
            if best: break
        if best is None: print("geen zaad",nm); continue
        sx,sy=best
    if lab[sy,sx]: print('zaad al bezet',nm,'door',ST[lab[sy,sx]-1][0]); continue
    q=[(sy,sx)]; lab[sy,sx]=k
    while q:
        y,x=q.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if mid[ny,nx] and not line[ny,nx] and mat[ny,nx]==mt and not lab[ny,nx]: lab[ny,nx]=k; q.append((ny,nx))
grown=lab.copy()
for k,(nm,_,_) in enumerate(ST,1): print(nm,(grown==k).sum())
# rest van het midden (en lijnen) -> dichtstbijzijnde stuk
dist=np.where(lab>0,0,999); dq=deque(zip(*np.where(lab>0)))
while dq:
    y,x=dq.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if mid[ny,nx] and dist[ny,nx]>dist[y,x]+1: dist[ny,nx]=dist[y,x]+1; lab[ny,nx]=lab[y,x]; dq.append((ny,nx))
np.save('stuk_nat.npy',lab); np.save('stuk_mat.npy',np.array([0]+[m for _,m,_ in ST]))
np.random.seed(5); col=np.random.randint(40,255,(len(ST)+1,3))
img=a.copy(); sel=lab>0; img[sel]=(a[sel]*0.35+col[lab[sel]]*0.65).astype(int)
Image.fromarray(img.astype(np.uint8)).crop((36,44,162,154)).resize((630,550),Image.NEAREST).save('stukken_5x.png')
