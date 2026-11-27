# meting romp (buiten het gezicht): per spritecel op het hi-res model: aandeel zwarte lijnpixels (L<75) en kleurgroep.
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image
im=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float); Lh=lum(im)
PX,FX,PY,FY=5.704,5.16,5.692,3.088; MY,MX=-21,-2
def hblok(y,x):
  r0,c0=MY+3*y,MX+3*x
  return (slice(int(round(FY+r0*PY)),int(round(FY+(r0+3)*PY))),slice(int(round(FX+c0*PX)),int(round(FX+(c0+3)*PX))))
zwart=Lh<75
def lijnfr(y,x): b=hblok(y,x); return zwart[b].mean()
def med(y,x):
  b=hblok(y,x); v=im[b][~zwart[b]]; return np.median(v,0) if len(v) else np.array([0,0,0.])
if __name__=='__main__':
  o=np.load(sys.argv[1])
  ch={0:'.',1:'#',2:'2',3:'3',4:'4',5:'c',6:'b',7:'r',8:'R',9:'p',10:'P',11:'o',12:'O',13:'l',14:'g',15:'G'}
  y0,y1,x0,x1=[int(v) for v in sys.argv[2:6]]
  print('   '+''.join('%-3d'%x for x in range(x0,x1)))
  for y in range(y0,y1):
    s=''
    for x in range(x0,x1):
      f=lijnfr(y,x); s+=ch[o[y,x]]+('L' if f>.25 else 'l' if f>.1 else ' ')+' '
    print('%2d '%y+s)
