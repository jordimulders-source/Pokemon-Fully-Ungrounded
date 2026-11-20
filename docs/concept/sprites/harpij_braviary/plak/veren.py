# Nieuwe kuifveren (eigen vorm, stijl van de r6-veren: grijs, 2 donkere banden, zwarte lijn) op het natieve raster, ACHTER bestaande pixels.
from PIL import Image; import numpy as np, math
nat=np.asarray(Image.open('plak/natief.png')).astype(int)
B=(85,94,108); D=(54,62,74); O=(22,24,30)
def feather(out,base,ang,L,W,bands=((0.30,0.42),(0.62,0.74))):
    dx,dy=math.cos(math.radians(ang)),-math.sin(math.radians(ang))
    H,Wd,_=out.shape; inside=np.zeros((H,Wd),bool); tt=np.zeros((H,Wd))
    for y in range(H):
        for x in range(Wd):
            px,py=x-base[0],y-base[1]
            t=(px*dx+py*dy)/L; s=-px*dy+py*dx
            if 0<=t<=1:
                tc=1-W/L
                w=W if t<=tc else math.sqrt(max(0,W*W-((t-tc)*L)**2))
                if abs(s)<=w: inside[y,x]=True; tt[y,x]=t
    bg=out.mean(2)>225
    for y,x in zip(*np.where(inside)):
        if not bg[y,x]: continue
        edge=any(not(0<=y+a<H and 0<=x+b<Wd and inside[y+a,x+b]) for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        c=O if edge else (D if any(lo<=tt[y,x]<=hi for lo,hi in bands) else B)
        out[y,x]=c
V={ # (basis, hoek, lengte, halve breedte) links en rechts; basis ligt achter de kop
 'A':[((35,21),155,14,3.0),((55,23),15,15,3.0)],
 'B':[((35,22),170,13,3.0),((56,24),0,14,3.0)],
 'C':[((36,20),140,14,3.0),((54,22),30,15,3.0)],
 'D':[((35,21),155,12,3.4),((55,23),15,12,3.4)],
}
tiles=[]
for k,fs in V.items():
    out=nat.copy()
    for f in fs: feather(out,*f)
    im=Image.fromarray(out.astype('uint8')); im.save(f'plak/variant_{k}.png')
    tiles.append(im.crop((15,0,80,40)).resize((65*8,40*8),Image.NEAREST))
vel=Image.new('RGB',(len(tiles)*540,320),'white')
for i,t in enumerate(tiles): vel.paste(t,(i*540,0))
vel.save('plak/varianten_kop.png'); print('ok')
