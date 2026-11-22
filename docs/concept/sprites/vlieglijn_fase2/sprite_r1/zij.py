# zij.py raster.txt S out.png : hele sprite op S x naast het model op dezelfde schaal
import sys,numpy as np; from PIL import Image
from kaal_pal import PAL
a=np.loadtxt(sys.argv[1],dtype=int); S=int(sys.argv[2])
P=np.array(PAL,'uint8'); c=P[a]; c[a==0]=(235,245,235)
sp=Image.fromarray(c).resize((64*S,64*S),Image.NEAREST)
nat=Image.open('natief.png').convert('RGB'); X0,Y0,fx,fy=21,12,109/56,123/63
m=nat.transform(sp.size,Image.EXTENT,(X0-4*fx,Y0-1*fy,X0+60*fx,Y0+63*fy),Image.NEAREST)
v=Image.new('RGB',(64*S*2+10,64*S),'white'); v.paste(sp,(0,0)); v.paste(m,(64*S+10,0)); v.save(sys.argv[3])
