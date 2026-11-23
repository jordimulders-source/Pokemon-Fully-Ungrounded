# vel.py: r8 | r7b | model (8x); daaronder 1x en 2x naast Gnomad (wit en gras)
import sys; sys.path.insert(0,'../sprite')
from PIL import Image
from kijk import model_op_schaal
def rgba(p): return Image.open(p).convert('RGBA')
r8=rgba('gnometrotter_rock.png'); r7=rgba('r7b_basis.png'); gn=rgba('../../gnomad/af/gnomad.png')
r8.resize((512,512),Image.NEAREST).save('gnometrotter_rock_8x.png')
W=Image.new('RGBA',(3*520,512+150),(255,255,255,255))
for i,im in enumerate([r8,r7]): W.paste(im.resize((512,512),Image.NEAREST),(i*520,0),im.resize((512,512),Image.NEAREST))
W.paste(model_op_schaal(n=512),(1040,0))
y=520; x=10
for bg in [(255,255,255,255),(152,208,160,255)]:
    for im in [r8,gn]:
        for k in (1,2):
            t=im.resize((64*k,64*k),Image.NEAREST); b=Image.new('RGBA',t.size,bg); b.alpha_composite(t); W.paste(b,(x,y+(128-64*k))); x+=64*k+8
    x+=20
W.save('vel.png')
