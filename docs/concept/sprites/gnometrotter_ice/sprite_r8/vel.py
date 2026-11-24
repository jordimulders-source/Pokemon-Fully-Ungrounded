# vel.py -> vel.png: r7 | r8, 8x
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'../../gnometrotter_rock/sprite'))
from kijk import sprite; from PIL import Image
ps=[sprite(os.path.join(H,'../sprite_%s/gnometrotter_ice.png'%r)).resize((512,512),Image.NEAREST) for r in ('r7','r8')]
W=Image.new('RGB',(1034,512),'white')
for i,p in enumerate(ps): W.paste(p,(i*522,0))
W.save(os.path.join(H,'vel.png'))
