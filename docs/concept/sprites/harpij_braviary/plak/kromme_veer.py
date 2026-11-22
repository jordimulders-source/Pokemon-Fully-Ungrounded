# Middelste veer: onderkant als variant E (82°), alleen de top buigt (niet volledig recht). Varianten met verschillende buiging.
import numpy as np, math
from PIL import Image, ImageDraw
ns={}; exec(open('plak/middenveer.py').read().split('out={}')[0],ns)
clear,dicht,D=ns['clear'],ns['dicht'],ns['D']
B=(85,94,108); Dk=(54,62,74); O=(22,24,30)
def bent(out,base,a0,bend,L,W,knik=0.5,bands=((0.30,0.42),(0.62,0.74))):
    # middellijn: recht onder 'knik', daarna buigt de hoek geleidelijk met 'bend' graden
    n=200; pts=[]; x,y=base
    for i in range(n+1):
        t=i/n; a=a0-(bend*((t-knik)/(1-knik))**1.5 if t>knik else 0)
        pts.append((x,y,t)); x+=math.cos(math.radians(a))*L/n; y-=math.sin(math.radians(a))*L/n
    P=np.array(pts); H,Wd,_=out.shape
    inside=np.zeros((H,Wd),bool); tt=np.zeros((H,Wd))
    for yy in range(H):
        for xx in range(Wd):
            d=np.hypot(P[:,0]-xx,P[:,1]-yy); i=d.argmin()
            # ronde punt: straal krimpt alleen op het laatste stuk (zoals de stadionvorm)
            if d[i]<=W and not (i==len(P)-1 and False): inside[yy,xx]=True; tt[yy,xx]=P[i,2]
    bg=out.mean(2)>225
    for yy,xx in zip(*np.where(inside)):
        if not bg[yy,xx]: continue
        edge=any(not(0<=yy+a<H and 0<=xx+b<Wd and inside[yy+a,xx+b]) for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        out[yy,xx]=O if edge else (Dk if any(lo<=tt[yy,xx]<=hi for lo,hi in bands) else B)
V={'H':12,'I':22,'J':32}
tiles=[('D+E',Image.open('plak/variant_D_E.png'))]
for k,bd in V.items():
    a=clear(D); bent(a,(43,17),82,bd,15-2.6,2.6); a=dicht(a)   # lengte = middellijn tot het centrum van de ronde punt
    im=Image.fromarray(a.astype('uint8')); im.save(f'plak/variant_D_{k}.png'); tiles.append((f'D+{k} ({bd}°)',im))
v=Image.new('RGB',(len(tiles)*410,99*5+40),'white'); d=ImageDraw.Draw(v)
for i,(n,t) in enumerate(tiles):
    v.paste(t.crop((10,0,90,99)).resize((400,495),Image.NEAREST),(i*410,40)); d.text((i*410+160,10),n,fill=(0,0,0))
v.save('plak/varianten_krom.png')
z=Image.new('RGB',(len(tiles)*450,260),'white')
for i,(n,t) in enumerate(tiles): z.paste(t.crop((28,0,72,26)).resize((440,260),Image.NEAREST),(i*450,0))
z.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/19dfe9e4-3efd-5231-a28d-9f6e305e37a4/scratchpad/krom.png')
