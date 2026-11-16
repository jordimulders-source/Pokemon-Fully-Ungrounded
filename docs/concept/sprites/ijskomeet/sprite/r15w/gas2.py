import numpy as np; from PIL import Image
o=np.load('r15w/o3.npy'); vap=np.load('r15w/vap.npy'); pal=Image.open('r15w/o3.png').getpalette()
fg=o>0; W,L,G,g=2,3,11,15
def near(mask,j,i,r):
  return mask[max(0,j-r):j+r+1,max(0,i-r):i+r+1].any()
nonvap=fg&~vap
out=o.copy()
for j,i in zip(*np.where(vap)):
  if near(~fg,j,i,1): out[j,i]=L
  elif near(nonvap,j,i,1): out[j,i]=G
  elif near(nonvap,j,i,2) or o[j,i]==G: out[j,i]=g
  else: out[j,i]=W
np.save('r15w/o4.npy',out)
im=Image.fromarray(out.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r15w/o4.png',transparency=0)
big=im.convert('RGB').resize((512,512),Image.NEAREST); big.save('r15w/o4_8x.png')
dk=Image.new('RGB',(150,150),(40,40,56)); dk.paste(im.convert('RGBA').resize((128,128),Image.NEAREST),(11,11),im.convert('RGBA').resize((128,128),Image.NEAREST))
v=Image.new('RGB',(512+20+150,512),'white'); v.paste(big,(0,0)); v.paste(dk,(532,0)); v.paste(im.convert('RGB').resize((128,128),Image.NEAREST),(543,180)); v.save('r15w/o4_vel.png')
