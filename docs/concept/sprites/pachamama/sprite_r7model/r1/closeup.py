# close-up hoofd: sprite 12x met raster+coordinaten | model (natief_g1) op dezelfde schaal
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image, ImageDraw
o=np.load(sys.argv[1]); y0,y1,x0,x1=11,33,20,40; S=24
MY,MX=np.load('basis_map.npy')
rgb=np.array([[(255,255,255) if v==0 else PAL[v] for v in r] for r in o[y0:y1,x0:x1]],np.uint8)
sp=Image.fromarray(rgb).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
md=Image.open('../natief_g1.png').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
W=sp.width; im=Image.new('RGB',(2*W+10,sp.height),'white'); im.paste(sp,(0,0)); im.paste(md,(W+10,0)); d=ImageDraw.Draw(im)
for off in (0,W+10):
  if len(sys.argv)>3: break
  for k in range(x1-x0+1): d.line([(off+k*S,0),(off+k*S,im.height)],fill=(200,200,200) if k%5 else (255,0,255))
  for k in range(y1-y0+1): d.line([(off,k*S),(off+W,k*S)],fill=(200,200,200) if k%5 else (255,0,255))
for k in range(0,x1-x0,5): d.text((k*S+1,1),str(x0+k),fill=(255,0,0))
for k in range(0,y1-y0,5): d.text((1,k*S+1),str(y0+k),fill=(255,0,0))
im.save(sys.argv[2])
