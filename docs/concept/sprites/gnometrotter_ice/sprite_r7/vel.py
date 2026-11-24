# vel.py -> vel.png: model | r5 | r6 | r7, 12x, alleen de benen (x15-51, y40-57)
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(H,'../../gnometrotter_rock/sprite'))
from kijk import sprite, model_op_schaal; from PIL import Image
x0,y0,x1,y1,z=15,40,51,57,12; w,h=(x1-x0)*z,(y1-y0)*z
ps=[model_op_schaal(os.path.join(H,'../r3/gemini_r3_lijf.png'),64*z).crop((x0*z,y0*z,x1*z,y1*z))]
for r in ('r5','r6','r7'): ps.append(sprite(os.path.join(H,'../sprite_%s/gnometrotter_ice.png'%r)).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST))
W=Image.new('RGB',(4*w+30,h),'white')
for i,p in enumerate(ps): W.paste(p,(i*(w+10),0))
W.save(os.path.join(H,'vel.png'))
