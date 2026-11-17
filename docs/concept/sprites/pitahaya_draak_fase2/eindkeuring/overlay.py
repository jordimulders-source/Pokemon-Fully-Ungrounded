# overlay.py <sprite> <uit> x0 y0 x1 y1 : sprite 24x met de modelomtrek (natief raster, geo uit sprite_r1/kaal_info.npz) in cyaan
# en de modellijnen (lum<70) als rode stipjes. native x = 2+3*sx, native y = 3*(sy-13).
import sys, numpy as np; from PIL import Image, ImageDraw
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
sp=Image.open(sys.argv[1]).convert('RGBA'); x0,y0,x1,y1=map(int,sys.argv[3:7]); S=24
nat=np.array(Image.open(B+'sprite_r9/natief.png').convert('RGB')).astype(int)
fg=nat.min(2)<225; lum=nat@[0.299,0.587,0.114]
W,H=(x1-x0)*S,(y1-y0)*S
img=Image.new('RGBA',(W,H),(225,232,240,255)); img.alpha_composite(sp.crop((x0,y0,x1,y1)).resize((W,H),Image.NEAREST))
d=ImageDraw.Draw(img)
def P(nx,ny): return (8*nx-16-x0*S, 8*ny+312-y0*S)
for ny in range(nat.shape[0]):
  for nx in range(nat.shape[1]):
    X,Y=P(nx,ny)
    if not(-4<X<W and -4<Y<H): continue
    if fg[ny,nx] and (not fg[ny-1,nx] or not fg[ny+1,nx] or not fg[ny,nx-1] or not fg[ny,nx+1]): d.rectangle([X,Y,X+7,Y+7],fill=(0,220,255,255))
    elif fg[ny,nx] and lum[ny,nx]<70: d.rectangle([X+2,Y+2,X+5,Y+5],fill=(255,0,0,200))
for x in range(x0,x1+1): d.line([((x-x0)*S,0),((x-x0)*S,H)],fill=(0,0,0,40) if x%5 else (0,0,255,120))
for y in range(y0,y1+1): d.line([(0,(y-y0)*S),(W,(y-y0)*S)],fill=(0,0,0,40) if y%5 else (0,0,255,120))
for x in range(x0,x1):
  if x%5==0: d.text(((x-x0)*S+1,1),str(x),fill=(0,0,200,255))
for y in range(y0,y1):
  if y%5==0: d.text((1,(y-y0)*S+1),str(y),fill=(0,0,200,255))
img.convert('RGB').save(sys.argv[2])
