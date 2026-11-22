from PIL import Image; import numpy as np, sys
r1=np.asarray(Image.open('r1_nat100.png').convert('RGB')).astype(int)
r2=np.asarray(Image.open('r2_nat100.png').convert('RGB')).astype(int)
dx,dy=int(sys.argv[1]),int(sys.argv[2])
W=np.array([255,255,255])
def wit(p): return p.min()>225
out=r1.copy()
# kop r1 weg
for y in range(0,45):
  for x in range(0,41):
    if y<=44: out[y,x]=W
# kop r2 erop
for y in range(0,46):
  for x in range(0,47):
    inkop = (y<30) or (x<=40)
    if inkop and not wit(r2[y,x]):
      out[y+dy,x+dx]=r2[y,x]
tx,ty=int(sys.argv[3]),int(sys.argv[4])
for y in range(38,85):
  for x in range(70,99): out[y,x]=W
for y in range(44,80):
  for x in range(66,95):
    if not wit(r2[y,x]): out[y+ty,x+tx]=r2[y,x]
Image.fromarray(out.astype('uint8')).save('combi_kop.png')
Image.fromarray(out.astype('uint8')).resize((792,792),Image.NEAREST).save('combi_kop_8x.png')
