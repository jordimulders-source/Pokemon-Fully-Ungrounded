# vel.py -> vel.png: model op schaal | r4 | r5, 8x (gedeelde geometrie uit gnometrotter_rock/sprite/kijk.py)
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'../../gnometrotter_rock/sprite'))
from kijk import sprite, model_op_schaal; from PIL import Image
ps=[model_op_schaal(os.path.join(H,'../r3/gemini_r3_lijf.png'),512),
    sprite(os.path.join(H,'../sprite_r4/gnometrotter_ice.png')).resize((512,512),Image.NEAREST),
    sprite(os.path.join(H,'gnometrotter_ice.png')).resize((512,512),Image.NEAREST)]
W=Image.new('RGB',(3*520,512),'white')
for i,p in enumerate(ps): W.paste(p,(i*520,0))
W.save(os.path.join(H,'vel.png'))
