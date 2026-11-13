# q.py x0 y0 x1 y1: per spritepixel 4 kwadranten (linksboven rechtsboven / linksonder rechtsonder) als tekens, zie sub.py
import sys,os,numpy as np; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from geo import *
c=model().astype(float)
x0,y0,x1,y1=map(int,sys.argv[1:5])
def ch(b):
    v=b.reshape(-1,3); l=np.median(v.mean(1)); m=np.median(v,0)
    if m[0]>m[2]+40: return 'R'
    return '#' if l<20 else 'k' if l<60 else 'D' if l<110 else 'C' if l<150 else 'B' if l<190 else 'A' if l<232 else '-'
print('     '+' '.join(f'{x:<2d}' for x in range(x0,x1)))
for Y in range(y0,y1):
  for h in (0,1):
    r=[]
    for X in range(x0,x1):
      s=''
      for w in (0,1):
        ya=int(OY+(Y+h/2)*S); xa=int(OX+(X+w/2)*S); hs=int(S/2)
        s+=ch(c[ya+1:ya+hs-1,xa+1:xa+hs-1])
      r.append(s)
    print((f'{Y:2d}  ' if h==0 else '    ')+' '+' '.join(r))
