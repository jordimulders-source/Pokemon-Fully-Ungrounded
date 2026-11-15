# python3 sprite/maker/kaart.py x0 x1 y0 y1  -> modelhelderheid per spritepixel (p10 en gem, /26)
import sys,numpy as np
exec(open('sprite/meet/px.py').read().split('if __name__')[0])
x0,x1,y0,y1=map(int,sys.argv[1:5])
for nm,f in (('p10',lambda l:np.percentile(l,10)),('gem',lambda l:l.mean())):
  print(nm); print('   '+''.join(str(x%10) for x in range(x0,x1)))
  for y in range(y0,y1):
    r=''
    for x in range(x0,x1):
      b,l=blok(x,y); r+= '.' if l.size==0 else str(min(9,int(f(l)/26)))
    print('%2d %s'%(y,r))
