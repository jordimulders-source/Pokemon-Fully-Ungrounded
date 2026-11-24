# sprite 8x naast het model (zelfde uitsnede, 8x per spritepixel)
import sys; from PIL import Image
a=Image.open(sys.argv[1]); m=Image.open('natief_A.png' if len(sys.argv)<4 else sys.argv[3]).convert('RGB')
s=82/60; X0,Y0=10,13; ox=2; HO=round(73/s); oy=63-HO
# model zo plaatsen dat het op het spriteraster ligt
mm=m.crop((int(X0-ox*s),int(Y0-oy*s),int(X0-ox*s+64*s),int(Y0-oy*s+64*s))).resize((512,512),Image.NEAREST)
v=Image.new('RGB',(1040,512),'white'); v.paste(a.convert('RGB'),(0,0)); v.paste(mm,(528,0)); v.save(sys.argv[2])
