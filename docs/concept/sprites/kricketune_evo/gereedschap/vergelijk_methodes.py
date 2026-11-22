# vergelijk_methodes.py: kale reductie op drie manieren (weglaten | samenvoegen K wint | samenvoegen buur wint), 8x naast elkaar
import sys; sys.path.insert(0,'gereedschap'); import numpy as np; from PIL import Image
from gemeen import *; import schrap as S
KM={0:0,1:1,2:2,3:3,4:5,5:6,6:7,7:8,8:9,9:10,10:11,11:12}
def naar(s):
    o=np.zeros((64,64),int); H,W=s.shape; b=np.vectorize(KM.get)(s); o[Y0:Y0+H,X0:X0+W]=b; return o
a,c,L=klassen()
A=S.schrap(c)[0]; B=S.schrap_merge(c)[0]
S.PRIO={11:4,5:4,4:4}; C=S.schrap_merge(c)[0]
v=Image.new('RGB',(3*520,512),'white')
for i,s in enumerate((A,B,C)): v.paste(rgb(naar(s),(255,255,255)).resize((512,512),Image.NEAREST),(i*520,0))
v.save(sys.argv[1])
