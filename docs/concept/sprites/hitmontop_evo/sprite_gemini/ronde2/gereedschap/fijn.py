# fijn.py x0 y0 x1 y1 [n]: per spritepixel n x n monsters van het model, geklasseerd naar spritepalet-tint (meting).
# 1=zwart 5=donkerbruin 4=schaduw 3=basis 2=licht 6=wit 7=grijs 9=geel .=leeg ; spritekolommen gescheiden door |
import sys,json,numpy as np; from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde2/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+k['model'])).astype(float)
x0,y0,x1,y1=map(int,sys.argv[1:5]); n=int(sys.argv[5]) if len(sys.argv)>5 else 3
def cl(p):
  if p[3]==0: return '.'
  r,g,b=p[:3]; L=(r+g+b)/3
  if L<60: return '1'
  if r>200 and g>180 and b<130: return '9'
  if abs(r-g)<20 and abs(g-b)<20: return '6' if L>225 else '7'
  if r>200 and b<110 and g>150: return '9'
  if L<95: return '5'
  if L<128: return '4'
  if L<162: return '3'
  return '2'
print('    '+''.join(f'{x:<{n+1}d}' for x in range(x0,x1)))
for y in range(y0,y1):
  for j in range(n):
    yy=int(Y0+(y+(j+.5)/n)*s); r=''
    for x in range(x0,x1):
      for i in range(n):
        xx=int(X0+(x+(i+.5)/n)*s); r+=cl(c[yy,xx])
      r+='|'
    print(f'{y:3d} '+r if j==0 else '    '+r)
