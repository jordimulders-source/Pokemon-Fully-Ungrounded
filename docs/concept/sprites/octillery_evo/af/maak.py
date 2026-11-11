# maak.py: oplevering Octillery-evolutie uit sprite/r5 (octillery_evo.png = kopie r5, P-mode, index 0 transparant;
# octillery_evo_8x.png = 8x op wit, NEAREST)
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
src=Image.open(D+'/../sprite/r5/octi.png')
assert src.mode=='P' and src.size==(64,64) and src.info.get('transparency')==0
src.save(D+'/octillery_evo.png',transparency=0)
rgba=src.convert('RGBA'); w=Image.new('RGBA',(64,64),(255,255,255,255)); w.alpha_composite(rgba)
w.convert('RGB').resize((512,512),Image.NEAREST).save(D+'/octillery_evo_8x.png')
print('klaar')
