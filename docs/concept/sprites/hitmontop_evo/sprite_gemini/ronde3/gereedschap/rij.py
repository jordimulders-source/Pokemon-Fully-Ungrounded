# rij.py y0 y1 x0 x1 : per spriterij de modelklassen per halve spritepixel (meting). 1=zwart .=achtergrond
# b=bruin licht B=bruin donker w=wit g=grijs y=geel o=oker G=groen l=lichtgroen u=blauw U=donkerblauw
import sys,json,numpy as np; from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+(sys.argv[5] if len(sys.argv)>5 else k['model']))).astype(float)
MOD=[((198,150,124),'b'),((150,102,78),'B'),((112,76,56),'B'),((248,248,248),'w'),((198,198,200),'g'),
     ((248,216,72),'y'),((180,146,80),'o'),((72,136,64),'G'),((120,184,72),'l'),((88,136,184),'u'),((56,88,136),'U')]
M=np.array([m for m,_ in MOD],float)
y0,y1,x0,x1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:<2d}'[-2:] if x%5==0 else '  ' for x in range(x0,x1)))
for y in range(y0,y1):
  for sub in (0.3,0.7):
    yy=int(Y0+(y+sub)*s); r=''
    for x in range(x0,x1):
      for sx in (0.25,0.75):
        xx=int(X0+(x+sx)*s); xx=min(max(xx,0),c.shape[1]-1)
        p=c[yy,xx]
        if p[3]==0: r+='.'; continue
        if p[:3].mean()<60: r+='1'; continue
        r+=MOD[((M-p[:3])**2).sum(1).argmin()][1]
    print(f'{y:2d}{"ab"[sub>0.5]} '+r)
