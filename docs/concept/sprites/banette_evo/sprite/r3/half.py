# halve-pixelkaart van het model (2x2 per spritepixel): python3 half.py x0 y0 x1 y1
# k zwart  D donkerbruin/oogkas  r rood  o oranje/ring  y geel  g grijs  d donkergrijs  b blauw  w wit/licht  . achtergrond
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(float); r,gg,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3; sat=a.max(2)-a.min(2)
S=968/62; x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
def cls(px):
    R,G,B=px; l=(R+G+B)/3; s=max(px)-min(px)
    if min(px)>=235: return '.'
    if l<45: return 'k'
    if R>190 and G>150 and B<190 and R-B>25: return 'y'
    if R-max(G,B)>40: return 'o' if (G>90 and R>200) else ('r' if l>85 else 'D')
    if B-R>10: return 'b'
    if l<80: return 'D'
    if s<35 and l<115: return 'd'
    if s<35 and l<185: return 'g'
    return 'w'
hdr='      '+''.join(('%-2d'%(i%100)) for i in range(x0,x1))
print(hdr)
for jj in range(2*y0,2*y1):
    row=''
    for ii in range(2*x0,2*x1):
        xa,ya=24+(ii/2-1)*S,1+(jj/2-4)*S; s=S/2
        blk=a[int(round(ya)):int(round(ya+s)),int(round(xa)):int(round(xa+s))].reshape(-1,3).mean(0)
        row+=cls(blk)
    print('%5.1f '%(jj/2)+row)
