# zie.py raster out [z]: sprite vergroot | BOX-verkleind model vergroot (zelfde schaal)
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image
from geo import *
import pal
z=int(sys.argv[3]) if len(sys.argv)>3 else 8
s=pal.rgb(pal.load(sys.argv[1])).resize((64*z,64*z),Image.NEAREST)
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
m=src.crop((int(OX),int(OY),int(OX+64*S),int(OY+64*S))).resize((64*z,64*z),Image.LANCZOS)
o=Image.new('RGB',(128*z+8,64*z),'white'); o.paste(s,(0,0)); o.paste(m,(64*z+8,0)); o.save(sys.argv[2])
