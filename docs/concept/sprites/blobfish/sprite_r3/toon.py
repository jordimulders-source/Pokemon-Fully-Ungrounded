# toon.py UIT.png IN1.png [IN2.png ...]: sprites naast elkaar op 8x, op lichtgrijs (alleen bekijken)
import sys; from PIL import Image
ims=[Image.open(p) for p in sys.argv[2:]]; z=8
o=Image.new('RGB',(len(ims)*(64*z+8),64*z),(255,255,255))
for k,p in enumerate(ims):
    q=p.convert('RGBA') if p.mode!='P' else p.convert('RGBA')
    b=Image.new('RGBA',(64,64),(214,222,214,255)); b.alpha_composite(q); o.paste(b.convert('RGB').resize((64*z,64*z),Image.NEAREST),(k*(64*z+8),0))
o.save(sys.argv[1])
